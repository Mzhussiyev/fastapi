with sprint_data as (
	select distinct on (sprint_id)
		sprint_id,
		board_id,
		sprint_name,
		project_key,
		sprint_state,
	    sprint_goal
	from stage_performance.t_jira_sprint_report
	where sprint_state = 'CLOSED' and project_key = :projectkey and board_id = :boardid
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
	where project_key = :projectkey and board_id = :boardid
	group by project_key, sprint_id, board_id
)
select
	sd.project_key,
    sd.board_id,
    sd.sprint_id,
	sd.sprint_name,
	sd.sprint_state,
    sr.planned_storypoints as commitment,
    sr.resolved_storypoints as completed,
    sd.sprint_goal
from sprint_data sd
left join sprint_report sr on
	sr.sprint_id = sd.sprint_id and sr.board_id = sd.board_id
order by sd.sprint_id desc
limit 3;