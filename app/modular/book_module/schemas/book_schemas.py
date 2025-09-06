from pydantic import BaseModel 

class BookBase(BaseModel): 
    title: str 
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str 

class BookResponse(BookBase): 
    id: int 
    
class BookCreateRequest(BookBase): 
    pass

class BookUpdateRequest(BaseModel):
    title: str | None = None  # Optional field cho update
    author: str | None = None  # Optional field cho update
    publisher: str | None = None  # Optional field cho update
    page_count: int | None = None  # Optional field cho update

