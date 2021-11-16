SELECT (SELECT count(time_off_days) AS days
FROM stage_performance.t_bamboohr_time_off_schedule_data
WHERE start_date >= (SELECT DISTINCT ON (sprint_startdate) sprint_startdate::date FROM stage_performance.t_jira_sprint_report WHERE project_key = :projectkey AND board_id = :boardid AND sprint_id = :sprintid)
AND end_date <= (SELECT DISTINCT ON (sprint_enddate) sprint_enddate::date FROM stage_performance.t_jira_sprint_report WHERE project_key = :projectkey AND board_id = :boardid AND sprint_id = :sprintid)
AND fullname IN (SELECT DISTINCT assignee FROM stage_performance.t_jira_sprint_report WHERE project_key = :projectkey AND board_id = :boardid AND sprint_id = :sprintid)
AND status = 'approved') AS time_off,
(SELECT count(DISTINCT assignee) FROM stage_performance.t_jira_sprint_report WHERE project_key = :projectkey AND board_id = :boardid AND sprint_id = :sprintid) AS total_team_member