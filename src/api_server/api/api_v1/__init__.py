from fastapi import APIRouter

from src.api_server.api.api_v1 import debug, models, providers
from src.api_server.config import settings

api_router = APIRouter()

api_router.include_router(models.router, prefix="/dl_models", tags=["dl_models"])
api_router.include_router(
    providers.router, prefix="/model_providers", tags=["model_providers"]
)

# 仅在非生产环境下包含调试路由
if not settings.is_production:
    api_router.include_router(
        debug.router, prefix="/debug", tags=["debug"]
    )
