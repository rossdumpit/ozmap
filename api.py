from fastapi import FastAPI
import psycopg2
import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def get_db():
    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )
    try:
        yield conn
    finally:
        conn.close()


app = FastAPI()

@app.get("/")
def root():
    return {"message": "ok"}

@app.get("/top30")
def top_20():
    with get_db() as conn:
        with conn.cursor() as cursor:
        
            query=  """
                SELECT reporting_unit, SUM(presentation) AS total_presentation
                FROM ed_pres
                WHERE reporting_unit_type = 'Hospital'
                GROUP BY reporting_unit
                ORDER BY total_presentation DESC
                LIMIT 30;
            """
            cursor.execute(query)
            results = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]
        

@app.get("/acuity")
def acuity():
    with get_db() as conn:
        with conn.cursor() as cursor:
            
            query = """
                SELECT state, triage_cat, SUM(presentation) AS total_presentation
                FROM ed_pres
                WHERE reporting_unit_type = 'State'
                GROUP BY state, triage_cat
            """
            cursor.execute(query)
            results = cursor.fetchall()

            columns= [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]


@app.get("/trend")
def trend():
    with get_db() as conn:
        with conn.cursor() as cursor:
            
            query = """
                SELECT year, triage_cat, SUM(presentation) AS total_presentation
                FROM ed_pres
                WHERE reporting_unit_type = 'National'
                GROUP BY year, triage_cat;
            """
            cursor.execute(query)
            results = cursor.fetchall()

            columns= [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]



@app.get("/triage_catpy")
def triage_catpy():
    with get_db() as conn:
        with conn.cursor() as cursor:
            
            query = """
                WITH agg AS (
                    SELECT
                        year,
                        triage_cat,
                        reporting_unit,
                        SUM(presentation) AS presentation
                    FROM ed_pres
                    WHERE reporting_unit_type = 'Hospital' AND presentation IS NOT NULL
                    GROUP BY year, triage_cat, reporting_unit
                ),
                ranked AS (
                    SELECT
                        year,
                        triage_cat,
                        reporting_unit,
                        presentation,
                        ROW_NUMBER() OVER (
                            PARTITION BY year, triage_cat
                            ORDER BY presentation DESC
                        ) AS rank
                    FROM agg
                )
                SELECT
                    year,
                    triage_cat,
                    reporting_unit,
                    presentation
                FROM ranked
                WHERE rank = 1
                ORDER BY year, triage_cat;
            """
            cursor.execute(query)
            results = cursor.fetchall()

            columns= [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]


        