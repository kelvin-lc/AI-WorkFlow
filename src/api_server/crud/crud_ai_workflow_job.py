"""CRUD operations for AI Workflow Job."""

from datetime import datetime
from typing import Optional

from sqlalchemy import ScalarResult, asc, desc
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api_server.crud.base import CRUDBase
from src.api_server.models.ai_workflow_job import (
    AIWorkflowJob,
    AIWorkflowJobCreate,
    AIWorkflowJobUpdate,
    JobStatus,
)


class CRUDAIWorkflowJob(
    CRUDBase[AIWorkflowJob, AIWorkflowJobCreate, AIWorkflowJobUpdate]
):
    """CRUD operations for AI Workflow Job."""

    async def create_workflow_job(
        self, db: AsyncSession, obj_in: AIWorkflowJobCreate, user_id: str
    ) -> AIWorkflowJob:
        """Create a new AI workflow job."""
        obj_in_data = obj_in.model_dump()
        obj_in_data["user_id_str"] = user_id
        new_workflow_job = AIWorkflowJob(**obj_in_data)

        db.add(new_workflow_job)
        await db.commit()
        await db.refresh(new_workflow_job)
        return new_workflow_job

    async def get_workflow_job(
        self,
        db: AsyncSession,
        user_id: str,
        is_deleted: bool = False,
        ai_workflow_def_id: Optional[str] = None,
        status: Optional[str] = None,
        job_name: Optional[str] = None,
        created_after: Optional[datetime] = None,
        created_before: Optional[datetime] = None,
        updated_after: Optional[datetime] = None,
        updated_before: Optional[datetime] = None,
        started_after: Optional[datetime] = None,
        started_before: Optional[datetime] = None,
        completed_after: Optional[datetime] = None,
        completed_before: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "updated_at_time",
        order: str = "desc",
    ) -> ScalarResult[AIWorkflowJob]:
        """Get AI workflow jobs with filters, pagination and sorting."""
        query = select(self.model).where(
            self.model.user_id_str == user_id,
            self.model.is_deleted_flag == is_deleted,
        )

        where_clause = []

        # 业务字段过滤
        if ai_workflow_def_id:
            where_clause.append(self.model.ai_workflow_def_id == ai_workflow_def_id)
        if status:
            where_clause.append(self.model.status_str == status)
        if job_name:
            where_clause.append(self.model.job_name_str.contains(job_name))

        # 时间过滤
        if created_after:
            where_clause.append(self.model.created_at_time >= created_after)
        if created_before:
            where_clause.append(self.model.created_at_time <= created_before)
        if updated_after:
            where_clause.append(self.model.updated_at_time >= updated_after)
        if updated_before:
            where_clause.append(self.model.updated_at_time <= updated_before)
        if started_after:
            where_clause.append(self.model.started_at_time >= started_after)
        if started_before:
            where_clause.append(self.model.started_at_time <= started_before)
        if completed_after:
            where_clause.append(self.model.completed_at_time >= completed_after)
        if completed_before:
            where_clause.append(self.model.completed_at_time <= completed_before)

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

        workflow_jobs = await db.exec(query)
        return workflow_jobs

    async def update_workflow_job(
        self,
        db: AsyncSession,
        workflow_job: AIWorkflowJob,
        obj_in: AIWorkflowJobUpdate,
    ) -> AIWorkflowJob:
        """Update an AI workflow job."""
        for k, v in obj_in.model_dump(exclude_unset=True).items():
            if hasattr(workflow_job, k):
                setattr(workflow_job, k, v)

        db.add(workflow_job)
        await db.commit()
        await db.refresh(workflow_job)
        return workflow_job

    async def get_jobs_by_status(
        self, db: AsyncSession, user_id: str, status: JobStatus
    ) -> ScalarResult[AIWorkflowJob]:
        """Get workflow jobs by status."""
        query = (
            select(self.model)
            .where(
                self.model.user_id_str == user_id,
                self.model.is_deleted_flag == False,
                self.model.status_str == status,
            )
            .order_by(desc(self.model.updated_at_time))
        )

        workflow_jobs = await db.exec(query)
        return workflow_jobs

    async def get_jobs_by_workflow_def(
        self, db: AsyncSession, user_id: str, ai_workflow_def_id: str
    ) -> ScalarResult[AIWorkflowJob]:
        """Get all jobs for a specific workflow definition."""
        query = (
            select(self.model)
            .where(
                self.model.user_id_str == user_id,
                self.model.is_deleted_flag == False,
                self.model.ai_workflow_def_id == ai_workflow_def_id,
            )
            .order_by(desc(self.model.updated_at_time))
        )

        workflow_jobs = await db.exec(query)
        return workflow_jobs


ai_workflow_job = CRUDAIWorkflowJob(AIWorkflowJob)
