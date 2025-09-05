from fastapi import FastAPI 
from src.endpoints import router as book_routers 

version = "v1"
app = FastAPI(
    title="Book",
    description="Hoc API",
    version= version
) 

app.include_router(book_routers, prefix=f"/api/{version}/books")






