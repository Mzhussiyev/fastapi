SELECT DISTINCT project_key,board_id,sprint_id,sprint_name
FROM stage_performance.t_jira_sprint_report
WHERE project_key = :projectkey AND board_id = :boardid
