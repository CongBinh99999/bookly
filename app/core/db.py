from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel
from app.core.config import config
from contextlib import asynccontextmanager
from typing import AsyncGenerator

async_engine: AsyncEngine = create_async_engine(
    url=config.DATABASE_URL,
    echo=True, 
    future=True,
    pool_pre_ping=True,
)

#tạo một session factory 
async_session_maker = async_sessionmaker(
    async_engine, 
    expire_on_commit= False, 
    class_ = AsyncSession, 
    autoflush= False, 
    autocommit=False  
)

# Context manager để sử dụng trong code (hỗ trợ nhiều ngôn ngữ )
@asynccontextmanager 
async def get_db_session() -> AsyncGenerator[AsyncSession, None]: 
    session: AsyncSession = async_session_maker()
    try: 
        yield session 
        await session.commit()
    except: 
        await session.rollback()
        raise
    finally: 
        await session.close()

# Dependency để sử dụng trong FastAPI routes
async def get_session()-> AsyncGenerator[AsyncSession, None]: 
    async with async_session_maker() as session: 
        yield session

# Hàm khởi tạo DB (chạy lúc server start)
async def init_db() -> None:
    async with async_engine.begin() as conn:
        from app.modular.book_module.models.book_model import Book
        await conn.run_sync(SQLModel.metadata.create_all)
