from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from app.modular.book_module.schemas.book_schemas import BookResponse, BookCreateRequest, BookUpdateRequest
from typing import List

router = APIRouter() 

@router.get("", response_model= List[BookResponse])
async def get_all_books(): 
    pass

@router.post("", response_model= BookResponse, status_code= status.HTTP_201_CREATED)
async def create_books(book_data: BookCreateRequest):
    new_book = book_data.model_dump() #model_dump() chuyển đổi object -> dict

@router.get("/{book_id}", response_model= BookResponse)
async def get_book(book_id: int ): 
    pass

@router.patch("/{book_id}", response_model= BookResponse)
async def update_book(book_id: int, update_data: BookUpdateRequest): 
    pass


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int): 
    pass