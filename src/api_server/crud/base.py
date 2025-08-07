from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: str) -> ModelType | None:
        model = await db.exec(select(self.model).where(self.model.id == id))
        return model.first()

    async def get_by_user_id(
        self, db: AsyncSession, user_id: int
    ) -> List[ModelType]:
        result = await db.exec(
            select(self.model).where(self.model.user_id == user_id)
        )
        return result.all()

    async def delete(self, db: AsyncSession, pk: int) -> None:
        # soft delete
        pass
