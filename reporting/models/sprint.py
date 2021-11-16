from datetime import date
from typing import Optional

from pydantic import BaseModel


class Sprint(BaseModel):
    sprint_id: int
    board_id: int
    sprint_name: str
    status: Optional[str]
    sprint_startdate: date
    sprint_enddate: date
    commitment: Optional[float]
    velocity: Optional[int]
    tasks_plan: Optional[int]
    tasks_fact: Optional[int]
    new_bugs: int = 0
    resolved_bugs: int = 0
    team_members: int = 0


class SprintHistory(BaseModel):
    items: list[Sprint]
    avg_commitment: float
    avg_velocity: int


class SprintCard(BaseModel):
    project_key: str
    board_id: int
    project_name: str
    sprint_id: int
    sprint_name: str
    sprint_startdate: date
    sprint_enddate: date
    commitment: float
    completed: float
    employee: int
    commitment_kpi: float
    sprint_goal: str
    weeks: int
    cluster_name: str
