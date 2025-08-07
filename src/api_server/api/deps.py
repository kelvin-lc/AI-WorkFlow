from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.api_server.config import settings

engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URI,
    echo=settings.ECHO_SQL,
    future=True,
    pool_size=200,
    max_overflow=100,
    pool_timeout=65,
    pool_recycle=3600 * 4,
)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@asynccontextmanager
async def session_maker() -> AsyncGenerator[AsyncSession, None]:
    session = async_session_maker()
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        sentry_sdk.capture_exception(e)
        raise
    finally:
        await session.close()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


skipped_tables = []


async def create_tables():
    async with engine.begin() as conn:
        tables_need_create = [
            table
            for table in SQLModel.metadata.tables.values()
            if table.name not in skipped_tables
        ]
        await conn.run_sync(
            lambda connection: SQLModel.metadata.create_all(
                connection, tables=tables_need_create
            )
        )
        await conn.commit()


async def drop_tables():
    async with engine.begin() as conn:
        tables_need_drop = [
            table
            for table in SQLModel.metadata.tables.values()
            if table.name not in skipped_tables
        ]
        await conn.run_sync(
            lambda connection: SQLModel.metadata.drop_all(
                connection, tables=tables_need_drop
            )
        )
        await conn.commit()
