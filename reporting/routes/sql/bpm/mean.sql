select
	   month_,
	   process_definition_name,
	   avg(avg_task_acl_days) as avg_task_acl_days
from stage_performance.v_bpm_reporting vbr
where coalesce(avg_task_acl_days, 0) > 0 and is_active_process = 0 and  vbr.start_date between :since and :until  and ((:name = 'All' and vbr.process_definition_name is not null) or (:name != 'All' and vbr.process_definition_name = :name))
group by month_, process_definition_name
order by avg_task_acl_days desc