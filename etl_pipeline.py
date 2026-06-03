import os
import random
import pandas as pd
from sqlalchemy import create_engine

def run_arkansas_pipeline():
    print("🚀 Scaling up Arkansas School District Financial Analytics Pipeline...")
    
    # List of real major Arkansas school districts across various counties
    base_districts = [
        {"name": "Heber Springs School District", "county": "Cleburne"},
        {"name": "Little Rock School District", "county": "Pulaski"},
        {"name": "North Little Rock School District", "county": "Pulaski"},
        {"name": "Conway School District", "county": "Faulkner"},
        {"name": "Fayetteville School District", "county": "Washington"},
        {"name": "Bentonville School District", "county": "Benton"},
        {"name": "Searcy School District", "county": "White"},
        {"name": "Cabot School District", "county": "Lonoke"},
        {"name": "Jonesboro School District", "county": "Craighead"},
        {"name": "Fort Smith School District", "county": "Sebastian"},
        {"name": "Texarkana School District", "county": "Miller"},
        {"name": "El Dorado School District", "county": "Union"},
        {"name": "Hot Springs School District", "county": "Garland"},
        {"name": "Russellville School District", "county": "Pope"},
        {"name": "Pine Bluff School District", "county": "Jefferson"}
    ]
    
    # 📡 PHASE 1: GENERATE MULTI-YEAR PRODUCTION DATASET
    print("📡 Synthesizing multi-year historical data metrics...")
    expanded_data = []
    
    # Generating a 5-year trend (2022-2026) for all districts to allow for rolling timeline analysis
    for year in range(2022, 2027):
        for i, base in enumerate(base_districts):
            # Baseline parameters to keep the data realistic
            if "Little Rock" in base["name"]:
                base_enrollment = 21000
                rev_per_student = 8500
            elif "Bentonville" in base["name"]:
                base_enrollment = 18000
                rev_per_student = 8200
            elif "Heber Springs" in base["name"]:
                base_enrollment = 2000
                rev_per_student = 7800
            else:
                base_enrollment = random.randint(3000, 10000)
                rev_per_student = random.randint(7500, 8000)
                
            # Simulate real population shifts (some losing enrollment, some gaining)
            trend_factor = 1 + ((i % 3 - 1) * 0.02) # Creates distinct growth/decline tracks
            enrollment = int(base_enrollment * (trend_factor ** (year - 2022)) * random.uniform(0.98, 1.02))
            
            # Simulate budget calculations
            total_revenue = enrollment * rev_per_student
            # Problem 1: Admin overhead variances (making some top-heavy)
            admin_percent = 0.05 if i % 4 != 0 else 0.095  # Every 4th district is administratively heavy
            admin_exp = int(total_revenue * admin_percent * random.uniform(0.95, 1.05))
            instructional_exp = int(total_revenue * 0.70 * random.uniform(0.97, 1.03))
            
            expanded_data.append({
                "record_id": f"AR-{year}-{i:03d}",
                "fiscal_year": year,
                "district_name": base["name"],
                "county": base["county"],
                "enrollment": enrollment,
                "admin_expenditures": admin_exp,
                "instructional_expenditures": instructional_exp,
                "total_revenue": total_revenue
            })
            
    df = pd.DataFrame(expanded_data)
    print(f"📊 Successfully generated {len(df)} historical public sector data rows.")

    # 🧠 PHASE 2: DATA ENGINEERING & METRIC CALCULATION
    print("🧠 Engineering analytical insights and performance ratios...")
    df['total_expenditures'] = df['admin_expenditures'] + df['instructional_expenditures']
    df['spending_per_student'] = (df['total_expenditures'] / df['enrollment']).round(2)
    df['admin_overhead_ratio'] = (df['admin_expenditures'] / df['instructional_expenditures']).round(4)

    # 🔌 PHASE 3: STORAGE ENGINE EXPORT
    azure_conn_str = os.getenv('AZURE_POSTGRES_CONN')
    if azure_conn_str:
        db_connection_str = azure_conn_str
    else:
        db_connection_str = 'sqlite:///arkansas_analytics.db'
        
    engine = create_engine(db_connection_str)
    df.to_sql('fact_school_finance', engine, if_exists='replace', index=False)
    
    # Overwrite the CSV with the new high-volume dataset
    df.to_csv('arkansas_school_finance.csv', index=False)
    print("✅ ETL pipeline successfully executed. High-volume data warehouse is live!")

if __name__ == "__main__":
    run_arkansas_pipeline()