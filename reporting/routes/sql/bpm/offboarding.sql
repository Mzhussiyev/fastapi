select *
from stage_bpm.offboarding t
where t.start_date between :since and :until