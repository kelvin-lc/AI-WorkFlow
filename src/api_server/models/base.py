import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Field

DeclarativeBase = declarative_base()


class IDMixin:
    id_str: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        max_length=36,
        description="Primary key UUID",
    )


class IsDeletedMixin:
    is_deleted_flag: bool = Field(default=False, description="是否删除")


class DateTimeMixin:
    created_at_time: datetime = Field(
        default_factory=datetime.utcnow, description="创建时间"
    )
    updated_at_time: datetime = Field(
        default_factory=datetime.utcnow, description="更新时间"
    )


class UserMixin:
    user_id_str: str = Field(
        default="dc_user_id", max_length=100, description="DC user id"
    )


class BaseResponse(BaseModel):
    code: int = 0
    message: str = "success"
