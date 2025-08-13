from fastapi import APIRouter

from src.api_server.api.api_v1 import (
    ai_workflow_def,
    ai_workflow_job,
    debug,
)
from src.api_server.config import settings

api_router = APIRouter()

api_router.include_router(
    ai_workflow_def.router, prefix="/ai_workflow_def", tags=["ai_workflow_def"]
)
api_router.include_router(
    ai_workflow_job.router, prefix="/ai_workflow_job", tags=["ai_workflow_job"]
)

# 仅在非生产环境下包含调试路由
if not settings.is_production:
    api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
