# OzMap — Australian ED Presentations Pipeline

## Overview
A batch data engineering pipeline that extracts Emergency Department presentation data from the AIHW MyHospitals API, transforms and cleans it in Python, loads it into PostgreSQL, and serves it via a FastAPI layer. Includes a frontend dashboard and Dagster orchestration.

## Tech Stack
Python, FastAPI, PostgreSQL, Neon, psycopg2, pandas, Alembic, Docker, Dagster, Apache Superset

## Data Source
AIHW MyHospitals API: `https://myhospitalsapi.aihw.gov.au/api/v1/measure-downloads/myh-ed`

Returns an XLSX file covering hospital, state, and national ED presentations by triage category from 2011 to 2024. Data is annual only and updated once per financial year.

## Project Structure
- `ingest.py` — HTTP extraction from AIHW API with response validation
- `transform.py` — Excel parsing, header detection, cleaning, type coercion
- `load.py` — Idempotent upsert into PostgreSQL using ON CONFLICT DO NOTHING
- `api.py` — FastAPI endpoints querying PostgreSQL
- `pipeline.py` — Dagster asset pipeline with yearly schedule
- `alembic/` — Database migrations

## How to Run with Docker

```bash
docker compose up -d
alembic upgrade head
python main.py
```

## How to Run Locally

```bash
python main.py       # run pipeline
uvicorn api:app --reload   # start API
```

## API Endpoints
- `GET /top30` — Top 30 hospitals by total ED presentations
- `GET /acuity` — Presentations by state and triage category
- `GET /trend` — National yearly trend by triage category
- `GET /triage_catpy` — Top hospital per triage category per year (window function)

## Database
Table `ed_pres` has a unique constraint on `(reporting_unit, reporting_unit_type, state, year, triage_cat)` which enforces idempotent inserts. Schema is managed via Alembic migrations.

## Limitations
- Annual data only, no monthly granularity available via the public API
- Geography is limited to state and reporting unit level, no postcode or suburb
- COVID-19 introduces a structural break in 2020-21 that affects any time-series analysis
