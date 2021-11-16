select company, process_definition_name as process_name, task_name, sum(case when approve_stage = 'Approve' then 1 else 0 end) as Approve,
                                 sum(case when approve_stage = 'Done' then 1 else 0 end) as Done,
                                 sum(case when approve_stage = 'Reject' then 1 else 0 end) as Reject,
                                 sum(case when approve_stage = 'Rework' then 1 else 0 end) as Rework,
                                 sum(case when approve_stage = 'Sign' then 1 else 0 end) as Sign,
                                 sum(case when approve_stage = 'Submit' then 1 else 0 end) as Submit,
                                 sum(case when approve_stage = 'Reasign' then 1 else 0 end) as Reasign,
                                 count(approve_stage) as total
from stage_performance.t_bpm_detailed_tasks vbdt
where (is_active_process = 'completed') and (start_date::date between :since and :until) and ((:name = 'All' and process_definition_name is not null) or (:name != 'All' and process_definition_name = :name))
group by vbdt.company, vbdt.process_definition_name, vbdt.task_name
