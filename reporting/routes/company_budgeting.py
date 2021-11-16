from datetime import date
from fastapi import APIRouter, Depends, Query
from reporting.db import get_db
from reporting.models.company_budgeting import CompanyBudgeting
from sqlalchemy import text
from sqlalchemy.engine import Engine

router = APIRouter(prefix="/api/v1/companybudgeting", tags=["company_budgeting"])


@router.get(
    "/",
    response_model=list[CompanyBudgeting],
    description="Get budgeting history of our company",
)
async def get_company_budgeting(
    since: date = Query(..., description="Period start", example=date(2021, 10, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 10, 9)),
    db_engine: Engine = Depends(get_db),
):
    with open("reporting/routes/sql/company_budgeting.sql", "r") as file:
        sql = text(file.read())

    async with db_engine.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results
