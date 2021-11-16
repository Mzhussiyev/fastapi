from datetime import date

from fastapi import APIRouter, Depends, Path, Query
from reporting.db import get_db
from reporting.models.sprint import Sprint, SprintCard, SprintHistory
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
import pandas as pd
import numpy as np

router = APIRouter(prefix="/api/v1/sprint", tags=["sprint"])


@router.get("/{projectkey:str}/history", response_model=SprintHistory)
async def get_sprint_history(
    projectkey: str = Path(
        ..., description="Team for which return sprint history", example="ASARND"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/sprint/history.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"projectkey": projectkey})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    sprints = [Sprint(**row) for row in results]
    sprint_history = SprintHistory(
        items=sprints,
        avg_commitment=round(
            sum(
                filter(
                    lambda commitment: commitment is not None,
                    map(lambda sprint: sprint.commitment, sprints[:3]),
                )
            )
            / len(sprints[:3]),
            2,
        ),
        avg_velocity=round(
            sum(
                filter(
                    lambda velocity: velocity is not None,
                    map(lambda sprint: sprint.velocity, sprints[:3]),
                )
            )
            / len(sprints[:3]),
            2,
        ),
    )
    return sprint_history


@router.get("/timerange", response_model=list[SprintCard])
async def get_sprint_cards(
    since: date = Query(..., description="Period start", example=date(2021, 7, 5)),
    until: date = Query(..., description="Period end", example=date(2021, 7, 9)),
    cluster: str = Query(
        ..., description="Cluster for wich return sprints", example="EA"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/sprint/cards.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"since": since, "until": until})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]
    
    df = pd.DataFrame(results)
    df["commitment_kpi"] = df["completed"] / df["commitment"]
    df.loc[df['commitment_kpi'] >= 1, 'sprint_goal'] = 'Achieved'
    # df.loc[df['commitment_kpi'] < 1, 'sprint_goal'] = 'Not achieved'
    df.loc[(df['commitment_kpi'] < 1) & (df['sprint_enddate'] < date.today()), 'sprint_goal'] = 'Not achieved'
    df['enddate'] = pd.to_datetime(df['sprint_enddate'])
    df['startdate'] = pd.to_datetime(df['sprint_startdate'])
    df['weeks'] = (df['enddate'] - df['startdate']) / np.timedelta64(1, 'W')
    df['weeks'] = df['weeks'].apply(np.ceil, 1).astype(np.int64)
    df = df.drop(columns=['enddate', 'startdate'])
    df['length']  = df['project_key'].str.len()
    df.loc[df['length'] < 3, 'cluster_name'] = 'EA'
    df.loc[df['length'] > 2 ,  'cluster_name'] = 'Fintech'
    df.loc[df['length'] >= 5, 'cluster_name'] = 'Ecosystem'
    df["commitment"] = df["commitment"].replace(np.nan, 0.0)
    df["commitment_kpi"] = df["commitment_kpi"].replace(np.nan, 0.0)
    df["completed"] = df["completed"].replace(np.nan, 0.0)
    df["sprint_goal"] = df["sprint_goal"].replace(np.nan, "-")
    df["project_name"] = df["project_name"].replace(np.nan, "-")    
    results = df.to_dict(orient="records")

    return list(filter(lambda v: v.get("cluster_name") == cluster, results))
