import datetime
from typing import Optional

from pydantic.main import BaseModel

class Reporting(BaseModel):
    month_: datetime.date
    start_date: datetime.date
    author: Optional[str]
    process_definition_name: Optional[str]
    company: Optional[str]
    is_active_process: Optional[int]
    cnt_task: Optional[int]
    amount: Optional[int]
    avg_task_acl_days: Optional[int]
    cnt_process: Optional[int]

class Process(BaseModel):
    process_definition_name: Optional[str]

class Activity(BaseModel):
    process_name: Optional[str]
    company: Optional[str]
    completed: Optional[int]
    launched: Optional[int]
    authors: Optional[list]

class Cost(BaseModel):
    month_: datetime.date
    process_definition_name: Optional[str]
    company: Optional[str]
    amoutn: Optional[int]

class Mean(BaseModel):
    month_: datetime.date
    process_definition_name: Optional[str]
    avg_task_acl_days: Optional[str]

class First(BaseModel):
    company: Optional[str]
    completed: Optional[int]
    launched: Optional[int]
    total: Optional[int]

class Third(BaseModel):
    company: Optional[str]
    process_name: Optional[str]
    task_name: Optional[str]
    approve: Optional[int]
    done: Optional[int]
    reject: Optional[int]
    rework: Optional[int]
    sign: Optional[int]
    submit: Optional[int]
    reasign: Optional[int]
    total: Optional[int]

class Fourth(BaseModel):
    company: Optional[str]
    process_name: Optional[str]
    task_name: Optional[str]
    hours: Optional[float]

class Fifth(BaseModel):
    company: Optional[str]
    process_name: Optional[str]
    task_name: Optional[str]
    assignee: Optional[str]
    hours: Optional[float]

class Payload(BaseModel):
    process_id: Optional[str]
    author: Optional[str]
    start_date: datetime.date
    end_date: datetime.date
    company: Optional[str]
    process_definition_name: Optional[str]
    task_name: Optional[str]
    assignee: Optional[str]
    amount: Optional[int]
    budget_detail: Optional[str]
    avg_task_acl_hours: Optional[int]
    is_active_process: Optional[str]
    approve_stage: Optional[str]

class Offboarding(BaseModel):
    author: Optional[str]
    process_id: Optional[str]
    start_date: datetime.date
    end_date: datetime.date
    process_definition_name: Optional[str]
    task_name: Optional[str]
    assignee: Optional[str]
    company: Optional[str]
    employee_select: Optional[str]
    approve_stage: Optional[str]
    task_status: Optional[str]
    termination_date: datetime.date
