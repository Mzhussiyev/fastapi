WITH allbugs AS (SELECT project_key,board_id,sprint_id,
                        COUNT(CASE WHEN sprint_content IS NOT NULL THEN 1 END) AS bugs,
                        COUNT(CASE WHEN sprint_content IN ('completedIssues','issuesCompletedInAnotherSprint') AND status = 'Done' THEN 1 END) AS resolved_bugs,
                        COUNT(CASE WHEN sprint_content = 'issuesNotCompletedInCurrentSprint' THEN 1 END) AS unresolved_bugs,
                        COUNT(CASE WHEN sprint_content IN ('completedIssues','issuesCompletedInAnotherSprint') AND status = 'Cancelled' THEN 1 END) AS cancelled_bugs,
                        COUNT(CASE WHEN sprint_content = 'puntedIssues' THEN 1 END) AS removed_bugs
                FROM stage_performance.t_jira_sprint_report
                GROUP BY project_key,board_id,sprint_id,issue_type
                HAVING issue_type = 'Bug'),
     sprint AS (SELECT project_key,board_id,sprint_id
                FROM stage_performance.t_jira_sprint_report
                GROUP BY project_key,board_id,sprint_id)
SELECT sprint.project_key,sprint.board_id,sprint.sprint_id,bugs,resolved_bugs,unresolved_bugs,cancelled_bugs,removed_bugs
FROM sprint
LEFT JOIN allbugs
ON sprint.project_key = allbugs.project_key AND sprint.board_id = allbugs.board_id AND sprint.sprint_id = allbugs.sprint_id
WHERE sprint.project_key = :projectkey AND sprint.board_id = :boardid AND sprint.sprint_id = :sprintid