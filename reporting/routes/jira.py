from fastapi import APIRouter, Depends, Path, Query
from reporting.db import get_db
from reporting.models.jira import (
    ActionPlan,
    Board,
    Bugs,
    Burndown,
    PlannedStoryPoints,
    PlannedTask,
    Project,
    SprintName,
    TeamDynamics,
    TeamParameters,
)
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

router = APIRouter(prefix="/api/v1/jira", tags=["jira"])


@router.get("/projects", response_model=list[Project])
async def get_projects(db: AsyncEngine = Depends(get_db)):
    with open("reporting/routes/sql/jira/projects_list.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql)
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results


@router.get("/boards", response_model=list[Board])
async def get_boards(
    projectkey: str = Query(
        ..., description="Project for which return boards", example="ASARND"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/jira/boards_list.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"projectkey": projectkey})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results


@router.get("/actionplan", response_model=list[ActionPlan])
async def get_action_plan(
    projectkey: str = Query(
        ..., description="Project for which return action plan", example="ASARND"
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/jira/action_plan.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"projectkey": projectkey})
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results


@router.get(
    "/{projectkey:str}/{boardid:int}/sprintnames", response_model=list[SprintName]
)
async def get_sprint_names(
    projectkey: str = Path(
        ..., description="Project for which return sprint names", example="ASARND"
    ),
    boardid: int = Path(
        ..., description="Board for which return sprint names", example=73
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/jira/sprint_names.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"projectkey": projectkey, "boardid": boardid})

        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results


@router.get("/teamparameters", response_model=list[TeamParameters])
async def get_team_parameters(
    projectkey: str = Query(
        ..., description="Project for which return team parameters", example="ASARND"
    ),
    boardid: int = Query(
        ..., description="Board for which return team parameters", example=73
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/jira/team_parameters.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(sql, {"projectkey": projectkey, "boardid": boardid})
        results = [
            {
                k: 0 if v is None and k in ("commitment", "completed") else v
                for k, v in zip(cursor.keys(), row)
            }
            for row in cursor.all()
        ]

    try:
        commitment = round(
            results[0].get("completed") / results[0].get("commitment"), 2
        )
    except ZeroDivisionError:
        commitment = 0.0

    velocity = round(results[0].get("completed"), 2)

    avg_velocity = round(
        sum(map(lambda v: v.get("completed"), results)) / len(results), 2
    )
    avg_commitment = round(
        sum(
            map(
                lambda v: v.get("completed") / v.get("commitment")
                if v.get("commitment") != 0
                else 0,
                results,
            )
        )
        / len(results),
        2,
    )

    return [
        {
            "project_key": projectkey,
            "board_id": boardid,
            "commitment": commitment,
            "velocity": velocity,
            "avg_commitment": avg_commitment,
            "avg_velocity": avg_velocity,
        }
    ]


@router.get("/plannedtasks", response_model=list[PlannedTask])
async def get_planned_tasks(
    projectkey: str = Query(
        ..., description="Project for which return planned tasks", example="ASARND"
    ),
    boardid: int = Query(
        ..., description="Board for which return planned tasks", example=73
    ),
    sprintid: int = Query(
        ..., description="Sprint for which return planned tasks", example=637
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/jira/planned_tasks.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(
            sql, {"projectkey": projectkey, "boardid": boardid, "sprintid": sprintid}
        )
        # result = [{k: v for k, v in zip(cursor.keys(), cursor.first())}]
        result = [dict(zip(cursor.keys(), row)) for row in cursor.all()]
    return result


@router.get("/plannedstorypoints", response_model=list[PlannedStoryPoints])
async def get_planned_storypoints(
    projectkey: str = Query(
        ...,
        description="Project for which return planned story points",
        example="ASARND",
    ),
    boardid: int = Query(
        ..., description="Board for which return planned story points", example=73
    ),
    sprintid: int = Query(
        ..., description="Sprint for which return planned story points", example=637
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/jira/planned_storypoints.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(
            sql, {"projectkey": projectkey, "boardid": boardid, "sprintid": sprintid}
        )
        # result = {k: v for k, v in zip(cursor.keys(), cursor.first())}
        result = [dict(zip(cursor.keys(), row)) for row in cursor.all()]
    return result


@router.get(
    "/burndown",
    response_model=list[Burndown],
)
async def get_burndown(
    projectkey: str = Query(
        ..., description="Project for which return burndown", example="ASARND"
    ),
    boardid: int = Query(
        ..., description="Board for which return burndown", example=73
    ),
    sprintid: int = Query(
        ..., description="Sprint for which return burndown", example=637
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/jira/burndown.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(
            sql, {"projectkey": projectkey, "boardid": boardid, "sprintid": sprintid}
        )
        results = [{k: v for k, v in zip(cursor.keys(), row)} for row in cursor.all()]

    return results


@router.get("/bugs", response_model=list[Bugs])
async def get_bugs(
    projectkey: str = Query(
        ..., description="Project for which return bugs", example="ASARND"
    ),
    boardid: int = Query(..., description="Board for which return bugs", example=73),
    sprintid: int = Query(..., description="Sprint for which return bugs", example=637),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/jira/bugs.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(
            sql, {"projectkey": projectkey, "boardid": boardid, "sprintid": sprintid}
        )
        result = [
            {
                k: 0
                if v is None and k not in ("project_key", "board_id", "sprint_id")
                else v
                for k, v in zip(cursor.keys(), row)
            }
            for row in cursor.all()
        ]

    return result


@router.get("/teamdynamics", response_model=list[TeamDynamics])
async def get_team_dynamics(
    projectkey: str = Query(
        ..., description="Project for which return team dynamics", example="ASARND"
    ),
    boardid: int = Query(
        ..., description="Board for which return team dynamics", example=73
    ),
    sprintid: int = Query(
        ..., description="Sprint for which return team dynamics", example=637
    ),
    db: AsyncEngine = Depends(get_db),
):
    with open("reporting/routes/sql/jira/team_dynamics.sql", "r") as file:
        sql = text(file.read())

    async with db.connect() as conn:
        cursor = await conn.execute(
            sql, {"projectkey": projectkey, "boardid": boardid, "sprintid": sprintid}
        )
        result = {k: v for k, v in zip(cursor.keys(), cursor.first())}

    result.update(
        {"project_key": projectkey, "board_id": boardid, "sprint_id": sprintid}
    )

    return [result]
