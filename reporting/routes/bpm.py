from datetime import date, datetime

from fastapi import APIRouter, Depends, Query
from reporting.db import get_db
from reporting.models.bpm import Reporting, Process, Activity, Cost, Mean, First, Third, Fourth, Fifth, Payload, Offboarding
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

router = APIRouter(prefix="/api/v1/bpm", tags=["bpm"])

@router.get("/reporting", response_model=list[Reporting])
async def get_reporting(
    # period: date = Query(..., description="Period month", example=date(2021, 4, 1)),
    since: date = Query(..., description="Period start", example=date(2021, 8, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 8, 15)),
    name: str = Query(
        ..., description="Process definition name", example="Agreements"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/bpm/bpm.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until, "name" : name})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results

@router.get("/process", response_model=list[Process])
async def get_process(db: AsyncEngine = Depends(get_db)):
    with open("reporting/routes/sql/bpm/process.sql", "r") as file:
        sql = text(file.read())
    async with db.connect() as conn:
        cursor = await conn.execute(sql)
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]
        results.append({'process_definition_name': 'All'})
    return results

@router.get("/activity", response_model=list[Activity])
async def get_activity(
    since: date = Query(..., description="Period start", example=date(2021, 8, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 8, 15)),
    name: str = Query(..., description="Process definition name", example="All"),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/bpm/activity.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until" : until, "name" : name})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]
        for i, s in enumerate(results):
            word_counter = {}
            if s['authors'] is not None:
                for word in s['authors']:
                    if word in word_counter:
                        word_counter[word] += 1
                    else:
                        word_counter[word] = 1
                popular_name = sorted(word_counter, key=word_counter.get, reverse=True)
                top_5 = popular_name[:5]
                results[i]['authors'] = top_5
            else:
                results[i]['authors'] = []
                continue
    return results

@router.get("/cost", response_model=list[Cost])
async def get_cost(
    since: date = Query(..., description="Period start", example=date(2021, 8, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 8, 15)),
    name: str = Query(
        ..., description="Process definition name", example="Agreements"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/bpm/cost.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until, "name" : name})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results

@router.get("/mean", response_model=list[Mean])
async def get_mean(
    since: date = Query(..., description="Period start", example=date(2021, 8, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 8, 15)),
    name: str = Query(
        ..., description="Process definition name", example="Agreements"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/bpm/mean.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until, "name" : name})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results

@router.get("/first", response_model=list[First])
async def get_reporting(
    since: date = Query(..., description="Period start", example=date(2021, 8, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 8, 15)),
    name: str = Query(
        ..., description="Process definition name", example="Agreements"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/bpm/first.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until, "name" : name})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results

@router.get("/third", response_model=list[Third])
async def get_reporting(
    since: date = Query(..., description="Period start", example=date(2021, 8, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 8, 15)),
    name: str = Query(
        ..., description="Process definition name", example="All"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/bpm/third.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until, "name" : name})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results

@router.get("/fourth", response_model=list[Fourth])
async def get_reporting(
    since: date = Query(..., description="Period start", example=date(2021, 8, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 8, 15)),
    name: str = Query(
        ..., description="Process definition name", example="All"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/bpm/fourth.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until, "name" : name})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results

@router.get("/fifth", response_model=list[Fifth])
async def get_reporting(
    since: date = Query(..., description="Period start", example=date(2021, 8, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 8, 15)),
    name: str = Query(
        ..., description="Process definition name", example="All"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/bpm/fifth.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until, "name" : name})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results

@router.get("/payload", response_model=list[Payload])
async def get_reporting(
    since: date = Query(..., description="Period start", example=date(2021, 8, 14)),
    until: date = Query(..., description="Period end", example=date(2021, 8, 15)),
    name: str = Query(
        ..., description="Process definition name", example="Accesses"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/bpm/payload.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until, "name" : name})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results

@router.get("/export")
async def get_export(
    since: date = Query(..., description="Period start", example=date(2021, 9, 1)),
    until: date = Query(..., description="Period end", example=date(2021, 9, 3)),
    name: str = Query(
            ..., description="Process definition name", example="Offboarding"
        ),
    db: AsyncEngine = Depends(get_db),
    ):
    # with open("reporting/routes/sql/bpm/export.sql", "r") as file:
    # sql = text(file.read())
    query = """select * 
            from stage_bpm.{}
            where start_process_date between :since and :until
            order by process_id""".format(name.replace(' ', '_').replace(':', ''))
    sql = text(query)
    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]
        filtered = [d for d in results if d['assignee'] is not None]
    return filtered
