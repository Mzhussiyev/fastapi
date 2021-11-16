with sprint_data as (
	select distinct on (sprint_id)
		sprint_id,
		board_id,
		sprint_name,
		project_key,
		sprint_startdate::date,
		sprint_enddate::date
	from stage_performance.t_jira_sprint_report
	where sprint_state = 'CLOSED' and project_key = :projectkey
),
sprint_report as (
	select
		project_key,
		sprint_id,
		board_id,
		count(distinct assignee) as team_members,
		count(case when sprint_content is not null then 1 end) as planned_tasks,
		count(case when sprint_content in ('completedIssues','issuesCompletedInAnotherSprint') and status = 'Done' then 1 end) as resolved_tasks,
	    sum(case when sprint_content is not null then storypoints else 0 end)::bigint as planned_storypoints,
	    sum(case when sprint_content in ('completedIssues','issuesCompletedInAnotherSprint') then storypoints else 0 end)::bigint as resolved_storypoints
	from stage_performance.t_jira_sprint_report
	where project_key = :projectkey
	group by project_key, sprint_id, board_id
)
select
	sd.sprint_id,
	sd.board_id,
	sd.sprint_name,
	sd.project_key,
	sd.sprint_startdate,
	sd.sprint_enddate,
	case
		when sr.team_members is not null then sr.team_members
		else 0
	end as team_members,
    (case
		when sr.planned_storypoints is not null and sr.planned_storypoints <> 0 and sr.resolved_storypoints is not null then round((sr.resolved_storypoints::numeric/sr.planned_storypoints),2)
		else 0
	end) as commitment,
    sr.resolved_storypoints as velocity,
    (case
		when sr.planned_storypoints is not null and sr.planned_storypoints <> 0 and sr.resolved_storypoints is not null and round((sr.resolved_storypoints::numeric/sr.planned_storypoints),2) >= 1 then 'Achieved'
		when sr.planned_storypoints is not null and sr.planned_storypoints <> 0 and sr.resolved_storypoints is not null and round((sr.resolved_storypoints::numeric/sr.planned_storypoints),2) < 1 then 'Not achieved'
		else '-'
    end) as status,
	sr.planned_tasks as tasks_plan,
	sr.resolved_tasks as tasks_fact
from sprint_data sd
left join sprint_report sr on
	sr.sprint_id = sd.sprint_id and sr.board_id = sd.board_id
order by sd.sprint_id desc;