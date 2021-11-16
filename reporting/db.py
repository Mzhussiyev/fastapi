from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from reporting.settings import AppConfig, get_config


async def get_db(app_config: AppConfig = Depends(get_config)) -> AsyncEngine:
    db_url = app_config.db_url
    engine = create_async_engine(db_url)
    return engine
