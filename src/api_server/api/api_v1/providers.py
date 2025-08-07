from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from src.api_server import crud
from src.api_server.api import deps
from src.api_server.api.errors import ModelProviderNotFound
from src.api_server.models import model_providers

router = APIRouter()


@router.post(
    "",
    response_model=model_providers.ModelProviderOut,
)
async def create_model_providers(
    provide: model_providers.ModelProvidersCreate,
    db: Session = Depends(deps.get_session),
) -> Any:
    """
    Create a new provider
    """
    await crud.model_providers.create_provider(db, obj_in=provide, user_id="user_id")
    return {"result": provide}


@router.get(
    "",
    response_model=model_providers.ModelProvidersOut,
)
async def get_model_providers(
    db: Session = Depends(deps.get_session),
    provider_name: str = Query(None),
) -> Any:
    """
    Get all providers
    """
    providers = await crud.model_providers.get_provider(
        db, user_id="user_id", provider_name=provider_name
    )
    return {"result": providers}


@router.patch(
    "/{provider_id}",
    response_model=model_providers.ModelProviderOut,
)
async def update_model_providers(
    provider_id: str,
    provider_update: model_providers.ModelProviderUpdate,
    db: Session = Depends(deps.get_session),
) -> Any:
    """
    Update a provider
    """

    one_provider = await crud.model_providers.get(db, id=provider_id)
    if not one_provider:
        raise ModelProviderNotFound()

    provider = await crud.model_providers.update_provider(
        db, provider=one_provider, obj_in=provider_update
    )
    return {"result": provider}
