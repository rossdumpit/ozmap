import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def load(df):

    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv('DB_PASSWORD')
    )

    cursor = conn.cursor()

    query = """
    INSERT INTO ed_pres (
    reporting_unit,    
    reporting_unit_type, 
    state,
    year,           
    triage_cat,         
    presentation
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (reporting_unit, reporting_unit_type, state, year, triage_cat) DO NOTHING;
    """

    for _, row in df.iterrows():
        cursor.execute(query, (row['reporting_unit'], row['reporting_unit_type'], row['state'], row['year'], row['triage_cat'], row['presentation'] if pd.notna(row['presentation']) else None ))

    conn.commit()
    cursor.close()
    conn.close()