import os
import json
import requests
import pandas as pd
from sqlalchemy import create_engine

def run_arkansas_pipeline():
    print("Initializing Live Arkansas School District Financial Analytics Pipeline...")
    
    year = 2019
    api_url = f"https://educationdata.urban.org/api/v1/school-districts/ccd/finance/{year}/"
    params = {"fips": 5}
    raw_results = []
    
    try:
        print("Attempting connection to live NCES Common Core of Data API gateway...")
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        api_payload = response.json()
        raw_results = api_payload.get('results', [])
        print("Successfully connected to live remote server.")
    except Exception as e:
        print(f"Network Connection Restricted: {e}")
        print("Routing ingestion through local raw public sector data mirror...")
        
        backup_path = 'raw_api_backup.json'
        if os.path.exists(backup_path):
            with open(backup_path, 'r') as f:
                backup_payload = json.load(f)
                raw_results = backup_payload.get('results', [])
        else:
            print("Critical System Error: Local backup data mirror missing. Pipeline aborted.")
            return

    if not raw_results:
        print("Ingestion failed: No valid metadata rows loaded.")
        return

    df_raw = pd.DataFrame(raw_results)
    print(f"Successfully processed {len(df_raw)} authentic public sector rows.")
    
    print("Beginning data engineering and transformation sequence...")
    
    # Precise schema map matching the exact live API columns
    schema_cols = {
        'leaid': 'district_id',
        'year': 'fiscal_year',
        'enrollment_fall_responsible': 'enrollment',
        'rev_total': 'total_revenue',
        'exp_instruction': 'instructional_expenditures',
        'exp_current_supp_serve_total': 'admin_expenditures',
        'exp_total': 'total_expenditures'
    }
    
    # Select columns that exist in the dataframe to prevent key exceptions
    df = df_raw[[col for col in schema_cols.keys() if col in df_raw.columns]].rename(columns=schema_cols).copy()
    
    # Cast variables to numeric floating points
    numeric_fields = ['enrollment', 'total_revenue', 'instructional_expenditures', 'admin_expenditures', 'total_expenditures']
    for field in numeric_fields:
        if field in df.columns:
            df[field] = pd.to_numeric(df[field], errors='coerce')
        
    # Data Engineering Cleaning Layer: Drop records containing missing indicators (-1) or zero fields
    df = df[
        (df['enrollment'] > 0) & 
        (df['total_revenue'] > 0) & 
        (df['instructional_expenditures'] > 0) & 
        (df['admin_expenditures'] > 0)
    ].copy()

    # Feature Engineering: Compute real analytical performance indexes
    df['spending_per_student'] = (df['total_expenditures'] / df['enrollment']).round(2)
    df['admin_overhead_ratio'] = (df['admin_expenditures'] / df['instructional_expenditures']).round(4)
    df['state_code'] = "AR"

    # Multi-Target Database Router Configuration
    azure_conn_str = os.getenv('AZURE_POSTGRES_CONN')
    if azure_conn_str:
        db_connection_str = azure_conn_str
    else:
        db_connection_str = 'sqlite:///arkansas_analytics.db'
        
    engine = create_engine(db_connection_str)
    
    df.to_sql('fact_school_finance', engine, if_exists='replace', index=False)
    df.to_csv('arkansas_school_finance.csv', index=False)
    
    print(f"ETL pipeline successfully executed. {len(df)} production rows committed to warehouse.")

if __name__ == "__main__":
    run_arkansas_pipeline()