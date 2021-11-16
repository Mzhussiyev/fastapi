with team_members as (
select
	distinct
	case
		when coalesce(resolvedby, null) != null then resolvedby
		when coalesce(assignee, null) != null then assignee
		else reporter
	end as username
from
	stage_performance.jira_new_data
where
	project_key = :projectkey
),
sprint_dates as (
	select distinct sprint_startdate, sprint_enddate
	from stage_performance.t_jira_sprint_report
	where board_id = :boardid and sprint_id = :sprintid and project_key = :projectkey
)
select distinct 
	ca.login,
	ca.username,
	ca.dtime_start,
	ca.dtime_end,
	ca.ddate,
	ca.platform
from
	stage_performance.t_dar_employee_cloud_activity_log ca --stage_performance.v_dar_employee_cloud_activity_log ca
join team_members tm on ca.username = tm.username
join sprint_dates sd on ca.ddate between sd.sprint_startdate::date and sd.sprint_enddate::date;
