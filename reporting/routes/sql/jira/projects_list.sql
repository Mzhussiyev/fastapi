WITH projectslist AS (SELECT DISTINCT jira_all.project_key,jira_all.project_name
                        FROM (SELECT project_key, MAX(updated) AS lastdate
                                FROM stage_performance.jira_new_data
                                GROUP BY project_key) AS latest_issues
                        INNER JOIN stage_performance.jira_new_data AS jira_all
                        ON jira_all.project_key = latest_issues.project_key AND jira_all.updated = latest_issues.lastdate
                        WHERE created::date>='2021-03-21'),
     projects AS (SELECT DISTINCT project_key
                  FROM stage_performance.t_jira_sprint_report jsrd)
SELECT projects.project_key,projectslist.project_name
FROM projects
LEFT JOIN projectslist
ON projects.project_key = projectslist.project_key
WHERE projectslist.project_name IS NOT NULL