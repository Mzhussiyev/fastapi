select company, process_definition_name as process_name, task_name, round(avg(avg_task_acl_hours), 2) as hours
from stage_performance.t_bpm_detailed_tasks vbdt
where start_date between :since and :until and ((:name = 'All' and process_definition_name is not null) or (:name != 'All' and process_definition_name = :name))
group by vbdt.company, vbdt.process_definition_name, vbdt.task_name
