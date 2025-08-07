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


class ModelProvidersBase(SQLModel):
    provider_name_str: str = Field(max_length=255, description="提供商名称")
    provider_type_str: str = Field(
        default="custom", max_length=40, description="提供商类型"
    )
    api_key_str: Optional[str] = Field(
        default=None, max_length=500, description="API密钥"
    )
    api_base_url_str: Optional[str] = Field(
        default=None, max_length=500, description="API基础URL"
    )
    extra_config_json: Optional[str] = Field(
        default=None, max_length=2000, description="额外配置"
    )
    comment_text: Optional[str] = Field(
        default=None, max_length=500, description="备注"
    )


class ModelProviders(
    ModelProvidersBase,
    DeclarativeBase,
    IDMixin,
    UserMixin,
    IsDeletedMixin,
    DateTimeMixin,
    table=True,
):
    __tablename__ = "model_providers"

    def __repr__(self):
        return (
            f"<Provider(id={self.id}, user_id={self.user_id}, provider_name="
            f"'{self.provider_name}', provider_type='{self.provider_type}')>"
        )


class ModelProvidersCreate(ModelProvidersBase):
    pass


class ModelProviderUpdate(SQLModel):
    api_key: Optional[str] = Field(default=None)
    api_base_url: Optional[str] = Field(default=None)
    extra_config: Optional[str] = Field(default=None)


class ModelProviderOut(BaseResponse):
    result: ModelProviders


class ModelProvidersOut(BaseResponse):
    result: List[ModelProviders]
