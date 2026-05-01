from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from bot.core.config import settings


async_session_maker: async_sessionmaker[AsyncSession] | None = None
async_engine: AsyncEngine | None = None


async def init_db():
    global async_engine, async_session_maker
    if async_engine:
        return

    async_engine = create_async_engine(
        settings.db_uri
    )
    async_session_maker = async_sessionmaker[AsyncSession](
        bind=async_engine,
        expire_on_commit=False,
    )

async def session_provider():
    if not async_session_maker:
        raise RuntimeError("DB is not initialized")
    return async_session_maker()