from sqlalchemy import ScalarResult
from sqlmodel import and_, desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api_server.crud.base import CRUDBase
from src.api_server.models.model_providers import (
    ModelProviders,
    ModelProvidersCreate,
    ModelProviderUpdate,
)


class CRUDProvider(CRUDBase[ModelProviders, ModelProvidersCreate, ModelProviderUpdate]):
    async def create_provider(
        self, db: AsyncSession, obj_in: ModelProvidersCreate, user_id: str
    ) -> None:
        obj_in_data = obj_in.model_dump()
        obj_in_data["user_id_str"] = user_id
        new_provider = ModelProviders(**obj_in_data)

        db.add(new_provider)

    async def get_provider(
        self,
        db: AsyncSession,
        user_id: str,
        is_deleted: bool = False,
        provider_name: str = None,
        provider_type: str = None,
    ) -> ScalarResult[ModelProviders]:
        query = (
            select(self.model)
            .where(
                self.model.user_id_str == user_id,
                self.model.is_deleted_flag == is_deleted,
            )
            .order_by(desc(self.model.updated_at_time))
        )
        where_clause = []
        if provider_name:
            where_clause.append(self.model.provider_name_str == provider_name)
        if provider_type:
            where_clause.append(self.model.provider_type_str == provider_type)
        if where_clause:
            query = query.where(and_(*where_clause))

        providers = await db.exec(query)

        return providers

    # TODO: Implement update in base class
    async def update_provider(
        self,
        db: AsyncSession,
        provider: ModelProviders,
        obj_in: ModelProviderUpdate,
    ) -> ModelProviders:
        for k, v in obj_in.model_dump().items():
            if k in provider:
                setattr(provider, k, v)
        db.add(provider)
        await db.commit()
        await db.refresh(provider)
        return provider


model_providers = CRUDProvider(ModelProviders)
