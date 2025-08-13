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
        result = await db.exec(select(self.model).where(self.model.id_str == id))
        return result.first()

    async def get_by_user_id(
        self, db: AsyncSession, user_id: str
    ) -> List[ModelType]:
        result = await db.exec(
            select(self.model).where(self.model.user_id_str == user_id)
        )
        return result.all()

    async def remove(self, db: AsyncSession, id: str) -> ModelType | None:
        """Soft delete by setting is_deleted_flag to True."""
        obj = await self.get(db, id=id)
        if obj:
            obj.is_deleted_flag = True
            db.add(obj)
            await db.commit()
            await db.refresh(obj)
        return obj

    async def delete(self, db: AsyncSession, id: str) -> None:
        """Hard delete (for backward compatibility)."""
        obj = await self.get(db, id=id)
        if obj:
            await db.delete(obj)
            await db.commit()
