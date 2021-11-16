with completed as (
	select tdc.process_definition_name, coalesce(tdc.company, '-') as company, count(distinct tdc.process_id) as completed
	from stage_performance.t_dmsbpm_completed tdc
	where tdc.end_process_date::date between :since and :until
	group by tdc.process_definition_name, tdc.company
),
inprocess as (
	select tds.process_definition_name, coalesce(tds.company, '-') as company, count(distinct tds.process_id) as inprocess
	from stage_performance.t_dmsbpm_started tds
	left join stage_performance.t_dmsbpm_completed tdc on tds.process_id = tdc.process_id
	WHERE tdc.process_id is null and tds.start_process_date::date between :since and :until
	group by tds.process_definition_name, tds.company
),
author as (
	select tds.process_definition_name, coalesce(tds.company, '-') as company, array_agg(tds.author ) as authors
	from stage_performance.t_dmsbpm_started tds
	WHERE tds.start_process_date::date between :since and :until
	group by tds.process_definition_name, tds.company
),
joined as (
	select coalesce (c.process_definition_name, i.process_definition_name) as process_name, coalesce (c.company, i.company) as company_name, c.completed, i.inprocess
	from completed c
	full outer join inprocess i on
	c.process_definition_name = i.process_definition_name and c.company = i.company
)
select j.process_name, j.company_name as company, coalesce(j.completed, 0) as completed, coalesce(j.inprocess, 0) as launched, a.authors
from joined as j
left join author a on
	j.process_name = a.process_definition_name and j.company_name = a.company
where (:name = 'All' and j.process_name is not null) or (:name != 'All' and j.process_name = :name)
group by j.process_name, j.company_name, j.completed, j.inprocess, a.authors