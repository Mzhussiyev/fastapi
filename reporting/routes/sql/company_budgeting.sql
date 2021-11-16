select
    tcb.date,
    tcb.payment_order,
    tcb.pppd,
    tcb.actual,
    tcb.cost_center,
    tcb.cash_flow,
    tcb.group_of_budget,
    tcb.budget_detail,
    tcb.currency,
    tcb.receiver,
    tcb.contract,
    tcb.amount,
    tcb.amount_in_tenge,
    tcb.legal_entity
from stage_1c.t_company_budgeting tcb
where tcb.date >= :since and tcb.date<= :until
