from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from src.schemas import BookResponse, BookCreateRequest, BookUpdateRequest
from typing import List
from src.database import books

router = APIRouter() 

@router.get("", response_model= List[BookResponse])
async def get_all_books(): 
    return books 

@router.post("", response_model= BookResponse, status_code= status.HTTP_201_CREATED)
async def create_books(book_data: BookCreateRequest):
    new_book = book_data.model_dump() #model_dump() chuyển đổi object -> dict

    # Tạo ID mới một cách an toàn - tránh lỗi khi danh sách rỗng
    if books:
        id = max(b["id"] for b in books) + 1
    else:
        id = 1  # ID đầu tiên nếu danh sách rỗng

    new_book["id"] = id
    books.append(new_book)
    return new_book

@router.get("/{book_id}", response_model= BookResponse)
async def get_book(book_id: int ): 
    for book in books: 
        if book["id"] == book_id: 
            return book
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Not Found")

@router.patch("/{book_id}", response_model= BookResponse)
async def update_book(book_id: int, update_data: BookUpdateRequest): 
    for book in books: 
        if book["id"] == book_id: 
            if update_data.title is not None:
                book["title"] = update_data.title
            if update_data.author is not None:
                book["author"] = update_data.author
            if update_data.publisher is not None:
                book["publisher"] = update_data.publisher
            if update_data.page_count is not None:
                book["page_count"] = update_data.page_count
            return book  
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND, 
        detail="Not Found"
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int): 
    for book in books: 
        if book["id"] == book_id:
            books.remove(book)
            return {}
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND, 
        detail="Not Found"
    )