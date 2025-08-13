"""CRUD operations for AI Workflow Definition."""

from datetime import datetime
from typing import Optional

from sqlalchemy import ScalarResult, asc, desc
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api_server.crud.base import CRUDBase
from src.api_server.models.ai_workflow_def import (
    AIWorkflowDef,
    AIWorkflowDefCreate,
    AIWorkflowDefUpdate,
)


class CRUDAIWorkflowDef(
    CRUDBase[AIWorkflowDef, AIWorkflowDefCreate, AIWorkflowDefUpdate]
):
    """CRUD operations for AI Workflow Definition."""

    async def create_workflow_def(
        self, db: AsyncSession, obj_in: AIWorkflowDefCreate, user_id: str
    ) -> AIWorkflowDef:
        """Create a new AI workflow definition."""
        obj_in_data = obj_in.model_dump()
        obj_in_data["user_id_str"] = user_id
        new_workflow_def = AIWorkflowDef(**obj_in_data)

        db.add(new_workflow_def)
        await db.commit()
        await db.refresh(new_workflow_def)
        return new_workflow_def

    async def get_workflow_def(
        self,
        db: AsyncSession,
        user_id: str,
        is_deleted: bool = False,
        name: Optional[str] = None,
        is_active: Optional[bool] = None,
        tags: Optional[str] = None,
        version: Optional[str] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        updated_after: Optional[datetime] = None,
        updated_before: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "updated_at_time",
        order: str = "desc",
    ) -> ScalarResult[AIWorkflowDef]:
        """Get AI workflow definitions with filters, pagination and sorting."""
        query = select(self.model).where(
            self.model.user_id_str == user_id,
            self.model.is_deleted_flag == is_deleted,
        )

        where_clause = []

        # 业务字段过滤
        if name:
            where_clause.append(self.model.name_str.contains(name))
        if is_active is not None:
            where_clause.append(self.model.is_active_flag == is_active)
        if tags:
            where_clause.append(self.model.tags_str.contains(tags))
        if version:
            where_clause.append(self.model.version_str.contains(version))

        # 时间过滤
        if created_after:
            where_clause.append(self.model.created_at_time >= created_after)
        if created_before:
            where_clause.append(self.model.created_at_time <= created_before)
        if updated_after:
            where_clause.append(self.model.updated_at_time >= updated_after)
        if updated_before:
            where_clause.append(self.model.updated_at_time <= updated_before)

        if where_clause:
            query = query.where(and_(*where_clause))

        # 排序
        order_column = getattr(self.model, order_by, self.model.updated_at_time)
        if order == "asc":
            query = query.order_by(asc(order_column))
        else:
            query = query.order_by(desc(order_column))

        # 分页
        query = query.offset(offset).limit(limit)

        workflow_defs = await db.exec(query)
        return workflow_defs

    async def update_workflow_def(
        self,
        db: AsyncSession,
        workflow_def: AIWorkflowDef,
        obj_in: AIWorkflowDefUpdate,
    ) -> AIWorkflowDef:
        """Update an AI workflow definition."""
        for k, v in obj_in.model_dump(exclude_unset=True).items():
            if hasattr(workflow_def, k):
                setattr(workflow_def, k, v)

        db.add(workflow_def)
        await db.commit()
        await db.refresh(workflow_def)
        return workflow_def

    async def get_active_workflow_defs(
        self, db: AsyncSession, user_id: str
    ) -> ScalarResult[AIWorkflowDef]:
        """Get all active workflow definitions for a user."""
        query = (
            select(self.model)
            .where(
                self.model.user_id_str == user_id,
                self.model.is_deleted_flag == False,
                self.model.is_active_flag == True,
            )
            .order_by(desc(self.model.updated_at_time))
        )

        workflow_defs = await db.exec(query)
        return workflow_defs


ai_workflow_def = CRUDAIWorkflowDef(AIWorkflowDef)
