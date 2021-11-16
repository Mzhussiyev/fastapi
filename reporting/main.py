from fastapi import FastAPI

from reporting.routes import cloud_activity, jira, sprint, bpm, company_budgeting

app = FastAPI(
    title="DAR Reporting API",
    version="1.0.0",
    description="API for DMS reporting module",
    redoc_url=None,
    docs_url="/",
)

app.include_router(cloud_activity.router)
app.include_router(sprint.router)
app.include_router(jira.router)
app.include_router(bpm.router)
app.include_router(company_budgeting.router)
