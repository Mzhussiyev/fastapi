select process_id, author, start_date, end_date, company, process_definition_name, task_name, assignee, amount, budget_detail, avg_task_acl_hours, is_active_process, approve_stage
from stage_performance.t_bpm_detailed_tasks vbdt
where (start_date::date between :since and :until) and ((:name = 'All' and process_definition_name is not null) or (:name != 'All' and process_definition_name = :name))
