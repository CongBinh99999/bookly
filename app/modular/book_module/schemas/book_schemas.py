from pydantic import BaseModel 
import uuid
from datetime import datetime

class Book(BaseModel): 
    title: str 
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str 
    created_at: datetime
    updated_at: datetime 
    

class BookResponse(BaseModel): 
    id: uuid.UUID
    
class BookCreateModule(BaseModel): 
    title: str
    author: str
    publisher: str
    published_date: str
    created_at: datetime
    updated_at: datetime 

class BookUpdateModule(BaseModel):
    title: str | None = None 
    author: str | None = None
    publisher: str | None = None
    page_count: int | None = None


