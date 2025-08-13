"""AI Workflow Job models."""

from enum import Enum
from typing import List, Optional

from sqlmodel import Field, SQLModel

from src.api_server.models.base import (
    BaseResponse,
    DateTimeMixin,
    DeclarativeBase,
    IDMixin,
    IsDeletedMixin,
    UserMixin,
)


class JobStatus(str, Enum):
    """Job status enumeration."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AIWorkflowJobBase(SQLModel):
    """Base model for AI Workflow Job."""
    
    ai_workflow_def_id: str = Field(max_length=36, description="工作流定义ID")
    job_name_str: str = Field(max_length=255, description="任务名称")
    trigger_data_json: str = Field(description="触发数据，JSON格式")
    status_str: str = Field(default=JobStatus.PENDING, max_length=50, description="任务状态")
    result_data_json: Optional[str] = Field(default=None, description="结果数据，JSON格式")
    error_message_text: Optional[str] = Field(default=None, max_length=2000, description="错误信息")
    started_at_time: Optional[str] = Field(default=None, description="开始时间")
    completed_at_time: Optional[str] = Field(default=None, description="完成时间")
    execution_time_seconds: Optional[float] = Field(default=None, description="执行时间（秒）")

    class Config:
        protected_namespaces = []


class AIWorkflowJob(
    AIWorkflowJobBase,
    DeclarativeBase,
    UserMixin,
    IDMixin,
    IsDeletedMixin,
    DateTimeMixin,
    table=True,
):
    """AI Workflow Job table model."""
    
    __tablename__ = "ai_workflow_job"


class AIWorkflowJobCreate(AIWorkflowJobBase):
    """Create AI Workflow Job schema."""
    pass


class AIWorkflowJobUpdate(SQLModel):
    """Update AI Workflow Job schema."""
    
    job_name_str: Optional[str] = Field(default=None, max_length=255, description="任务名称")
    trigger_data_json: Optional[str] = Field(default=None, description="触发数据，JSON格式")
    status_str: Optional[str] = Field(default=None, max_length=50, description="任务状态")
    result_data_json: Optional[str] = Field(default=None, description="结果数据，JSON格式")
    error_message_text: Optional[str] = Field(default=None, max_length=2000, description="错误信息")
    started_at_time: Optional[str] = Field(default=None, description="开始时间")
    completed_at_time: Optional[str] = Field(default=None, description="完成时间")
    execution_time_seconds: Optional[float] = Field(default=None, description="执行时间（秒）")


class AIWorkflowJobOut(BaseResponse):
    """Single AI Workflow Job response."""
    
    result: AIWorkflowJob


class AIWorkflowJobsOut(BaseResponse):
    """Multiple AI Workflow Jobs response."""
    
    result: List[AIWorkflowJob]
