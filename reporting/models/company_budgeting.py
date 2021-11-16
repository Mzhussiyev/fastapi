import datetime
from typing import Optional

from pydantic.main import BaseModel


class CompanyBudgeting(BaseModel):
    date: datetime.date
    payment_order: str
    pppd: str
    actual: str
    cost_center: str
    cash_flow: str
    group_of_budget: str
    budget_detail: str
    currency: str
    receiver: str
    contract: str
    amount: int
    amount_in_tenge: int
    legal_entity: str
