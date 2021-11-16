from fastapi import APIRouter, Depends, Query
from reporting.db import get_db
from reporting.models.cloud_activity import CloudActivity
from sqlalchemy import text
from sqlalchemy.engine import Engine

router = APIRouter(prefix="/api/v1/cloudactivity", tags=["cloud_activity"])


@router.get(
    "/",
    response_model=list[CloudActivity],
    description="Get employees activity in cloud services like Slack, Zoom, Jira, etc.",
)
async def get_cloud_activity(
    projectkey: str = Query(
        ..., description="Team for which return activity", example="ASARND"
    ),
    boardid: int = Query(..., description="ID of JIRA Board", example=73),
    sprintid: int = Query(..., description="ID of the sprint", example=637),
    db_engine: Engine = Depends(get_db),
):
    with open("reporting/routes/sql/cloud_activity.sql", "r") as file:
        sql = text(file.read())

    async with db_engine.connect() as conn:
        cursor = await conn.execute(
            sql, {"projectkey": projectkey, "sprintid": sprintid, "boardid": boardid}
        )
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results
