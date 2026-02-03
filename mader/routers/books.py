from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models import Author, Book, User
from mader.schemas import (
    Books,
    BookSchema,
    BookUpdate,
    FilterBook,
    Message,
    PublicBook,
)
from mader.security import get_current_user

router = APIRouter(prefix='/livro', tags=['books'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=Books)
async def filter_book(
    session: Session, filter: Annotated[FilterBook, Query()]
):
    offset = (filter.page - 1) * 20
    limit = filter.page * 20

    stmt = select(Book)

    if filter.ano:
        stmt = stmt.where(Book.year == filter.ano).offset(offset).limit(limit)

    if filter.titulo:
        stmt = (
            stmt
            .where(Book.title.ilike(f'%{filter.titulo}%'))
            .offset(offset)
            .limit(limit)
        )

    books = await session.scalars(stmt)

    return {'livros': books}


@router.get('/{id}', response_model=PublicBook)
async def read_book(id: int, session: Session):
    db_book = await session.scalar(select(Book).where(Book.id == id))

    if not db_book:
        raise HTTPException(
            detail='Book not found', status_code=HTTPStatus.NOT_FOUND
        )

    return db_book


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PublicBook)
async def create_book(
    session: Session,
    book: BookSchema,
    current_user: CurrentUser,
):
    db_book = await session.scalar(
        select(Book).where(Book.title == book.titulo)
    )

    if db_book:
        raise HTTPException(
            detail=f'{book.titulo} already exist',
            status_code=HTTPStatus.CONFLICT,
        )

    db_author = await session.scalar(
        select(Author).where(Author.id == book.romancista_id)
    )

    if not db_author:
        raise HTTPException(
            detail=f'Author {book.romancista_id} not found',
            status_code=HTTPStatus.NOT_FOUND,
        )

    new_book = Book(
        year=book.ano,
        title=book.titulo,
        author_id=book.romancista_id,
    )

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book


@router.patch('/{id}', response_model=PublicBook)
async def update_book(
    id: int, session: Session, book: BookUpdate, current_user: CurrentUser
):
    current_book = await session.scalar(select(Book).where(Book.id == id))

    if not current_book:
        raise HTTPException(
            detail='Book not exist',
            status_code=HTTPStatus.NOT_FOUND,
        )

    try:
        if book.ano:
            current_book.year = book.ano

        if book.titulo:
            current_book.title = book.titulo

        if book.romancista_id:
            current_book.author_id = book.romancista_id

        await session.commit()
        await session.refresh(current_book)

        return current_book
    except IntegrityError:
        raise HTTPException(
            detail=f'{book.titulo} already exist',
            status_code=HTTPStatus.CONFLICT,
        )


@router.delete('/{id}', response_model=Message)
async def delete_book(id: int, session: Session, current_user: CurrentUser):
    current_book = await session.scalar(select(Book).where(Book.id == id))

    if not current_book:
        raise HTTPException(
            detail='Book not exist', status_code=HTTPStatus.NOT_FOUND
        )

    await session.delete(current_book)
    await session.commit()

    return {'message': 'Book deleted'}
