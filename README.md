# DAR Reporting API

## Development server
### https://reporting-api.dar-dev.zone/

## Prerequisites
- **Python 3.9.6**
- `asyncpg==0.23.0`
- `fastapi==0.65.2`
- `gunicorn==20.1.0`
- `psycopg2-binary==2.9.1`
- `SQLAlchemy==1.4.20`
- `uvicorn==0.14.0`
- `pydantic==1.8.2`

## Running

Install requirements via `pip install -r requirements.txt`

Create `.env` file for configuration. Place `DB_URL` parameter inside of format `postgresql+asyncpg://<db_user>:<password>@<db_host>:<db_port>/<db_name>`

Run via `uvicorn --env-file .env --reload reporting.main:app`

Documentation page will be available at http://localhost:8000/