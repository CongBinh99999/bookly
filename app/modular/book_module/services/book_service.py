from sqlmodel.ext.asyncio.session import AsyncSession 
from schemas.book_schemas import BookCreateModule, BookUpdateModule
from sqlmodel import text
from datetime import datetime 
import uuid
class BookServices: 
    async def get_all_books(self, session: AsyncSession) : 
        statement = text(
            """
            SELECT * FROM books
            ORDER BY created_at DESC
            """
        )

        result = await session.execute(statement= statement)
        books = [dict(row) for row in result.mappings().all()]
        return books 

    async def get_book(self, book_uid: str, session: AsyncSession): 
        statement = text(
            """
            SELECT * FROM books 
            WHERE uid = :uid
            """
        )

        result = await session.execute(statement= statement, params= {"uid": book_uid})
        row = result.mappings().first()

        if row is None: 
            return None 
        return dict()

    async def create_book(self, book_data: BookCreateModule, session: AsyncSession): 
        book_uid = uuid.uuid4()
        current_time = datetime.now()

        params ={
            "uid": book_uid, 
            **book_data.model_dump(), 
            "page_count": 0, 
            "language": ""
        }


        statement = text(
            """
            IINSERT INTO books (uid, title, author, publisher, published_date, 
                              page_count, language, created_at, updated_at)
                        VALUES (:uid, :title, :author, :publisher, :published_date, 
                   :page_count, :language, :created_at, :updated_at)
            RETURING * 
            """ 
        )

        result = await session.execute(statement= statement, params= params)
        await session.commit() 

        book = result.mappings().first 

        return dict(book)

    async def update_book(self, book_uid:str ,book_update_data: BookUpdateModule, session: AsyncSession): 
        book = await self.get_book(book_uid, session)
        if book is None: 
            return None 
        
        update_fields = [] 
        params = {"uid": book_uid}

        update_dict = book_update_data.model_dump(exclude_unset= True) 
        for field, value in update_dict.items(): 
            if value is not None: 
                update_fields.append(f"{field} = :{field}")
                params[field] = value 
        
        update_fields.append("updated_at = :updated_at")
        params["updated_at"] = datetime.now()

        if len(update_fields) == 1: 
            return book
        
        update_data = ", ".join(update_fields)
        statement = text(
            f"""
                UPDATE books 
                SET {update_data}
                WHERE uid = :uid
                RETURNING *
            """
        )

        result = await session.execute(statement= statement, params= params)
        await session.commit()

        book = result.mappings().first() 
        if book is None: 
            return None 
        return book 
    async def delete_book(self, book_uid:str,  session: AsyncSession): 
        book = await self.get_book(book_uid= book_uid, session= session)
        if book is None: 
            return None 
        
        statement = text(
            """
            DELETE FROM books 
            WHERE uid = :uid
            """     
        )

        result = await session.execute(statement= statement, params={"uid": book_uid})
        session.commit() 
        
        return result.rowcount > 0 
