with velocity as (
	select 
		sprint_id, 
		board_id, 
		sum(case when sprint_content is not null then storypoints else 0 end)::bigint as commitment, 
		sum(case when sprint_content in ('completedIssues','issuesCompletedInAnotherSprint') then storypoints else 0 end)::bigint as completed 
	from stage_performance.t_jira_sprint_report 
	group by sprint_id, board_id 
)
select
	distinct on
	(jsd.sprint_id) jsd.sprint_id,
	jsd.sprint_name,
	substring(jsd.issue_key, 0, strpos(jsd.issue_key, '-')) as project_key,
	jmd.project_name,
	jsd.board_id,
	jsd.sprint_startdate::date,
	jsd.sprint_enddate::date,
	velocity.commitment,
	velocity.completed,
	count(distinct jsrdta.assignee) as employee
from
	stage_performance.t_jira_sprint_report jsd
left join velocity on
	velocity.sprint_id = jsd.sprint_id
	and velocity.board_id = jsd.board_id
left join stage_performance.jira_main_data jmd on
	jmd.issue_key = jsd.issue_key
left join stage_performance.t_jira_sprint_report jsrdta on
	jsrdta.sprint_id = jsd.sprint_id
	and jsrdta.board_id = jsd.board_id
where
	(jsd.sprint_startdate::date,
	jsd.sprint_enddate::date) overlaps (:since, :until)
	and jsd.sprint_state <> 'future'
group by
	jsd.sprint_id,
	jsd.sprint_name,
	jsd.issue_key,
	jmd.project_name,
	jsd.board_id,
	jsd.sprint_startdate,
	jsd.sprint_enddate,
	velocity.commitment,
	velocity.completed
