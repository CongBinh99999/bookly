from sqlmodel import SQLModel, Field, Column
from datetime import datetime, date 
import uuid 
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.sql import func

class Book(SQLModel, table=True): 
    __tablename__ = "books"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
        )
    )
    title: str 
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str 
    # Sử dụng func.now() thay vì datetime.now để tránh vấn đề timezone
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, 
        default=func.now(), 
        nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP, 
            default=func.now(), 
            onupdate=func.now(),  # Tự động cập nhật khi record thay đổi
            nullable=False
        )
    )

    def __repr__(self):
        return f"<Book {self.title}>"