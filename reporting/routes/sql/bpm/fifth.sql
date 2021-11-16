select company, process_definition_name as process_name, task_name, assignee, avg(case when avg_task_acl_hours <= 0 then 0 else avg_task_acl_hours end) as hours
from stage_performance.t_bpm_detailed_tasks vbdt
where is_active_process = 'completed' and (start_date between :since and :until) and ((:name = 'All' and process_definition_name is not null) or (:name != 'All' and process_definition_name = :name))
group by vbdt.company, vbdt.process_definition_name, vbdt.task_name, vbdt.assignee
order by hours desc
