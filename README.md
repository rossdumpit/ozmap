ED Presentations Data Pipeline (AIHW MyHospitals)
Overview

This project builds a batch data pipeline that extracts Emergency Department (ED) presentation data from the Australian Institute of Health and Welfare (AIHW) MyHospitals API, transforms it in Python, loads it into a PostgreSQL database, and exposes analytical endpoints via a FastAPI service. The dataset is further explored using Apache Superset dashboards and Jupyter notebooks for time-series analysis and forecasting experiments.

Data Source

Data is retrieved from the AIHW MyHospitals API:

ED dataset endpoint:
https://myhospitalsapi.aihw.gov.au/api/v1/measure-downloads/myh-ed

The API returns an Excel (.xlsx) file containing structured ED presentation data across:

Reporting units (hospital, state, national levels)
States and territories
Financial years (e.g. 2011–12 format)
Triage categories
Number of ED presentations
Architecture

The system is divided into four main components:

1. Ingestion Layer (API → Raw File)
Python requests used to call AIHW API
Response validated using headers (spreadsheet / octet-stream)
Raw Excel file saved locally as raw.xlsx
2. Transformation Layer (Excel → Clean DataFrame)
Excel file processed using pandas
Header row dynamically detected
Relevant columns extracted:
Reporting unit
Reporting unit type
State
Year
Triage category
Number of presentations
Data cleaning includes:
Converting financial year (2011–12) → integer year (2011)
Handling suppressed values (<5)
Converting numeric types safely
Standardising column names to snake_case
3. Load Layer (DataFrame → PostgreSQL)
PostgreSQL connection managed via environment variables (.env)
Data inserted into ed_pres table using psycopg2
Idempotency enforced using:

    ON CONFLICT (reporting_unit, reporting_unit_type, state, year, triage_cat)
DO NOTHING;

This prevents duplicate ingestion when the pipeline is rerun.

4. Serving Layer (FastAPI → SQL Queries)

FastAPI is used to expose analytical endpoints directly from PostgreSQL.

Endpoints:
GET /top30
Returns top 30 hospitals by total ED presentations.
GET /acuity
Aggregates presentations by state and triage category.
GET /trend
Returns national-level yearly trends by triage category.
GET /triage_catpy
Returns top hospital per triage category per year using window functions.
Data Storage (PostgreSQL)

Main table: ed_pres

Columns:

id (primary key, auto-increment)
reporting_unit
reporting_unit_type
state
year
triage_cat
presentation

Constraints:

Unique constraint on:
(reporting_unit, reporting_unit_type, state, year, triage_cat)

This ensures idempotent inserts.

Analytics Layer
Apache Superset
Used for dashboarding and visual exploration of ED trends
Supports aggregation by state, triage category, and time
Jupyter Notebook
Used for exploratory data analysis
Time-series forecasting experiments using Facebook Prophet
Identified structural distortion in post-2020 data due to COVID-19 impact on ED patterns
Limitations
Data is annual only (financial year granularity)
No real-time or monthly resolution available
Geographic resolution limited to state/territory and reporting unit level (no suburb-level mapping)
COVID-19 period introduces structural breaks in time-series analysis
API provides batch datasets, not streaming updates
Summary

This project demonstrates a full batch data engineering pipeline:

API ingestion
Data transformation and cleaning
Relational database modelling in PostgreSQL
Idempotent data loading
REST API layer using FastAPI
Downstream analytics via Superset and Jupyter
