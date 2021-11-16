select *
from stage_performance.v_bpm_reporting vbr
where start_date between :since and :until and ((:name = 'All' and process_definition_name is not null) or (:name != 'All' and process_definition_name = :name))

