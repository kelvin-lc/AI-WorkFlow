from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.api_server import crud
from src.api_server.api import deps
from src.api_server.api.errors import ModelProviderNotFound
from src.api_server.models import dl_models

router = APIRouter()


@router.post(
    "",
    response_model=dl_models.BaseResponse,
)
async def create_dl_models(
    model: dl_models.DLModelCreate,
    db: Session = Depends(deps.get_session),
) -> Any:
    """
    Create a new dl model
    """
    # TODO: get user_id from token
    provider = await crud.model_providers.get(db, id=model.model_provider_id)
    if not provider:
        raise ModelProviderNotFound()

    new_model = await crud.dl_model.create_model(
        db,
        obj_in=model,
        user_id="user_id",
        provider_name=provider.provider_name_str,
    )
    return {"result": new_model}


@router.get(
    "",
    response_model=dl_models.DLModelsOut,
)
async def get_dl_models(
    db: Session = Depends(deps.get_session),
    model_name: str = Query(None),
    model_type: str = Query(None),
    provider_name: str = Query(None),
) -> Any:
    """
    Get all dl models
    """
    models = await crud.dl_model.get_model(
        db,
        user_id="user_id",
        model_name=model_name,
        model_type=model_type,
        provider_name=provider_name,
    )
    return {"result": models}
