WITH burndown AS (SELECT project_key,board_id,sprint_id,issue_date,issue_key,
                         (SUM(CASE WHEN added=true THEN 1 ELSE 0 END) OVER (PARTITION BY (project_key,sprint_id,issue_key) ORDER BY issue_date) - (CASE WHEN added=true THEN 1 ELSE 0 END)) AS grouppart,
                         added, old_storypoints,new_storypoints,not_completed,completed,status, sprint_startdate,sprint_enddate,sprint_completedate
                  FROM stage_performance.t_jira_burndown),
     eventdetails AS (SELECT MAX(issue_date) AS issue_date,project_key,board_id,sprint_id,issue_key,grouppart,
                             bool_and(added) AS added,
                             MAX(old_storypoints) AS old_storypoints,
                             MAX(new_storypoints) AS new_storypoints,
                             bool_and(not_completed) AS not_completed,
                             bool_and(completed) AS completed,
                             MAX(status) AS status
                      FROM burndown
                      WHERE grouppart = 0
                      GROUP BY project_key,board_id,sprint_id,issue_key,grouppart
                      UNION ALL
                      SELECT issue_date,project_key,board_id,sprint_id,issue_key,grouppart,
                             added,old_storypoints,new_storypoints,not_completed,completed,status
                      FROM burndown
                      WHERE grouppart !=0
                      ORDER BY issue_date, issue_key),
     projectsprintdates AS (SELECT DISTINCT ON (project_key,board_id,sprint_id) project_key,board_id,sprint_id,sprint_startdate,sprint_enddate,sprint_completedate
                            FROM stage_performance.t_jira_burndown),
     eva AS (SELECT eventdetails.project_key,eventdetails.board_id,eventdetails.sprint_id,issue_date,issue_key,
                   CASE
                       WHEN added=true AND issue_date::timestamp<projectsprintdates.sprint_startdate::timestamp THEN 'Sprint start'
                       WHEN added=true AND issue_date::timestamp>=projectsprintdates.sprint_startdate::timestamp THEN 'Issue added to sprint'
                       WHEN added=false THEN 'Issue removed from sprint'
                       WHEN completed=true THEN 'Issue completed'
                       WHEN added IS NULL AND old_storypoints IS NULL THEN 'Estimate of ' || new_storypoints::text || ' has been added'
                       WHEN added IS NULL AND old_storypoints IS NOT NULL THEN 'Estimate changed from ' || old_storypoints::text || ' to ' || new_storypoints::text
                   END AS event_detail,
                   grouppart,added,
                   old_storypoints,new_storypoints,not_completed,completed,status,sprint_startdate,sprint_enddate,sprint_completedate
            FROM eventdetails
            LEFT JOIN projectsprintdates
            ON eventdetails.project_key=projectsprintdates.project_key AND eventdetails.board_id=projectsprintdates.board_id AND eventdetails.sprint_id=projectsprintdates.sprint_id),
     new AS (SELECT *, row_number() OVER (PARTITION BY issue_key ORDER BY issue_date) AS row_number
             FROM eva WHERE event_detail NOT IN ('Issue completed','Issue removed from sprint') ORDER BY issue_key, row_number DESC),
     completed AS (SELECT eva.project_key,eva.board_id,eva.sprint_id,eva.issue_date,eva.issue_key,eva.event_detail,newest.difference,
                          eva.sprint_startdate,eva.sprint_enddate,eva.sprint_completedate
                   FROM eva
                   LEFT JOIN (SELECT DISTINCT ON (issue_key) *, (0-new_storypoints::bigint) AS difference FROM new) AS newest
                   ON eva.issue_key = newest.issue_key
                   WHERE eva.event_detail IN ('Issue completed','Issue removed from sprint')),
     merged AS (SELECT eva.project_key,eva.board_id,eva.sprint_id,eva.issue_date,eva.issue_key,eva.event_detail,
                       CASE
                           WHEN event_detail IN ('Issue added to sprint','Sprint start') THEN new_storypoints::bigint
                           WHEN event_detail NOT IN ('Issue added to sprint','Sprint start') AND old_storypoints IS NULL THEN new_storypoints::bigint
                           WHEN event_detail NOT IN ('Issue added to sprint','Sprint start') AND old_storypoints IS NOT NULL THEN (new_storypoints::bigint - old_storypoints::bigint)
                       END AS difference,
                       eva.sprint_startdate,eva.sprint_enddate,eva.sprint_completedate
                FROM eva
                WHERE eva.event_detail NOT IN ('Issue completed','Issue removed from sprint')
                UNION ALL
                SELECT * FROM completed
                ORDER BY issue_date)
SELECT project_key,board_id,sprint_id,
       CASE WHEN issue_date::timestamp<sprint_startdate::timestamp THEN sprint_startdate::timestamp ELSE issue_date::timestamp END AS issue_date,
       issue_key,event_detail,difference,
       (SUM(difference) over (order by issue_date))::bigint as remaining,
       sprint_startdate,sprint_enddate,sprint_completedate
FROM merged WHERE project_key = :projectkey AND board_id = :boardid AND sprint_id = :sprintid
