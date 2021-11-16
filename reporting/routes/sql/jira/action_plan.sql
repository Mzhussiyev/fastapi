SELECT DISTINCT jira_all.project_key,jira_all.issue_key, issue_name, created::date AS created_date
FROM (SELECT issue_key, MAX(updated) AS lastdate
        FROM stage_performance.jira_new_data
        GROUP BY issue_key) AS latest_issues
INNER JOIN stage_performance.jira_new_data AS jira_all
ON jira_all.issue_key = latest_issues.issue_key AND jira_all.updated = latest_issues.lastdate
WHERE project_key = :projectkey AND issue_type ='Epic' AND created::date>='2021-03-21'
