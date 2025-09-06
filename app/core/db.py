from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel, text
from app.core.config import config

engine: AsyncEngine = create_async_engine(
    url=config.DATABASE_URL,
    echo=True,   # In ra SQL khi chạy
    future=True
)

# Hàm khởi tạo DB (chạy lúc server start)
async def init_db() -> None:
    async with engine.begin() as conn:
        from app.modular.book_module.models.book_model import Book
        await conn.run_sync(SQLModel.metadata.create_all)

