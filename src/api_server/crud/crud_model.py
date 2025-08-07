from sqlmodel import and_, desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api_server.crud.base import CRUDBase
from src.api_server.models.dl_models import DLModelCreate, DLModels, DLModelUpdate


class CRUDModel(CRUDBase[DLModels, DLModelCreate, DLModelUpdate]):
    async def create_model(
        self,
        db: AsyncSession,
        obj_in: DLModelCreate,
        user_id: str,
        provider_name: str,
    ) -> None:
        obj_in_data = obj_in.model_dump()
        obj_in_data["user_id_str"] = user_id
        obj_in_data["provider_name_str"] = provider_name
        new_model = DLModels(**obj_in_data)

        db.add(new_model)

    async def get_model(
        self,
        db: AsyncSession,
        user_id: str,
        is_deleted: bool = False,
        model_name: str = None,
        model_type: str = None,
        provider_name: str = None,
    ) -> DLModels:
        query = (
            select(self.model)
            .where(
                self.model.user_id_str == user_id,
                self.model.is_deleted_flag == is_deleted,
            )
            .order_by(desc(self.model.updated_at_time))
        )
        where_clause = []
        if model_name:
            where_clause.append(self.model.model_name_str == model_name)
        if model_type:
            where_clause.append(self.model.model_type_str == model_type)
        if provider_name:
            where_clause.append(self.model.provider_name_str == provider_name)
        if where_clause:
            query = query.where(and_(*where_clause))

        models = await db.exec(query)

        return models


dl_model = CRUDModel(DLModels)
