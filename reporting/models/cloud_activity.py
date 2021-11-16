import datetime
from typing import Optional

from pydantic.main import BaseModel


class CloudActivity(BaseModel):
    login: Optional[str]
    username: str
    dtime_start: datetime.datetime
    dtime_end: datetime.datetime
    ddate: datetime.date
    platform: str
