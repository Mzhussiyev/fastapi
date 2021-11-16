from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, validator



class Project(BaseModel):
    project_key: str
    project_name: str


class Board(BaseModel):
    project_key: str
    board_id: int


class SprintName(Board):
    sprint_id: int
    sprint_name: str


class ActionPlan(BaseModel):
    project_key: str
    issue_key: str
    issue_name: str
    created_date: date


class PlannedTask(BaseModel):
    project_key: str
    board_id: int
    sprint_id: int
    planned_tasks: int
    resolved_tasks: int
    unresolved_tasks: int
    cancelled_tasks: int
    removed_tasks: int
    percentage: int
    days_remaining: int


class PlannedStoryPoints(BaseModel):
    project_key: str
    board_id: int
    sprint_id: int
    planned_storypoints: Optional[int]
    resolved_storypoints: Optional[int]
    unresolved_storypoints: Optional[int]
    removed_storypoints: Optional[int]
    percentage: Optional[int]

    class Config:
        validate_assignment = True

    @validator(
        "planned_storypoints",
        "resolved_storypoints",
        "unresolved_storypoints",
        "removed_storypoints",
        "percentage"
    )
    def none_to_zero(cls, value):
        """Assign None values to zero
        """
        return value or 0


class Burndown(BaseModel):
    project_key: Optional[str]
    board_id: Optional[int]
    sprint_id: Optional[int]
    issue_date: Optional[datetime]
    issue_key: Optional[str]
    event_detail: Optional[str]
    difference: Optional[int]
    remaining: Optional[int]
    sprint_startdate: Optional[datetime]
    sprint_enddate: Optional[datetime]
    sprint_completedate: Optional[datetime]


class Bugs(BaseModel):
    project_key: str
    board_id: int
    sprint_id: int
    bugs: int
    resolved_bugs: int
    unresolved_bugs: int
    cancelled_bugs: int
    removed_bugs: int


class TeamParameters(BaseModel):
    project_key: str
    board_id: int
    commitment: float
    velocity: float
    avg_commitment: float
    avg_velocity: float


class TeamDynamics(BaseModel):
    project_key: str
    board_id: int
    sprint_id: int
    time_off: int
    total_team_member: int
