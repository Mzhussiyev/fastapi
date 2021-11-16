WITH groupped AS (SELECT project_key,board_id,sprint_id,
                         SUM(CASE WHEN sprint_content IS NOT NULL THEN storypoints ELSE 0 END)::bigint AS planned_storypoints,
                         SUM(CASE WHEN sprint_content IN ('completedIssues','issuesCompletedInAnotherSprint') THEN storypoints ELSE 0 END)::bigint AS resolved_storypoints,
                         SUM(CASE WHEN sprint_content IN ('issuesNotCompletedInCurrentSprint') THEN storypoints ELSE 0 END)::bigint AS unresolved_storypoints,
                         SUM(CASE WHEN sprint_content IN ('puntedIssues') THEN storypoints ELSE 0 END)::bigint AS removed_storypoints,
                         round((SUM(CASE WHEN sprint_content IN ('completedIssues','issuesCompletedInAnotherSprint') THEN storypoints ELSE 0 END)::double precision/ NULLIF(SUM(CASE WHEN sprint_content IN ('completedIssues','issuesCompletedInAnotherSprint','issuesNotCompletedInCurrentSprint') THEN storypoints END),0))*100)::bigint AS percentage
                  FROM stage_performance.t_jira_sprint_report
                  GROUP BY project_key,board_id,sprint_id)
SELECT *
FROM groupped
WHERE project_key= :projectkey AND board_id = :boardid AND sprint_id = :sprintid