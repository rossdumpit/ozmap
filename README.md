# Ozmap — ED Presentations Data Pipeline (AIHW MyHospitals)

## Overview
A batch data pipeline that extracts Emergency Department presentation data from the AIHW MyHospitals API, transforms it in Python, loads it into PostgreSQL, and exposes analytical endpoints via FastAPI.

## Tech Stack
Python, PostgreSQL, FastAPI, psycopg2, pandas, Apache Superset, Jupyter, Facebook Prophet

## Data Source
AIHW MyHospitals API: `https://myhospitalsapi.aihw.gov.au/api/v1/measure-downloads/myh-ed`
Returns an XLSX file covering hospital, state, and national ED presentations by triage category from 2011 to 2024.

## How to Run the Pipeline
```bash
python main.py
```

## How to Run the API
```bash
uvicorn api:app --reload
```

## API Endpoints
- `GET /top30` — Top 30 hospitals by total ED presentations across all years
- `GET /acuity` — Total presentations by state and triage category
- `GET /trend` — National yearly trend by triage category
- `GET /triage_catpy` — Top hospital per triage category per year using window functions

## Database
Table: `ed_pres` — unique constraint on `(reporting_unit, reporting_unit_type, state, year, triage_cat)` enforces idempotent inserts.

## Limitations
- Annual data only, no monthly granularity
- Geography limited to state level, no suburb or postcode
- COVID-19 causes structural breaks in time-series forecasting
