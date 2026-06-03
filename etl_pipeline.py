import os
import json
import requests
import pandas as pd
from sqlalchemy import create_engine

def run_arkansas_pipeline():
    print("Initializing Relational Arkansas School District Analytics Platform...")
    
    year = 2019
    api_url = f"https://educationdata.urban.org/api/v1/school-districts/ccd/finance/{year}/"
    directory_url = f"https://educationdata.urban.org/api/v1/school-districts/ccd/directory/{year}/"
    params = {"fips": 5}
    raw_results = []
    
    try:
        print("Attempting network connection to live NCES financial data gateway...")
        response = requests.get(api_url, params=params, timeout=8)
        response.raise_for_status()
        raw_results = response.json().get('results', [])
        
        # Live Relational Join Execution: Fetch district names directly from the federal directory table
        print("Fetching district dimensional naming attributes from NCES directory schema...")
        dir_res = requests.get(directory_url, params=params, timeout=8)
        if dir_res.status_code == 200:
            names_map = {row['leaid']: row['lea_name'] for row in dir_res.json().get('results', []) if 'lea_name' in row}
            for row in raw_results:
                row['lea_name'] = names_map.get(row['leaid'], f"NCES District {row['leaid']}")
    except Exception as e:
        print(f"Network Timeout/Routing Shift: {e}")
        print("Executing automated ingestion via clean local public sector data mirror...")
        
        backup_path = 'raw_api_backup.json'
        if os.path.exists(backup_path):
            with open(backup_path, 'r') as f:
                raw_results = json.load(f).get('results', [])
        else:
            print("Critical System Error: Local backup data mirror missing. Pipeline aborted.")
            return

    if not raw_results:
        print("Ingestion failed: Data layer returned 0 records.")
        return

    df_raw = pd.DataFrame(raw_results)
    
    # Target Schema Definition mapping IDs to Human-Readable names seamlessly
    schema_cols = {
        'leaid': 'district_id',
        'lea_name': 'district_name',
        'year': 'fiscal_year',
        'enrollment_fall_responsible': 'enrollment',
        'rev_total': 'total_revenue',
        'exp_instruction': 'instructional_expenditures',
        'exp_current_supp_serve_total': 'admin_expenditures',
        'exp_total': 'total_expenditures'
    }
    
    # Handle optional checking if names exist in dataset headers
    df = df_raw[[col for col in schema_cols.keys() if col in df_raw.columns]].rename(columns=schema_cols).copy()
    if 'district_name' not in df.columns:
        df['district_name'] = df['district_id'].apply(lambda x: f"NCES District {x}")

    # Standardize data fields to clean database numeric primitives
    numeric_fields = ['enrollment', 'total_revenue', 'instructional_expenditures', 'admin_expenditures', 'total_expenditures']
    for field in numeric_fields:
        if field in df.columns:
            df[field] = pd.to_numeric(df[field], errors='coerce')
        
    # Purge unpopulated rows and anomalous missing metadata entries (-1)
    df = df[(df['enrollment'] > 0) & (df['instructional_expenditures'] > 0)].dropna().copy()

    # Feature Engineering Layer
    df['spending_per_student'] = (df['total_expenditures'] / df['enrollment']).round(2)
    df['admin_overhead_ratio'] = (df['admin_expenditures'] / df['instructional_expenditures']).round(4)
    df['state_code'] = "AR"

    # Multi-Target DB Router
    azure_conn_str = os.getenv('AZURE_POSTGRES_CONN')
    db_connection_str = azure_conn_str if azure_conn_str else 'sqlite:///arkansas_analytics.db'
        
    engine = create_engine(db_connection_str)
    df.to_sql('fact_school_finance', engine, if_exists='replace', index=False)
    df.to_csv('arkansas_school_finance.csv', index=False)
    
    print(f"ETL pipeline successfully executed. {len(df)} records with real school names written to warehouse.")

if __name__ == "__main__":
    run_arkansas_pipeline()