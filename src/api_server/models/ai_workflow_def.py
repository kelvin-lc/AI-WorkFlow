"""AI Workflow Definition models."""

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


class AIWorkflowDefBase(SQLModel):
    """Base model for AI Workflow Definition."""
    
    name_str: str = Field(max_length=255, description="工作流名称")
    description_text: Optional[str] = Field(default=None, max_length=1000, description="工作流描述")
    hs_yaml_content: str = Field(description="Haystack YAML配置内容")
    version_str: str = Field(default="1.0.0", max_length=50, description="工作流版本")
    is_active_flag: bool = Field(default=True, description="是否激活")
    tags_str: Optional[str] = Field(default=None, max_length=500, description="标签，逗号分隔")

    class Config:
        protected_namespaces = []


class AIWorkflowDef(
    AIWorkflowDefBase,
    DeclarativeBase,
    UserMixin,
    IDMixin,
    IsDeletedMixin,
    DateTimeMixin,
    table=True,
):
    """AI Workflow Definition table model."""
    
    __tablename__ = "ai_workflow_def"


class AIWorkflowDefCreate(AIWorkflowDefBase):
    """Create AI Workflow Definition schema."""
    pass


class AIWorkflowDefUpdate(SQLModel):
    """Update AI Workflow Definition schema."""
    
    name_str: Optional[str] = Field(default=None, max_length=255, description="工作流名称")
    description_text: Optional[str] = Field(default=None, max_length=1000, description="工作流描述")
    hs_yaml_content: Optional[str] = Field(default=None, description="Haystack YAML配置内容")
    version_str: Optional[str] = Field(default=None, max_length=50, description="工作流版本")
    is_active_flag: Optional[bool] = Field(default=None, description="是否激活")
    tags_str: Optional[str] = Field(default=None, max_length=500, description="标签，逗号分隔")


class AIWorkflowDefOut(BaseResponse):
    """Single AI Workflow Definition response."""
    
    result: AIWorkflowDef


class AIWorkflowDefsOut(BaseResponse):
    """Multiple AI Workflow Definitions response."""
    
    result: List[AIWorkflowDef]
