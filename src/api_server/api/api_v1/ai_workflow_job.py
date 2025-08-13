"""AI Workflow Job API endpoints."""

from datetime import datetime
from typing import Any, Literal, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api_server import crud
from src.api_server.api import deps
from src.api_server.api.errors import NotFoundError
from src.api_server.models import ai_workflow_job
from src.api_server.models.ai_workflow_job import JobStatus

router = APIRouter()


@router.post(
    "",
    response_model=ai_workflow_job.AIWorkflowJobOut,
)
async def create_ai_workflow_job(
    workflow_job: ai_workflow_job.AIWorkflowJobCreate,
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    创建新的AI工作流任务
    """
    # 验证工作流定义是否存在
    workflow_def = await crud.ai_workflow_def.get(
        db, id=workflow_job.ai_workflow_def_id
    )
    if not workflow_def:
        raise NotFoundError(message="AI Workflow Definition not found")

    # TODO: 从token获取user_id
    new_workflow_job = await crud.ai_workflow_job.create_workflow_job(
        db,
        obj_in=workflow_job,
        user_id="user_id",
    )
    return {"result": new_workflow_job}


@router.get(
    "",
    response_model=ai_workflow_job.AIWorkflowJobsOut,
)
async def get_ai_workflow_jobs(
    db: AsyncSession = Depends(deps.get_session),
    # 业务过滤参数
    ai_workflow_def_id: Optional[str] = Query(None, description="工作流定义ID过滤"),
    status: Optional[str] = Query(None, description="任务状态过滤"),
    job_name: Optional[str] = Query(None, description="任务名称过滤"),
    # 时间过滤参数
    created_after: Optional[datetime] = Query(None, description="创建时间起始过滤"),
    created_before: Optional[datetime] = Query(None, description="创建时间结束过滤"),
    updated_after: Optional[datetime] = Query(None, description="更新时间起始过滤"),
    updated_before: Optional[datetime] = Query(None, description="更新时间结束过滤"),
    started_after: Optional[datetime] = Query(None, description="开始时间起始过滤"),
    started_before: Optional[datetime] = Query(None, description="开始时间结束过滤"),
    completed_after: Optional[datetime] = Query(None, description="完成时间起始过滤"),
    completed_before: Optional[datetime] = Query(None, description="完成时间结束过滤"),
    # 分页和排序参数
    limit: int = Query(100, ge=1, le=1000, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    order_by: Literal[
        "created_at_time",
        "updated_at_time",
        "started_at_time",
        "completed_at_time",
        "execution_time_seconds",
    ] = Query("updated_at_time", description="排序字段"),
    order: Literal["asc", "desc"] = Query("desc", description="排序方向"),
) -> Any:
    """
    获取所有AI工作流任务
    支持多种过滤、分页和排序参数
    """
    workflow_jobs = await crud.ai_workflow_job.get_workflow_job(
        db,
        user_id="user_id",
        ai_workflow_def_id=ai_workflow_def_id,
        status=status,
        job_name=job_name,
        created_after=created_after,
        created_before=created_before,
        updated_after=updated_after,
        updated_before=updated_before,
        started_after=started_after,
        started_before=started_before,
        completed_after=completed_after,
        completed_before=completed_before,
        limit=limit,
        offset=offset,
        order_by=order_by,
        order=order,
    )
    return {"result": list(workflow_jobs)}


@router.get(
    "/{workflow_job_id}",
    response_model=ai_workflow_job.AIWorkflowJobOut,
)
async def get_ai_workflow_job(
    workflow_job_id: str,
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    根据ID获取AI工作流任务
    """
    workflow_job = await crud.ai_workflow_job.get(db, id=workflow_job_id)
    if not workflow_job:
        raise NotFoundError(message="AI Workflow Job not found")
    return {"result": workflow_job}


# @router.delete(
#     "/{workflow_job_id}",
# )
async def delete_ai_workflow_job(
    workflow_job_id: str,
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    删除AI工作流任务（软删除）
    """
    workflow_job = await crud.ai_workflow_job.get(db, id=workflow_job_id)
    if not workflow_job:
        raise NotFoundError(message="AI Workflow Job not found")

    await crud.ai_workflow_job.remove(db, id=workflow_job_id)
    return {"message": "AI Workflow Job deleted successfully"}


# @router.get(
#     "/status/{status}",
#     response_model=ai_workflow_job.AIWorkflowJobsOut,
# )
async def get_ai_workflow_jobs_by_status(
    status: JobStatus,
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    根据状态获取AI工作流任务
    """
    workflow_jobs = await crud.ai_workflow_job.get_jobs_by_status(
        db, user_id="user_id", status=status
    )
    return {"result": list(workflow_jobs)}


# @router.get(
#     "/workflow/{workflow_def_id}/jobs",
#     response_model=ai_workflow_job.AIWorkflowJobsOut,
# )
async def get_ai_workflow_jobs_by_def(
    workflow_def_id: str,
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    获取特定工作流定义的所有任务
    """
    # 验证工作流定义是否存在
    workflow_def = await crud.ai_workflow_def.get(db, id=workflow_def_id)
    if not workflow_def:
        raise NotFoundError(message="AI Workflow Definition not found")

    workflow_jobs = await crud.ai_workflow_job.get_jobs_by_workflow_def(
        db, user_id="user_id", ai_workflow_def_id=workflow_def_id
    )
    return {"result": list(workflow_jobs)}
