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


class DLModelsBase(SQLModel):
    model_name_str: str = Field(max_length=255, description="模型名称")
    model_type_str: str = Field(max_length=40, description="模型类型")
    config_json: Optional[str] = Field(
        default=None, max_length=1000, description="模型配置"
    )
    model_provider_id: str = Field(max_length=36, description="模型提供商ID")

    comment_text: Optional[str] = Field(
        default=None, max_length=500, description="备注"
    )

    class Config:
        protected_namespaces = []


class DLModels(
    DLModelsBase,
    DeclarativeBase,
    UserMixin,
    IDMixin,
    IsDeletedMixin,
    DateTimeMixin,
    table=True,
):
    __tablename__ = "dl_models"
    # for easy search - provider_name for filtering
    provider_name_str: str = Field(max_length=255, description="提供商名称")


class DLModelCreate(DLModelsBase):
    pass


class DLModelUpdate(DLModelsBase):
    pass


class DLModelOut(BaseResponse):
    result: DLModels


class DLModelsOut(BaseResponse):
    result: List[DLModels]
