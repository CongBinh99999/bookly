from fastapi import FastAPI 
from app.modular.book_module.api.v1.endpoints import router as book_routers 
from contextlib import asynccontextmanager
from app.core.db import init_db

@asynccontextmanager
async def life_span(app: FastAPI): 
    print("Server is start")
    await init_db()
    yield
    print("Server has been stopped")

version = "v1"
app = FastAPI(
    title="Book",
    description="Hoc API",
    version= version,
    lifespan= life_span
) 

app.include_router(book_routers, prefix=f"/api/{version}")






