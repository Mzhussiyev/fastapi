select month_,
	   process_definition_name,
	   coalesce(nullif(company, ''), 'Unknown') as company,
	   sum(amount) as amoutn
from stage_performance.v_bpm_reporting vbr
where amount > 0 and (vbr.start_date between :since and :until) and ((:name = 'All' and vbr.process_definition_name is not null) or (:name != 'All' and vbr.process_definition_name = :name))
group by month_, process_definition_name, coalesce(nullif(company, ''), 'Unknown')
order by amoutn desc