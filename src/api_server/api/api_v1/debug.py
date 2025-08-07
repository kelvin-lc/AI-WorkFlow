"""Debug endpoints for internal testing."""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.api_server.api import deps
from src.api_server.api.deps import create_tables, drop_tables
from src.api_server.api.errors import APIError
from src.api_server.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/create-tables", tags=["debug"])
async def create_all_tables() -> Any:
    """
    创建所有数据库表 - 仅用于开发调试
    """
    if settings.is_production:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is not available in production",
        )

    try:
        # 直接调用deps中的create_tables函数
        await create_tables()

        # 获取表名列表用于返回信息
        table_names = [
            table.name
            for table in SQLModel.metadata.tables.values()
            if table.name not in deps.skipped_tables
        ]

        logger.info(f"Successfully created tables: {table_names}")

        return {
            "message": "All tables created successfully",
            "tables": table_names,
            "count": len(table_names),
        }

    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise APIError(
            message=f"Failed to create tables: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.delete("/drop-tables", tags=["debug"])
async def drop_all_tables() -> Any:
    """
    删除所有数据库表 - 仅用于开发调试
    ⚠️ 警告：此操作将删除所有数据，不可恢复！
    """
    if settings.is_production:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is not available in production",
        )

    try:
        # 获取表名列表（在删除之前）
        table_names = [
            table.name
            for table in SQLModel.metadata.tables.values()
            if table.name not in deps.skipped_tables
        ]

        # 直接调用deps中的drop_tables函数
        await drop_tables()

        logger.warning(f"Successfully dropped tables: {table_names}")

        return {
            "message": "All tables dropped successfully",
            "tables": table_names,
            "count": len(table_names),
            "warning": "All data has been permanently deleted!",
        }

    except Exception as e:
        logger.error(f"Failed to drop tables: {e}")
        raise APIError(
            message=f"Failed to drop tables: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/table-info", tags=["debug"])
async def get_table_info(
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    获取数据库表信息 - 仅用于开发调试
    """
    if settings.is_production:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This endpoint is not available in production",
        )

    try:
        tables_info = []

        for table_name, table in SQLModel.metadata.tables.items():
            columns = []
            for column in table.columns:
                columns.append(
                    {
                        "name": column.name,
                        "type": str(column.type),
                        "nullable": column.nullable,
                        "primary_key": column.primary_key,
                        "default": str(column.default) if column.default else None,
                    }
                )

            tables_info.append(
                {
                    "table_name": table_name,
                    "columns": columns,
                    "column_count": len(columns),
                }
            )

        return {
            "message": "Table information retrieved successfully",
            "tables": tables_info,
            "table_count": len(tables_info),
        }

    except Exception as e:
        logger.error(f"Failed to get table info: {e}")
        raise APIError(
            message=f"Failed to get table info: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/health-check", tags=["debug"])
async def debug_health_check(
    db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    调试健康检查 - 测试数据库连接
    """
    try:
        # 简单的数据库连接测试
        from sqlalchemy import text

        async with db as session:
            result = await session.execute(text("SELECT 1 as test"))
            row = result.fetchone()

        return {
            "message": "Database connection successful",
            "database_test": row[0] if row else None,
            "environment": settings.ENVIRONMENT,
            "debug_mode": settings.DEBUG,
        }

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise APIError(
            message=f"Health check failed: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
