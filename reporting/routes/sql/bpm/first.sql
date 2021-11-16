select company, count(distinct case when is_active_process = 'completed' then process_id end) as completed,
                                 count(distinct case when is_active_process = 'in progress' then process_id end) as launched,
                                 count(distinct process_id) as total
from stage_performance.t_bpm_detailed_tasks vbdt
where (start_date::date between :since and :until) and ((:name = 'All' and process_definition_name is not null) or (:name != 'All' and process_definition_name = :name))
group by vbdt.company
