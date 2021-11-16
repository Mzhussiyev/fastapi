SELECT DISTINCT project_key, board_id
FROM stage_performance.t_jira_sprint_report
WHERE project_key = :projectkey
