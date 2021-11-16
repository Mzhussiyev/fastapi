WITH groupped AS (SELECT project_key,board_id,sprint_id,
                         COUNT(CASE WHEN sprint_content IS NOT NULL THEN 1 END) AS planned_tasks,
                         COUNT(CASE WHEN sprint_content IN ('completedIssues','issuesCompletedInAnotherSprint') AND status = 'Done' THEN 1 END) AS resolved_tasks,
                         COUNT(CASE WHEN sprint_content = 'issuesNotCompletedInCurrentSprint' THEN 1 END) AS unresolved_tasks,
                         COUNT(CASE WHEN sprint_content IN ('completedIssues','issuesCompletedInAnotherSprint') AND status = 'Cancelled' THEN 1 END) AS cancelled_tasks,
                         COUNT(CASE WHEN sprint_content = 'puntedIssues' THEN 1 END) AS removed_tasks,
                         round((COUNT(CASE WHEN sprint_content IN ('completedIssues','issuesCompletedInAnotherSprint') THEN 1 END)::double precision/NULLIF(COUNT(CASE WHEN sprint_content IN ('completedIssues','issuesCompletedInAnotherSprint','issuesNotCompletedInCurrentSprint') THEN 1 END),0))*100)::bigint AS percentage,
                         (CASE WHEN sprint_completedate IS NOT NULL AND (now() + interval '6 hour')::timestamp >= sprint_completedate::timestamp THEN 0::bigint
                               WHEN sprint_completedate IS NULL AND (now() + interval '6 hour')::timestamp >= sprint_enddate::timestamp THEN 0::bigint
                               WHEN sprint_completedate IS NULL AND (now() + interval '6 hour')::timestamp < sprint_enddate::timestamp THEN  ABS(EXTRACT(DAY FROM ((now() + interval '6 hour')::timestamp - sprint_enddate::timestamp))::bigint)
                          END) AS days_remaining
                  FROM stage_performance.t_jira_sprint_report
                  GROUP BY project_key, board_id, sprint_id,sprint_completedate,sprint_enddate)
SELECT *
FROM groupped
WHERE project_key= :projectkey AND board_id = :boardid AND sprint_id = :sprintid