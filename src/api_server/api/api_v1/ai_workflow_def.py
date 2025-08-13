"""AI Workflow Definition API endpoints."""

from datetime import datetime
from typing import Any, Literal, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api_server import crud
from src.api_server.api import deps
from src.api_server.api.errors import NotFoundError
from src.api_server.models import ai_workflow_def

router = APIRouter()


@router.post(
    "",
    response_model=ai_workflow_def.AIWorkflowDefOut,
)
async def create_ai_workflow_def(
    workflow_def: ai_workflow_def.AIWorkflowDefCreate,
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    创建新的AI工作流定义
    """
    # TODO: 从token获取user_id
    new_workflow_def = await crud.ai_workflow_def.create_workflow_def(
        db,
        obj_in=workflow_def,
        user_id="user_id",
    )
    return {"result": new_workflow_def}


# @router.get(
#     "",
#     response_model=ai_workflow_def.AIWorkflowDefsOut,
# )
async def get_ai_workflow_defs(
    db: AsyncSession = Depends(deps.get_session),
    # 业务过滤参数
    name: Optional[str] = Query(None, description="工作流名称过滤"),
    is_active: Optional[bool] = Query(None, description="是否激活过滤"),
    tags: Optional[str] = Query(None, description="标签过滤"),
    version: Optional[str] = Query(None, description="版本过滤"),
    # 时间过滤参数
    created_after: Optional[datetime] = Query(None, description="创建时间起始过滤"),
    created_before: Optional[datetime] = Query(None, description="创建时间结束过滤"),
    updated_after: Optional[datetime] = Query(None, description="更新时间起始过滤"),
    updated_before: Optional[datetime] = Query(None, description="更新时间结束过滤"),
    # 分页和排序参数
    limit: int = Query(100, ge=1, le=1000, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="偏移量"),
    order_by: Literal[
        "created_at_time", "updated_at_time", "name_str", "version_str"
    ] = Query("updated_at_time", description="排序字段"),
    order: Literal["asc", "desc"] = Query("desc", description="排序方向"),
) -> Any:
    """
    获取所有AI工作流定义
    支持多种过滤、分页和排序参数
    """
    workflow_defs = await crud.ai_workflow_def.get_workflow_def(
        db,
        user_id="user_id",
        name=name,
        is_active=is_active,
        tags=tags,
        version=version,
        created_after=created_after,
        created_before=created_before,
        updated_after=updated_after,
        updated_before=updated_before,
        limit=limit,
        offset=offset,
        order_by=order_by,
        order=order,
    )
    return {"result": list(workflow_defs)}


@router.get(
    "/{workflow_def_id}",
    response_model=ai_workflow_def.AIWorkflowDefOut,
)
async def get_ai_workflow_def(
    workflow_def_id: str,
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    根据ID获取AI工作流定义
    """
    workflow_def = await crud.ai_workflow_def.get(db, id=workflow_def_id)
    if not workflow_def:
        raise NotFoundError(message="AI Workflow Definition not found")
    return {"result": workflow_def}


# @router.delete(
#     "/{workflow_def_id}",
# )
async def delete_ai_workflow_def(
    workflow_def_id: str,
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    删除AI工作流定义（软删除）
    """
    workflow_def = await crud.ai_workflow_def.get(db, id=workflow_def_id)
    if not workflow_def:
        raise NotFoundError(message="AI Workflow Definition not found")

    await crud.ai_workflow_def.remove(db, id=workflow_def_id)
    return {"message": "AI Workflow Definition deleted successfully"}


@router.get(
    "/list",
    response_model=ai_workflow_def.AIWorkflowDefsOut,
)
async def get_active_ai_workflow_defs(
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    获取所有激活的AI工作流定义
    """
    workflow_defs = await crud.ai_workflow_def.get_active_workflow_defs(
        db, user_id="user_id"
    )
    return {"result": list(workflow_defs)}
