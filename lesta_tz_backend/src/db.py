from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{str(DB_USER)}:{str(DB_PASS)}@{str(DB_HOST)}:{str(DB_PORT)}/{str(DB_NAME)}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_session_maker()
    async with async_session as session:
        try:
            yield session
        finally:
            await session.close()