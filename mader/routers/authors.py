from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models import Author, User
from mader.schemas import (
    Authors,
    AuthorSchema,
    FilterAuthor,
    Message,
    PublicAuthor,
)
from mader.security import get_current_user

router = APIRouter(prefix='/romancista', tags=['authors'])

CurrentUser = Annotated[User, Depends(get_current_user)]
Session = Annotated[AsyncSession, Depends(get_session)]


@router.get('/', response_model=Authors)
async def filter_author(
    session: Session, filter: Annotated[FilterAuthor, Query()]
):
    offset = (filter.page - 1) * 20
    limit = filter.page * 20

    stmt = select(Author)

    if filter.nome:
        stmt = stmt.where(Author.name.ilike(f'%{filter.nome}%'))

    authors = await session.scalars(stmt.offset(offset).limit(limit))

    return {'romancistas': authors}


@router.get('/{id}', response_model=PublicAuthor)
async def read_author(id: int, session: Session):
    db_author = await session.scalar(select(Author).where(Author.id == id))

    if not db_author:
        raise HTTPException(
            detail='Author not found', status_code=HTTPStatus.NOT_FOUND
        )

    return db_author


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PublicAuthor)
async def create_author(
    author: AuthorSchema, session: Session, current_user: CurrentUser
):
    db_author = await session.scalar(
        select(Author).where(Author.name == author.nome)
    )

    if db_author:
        raise HTTPException(
            detail=f'{author.nome} already exist',
            status_code=HTTPStatus.CONFLICT,
        )

    new_author = Author(name=author.nome)

    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)

    return new_author


@router.patch('/{id}', response_model=PublicAuthor)
async def update_author(
    id: int, session: Session, author: AuthorSchema, current_user: CurrentUser
):
    current_author = await session.scalar(
        select(Author).where(Author.id == id)
    )

    if not current_author:
        raise HTTPException(
            detail='Author not exist', status_code=HTTPStatus.NOT_FOUND
        )

    try:
        current_author.name = author.nome

        session.add(current_author)
        await session.commit()
        await session.refresh(current_author)

        return current_author

    except IntegrityError:
        raise HTTPException(
            detail=f'{author.nome} already exist',
            status_code=HTTPStatus.CONFLICT,
        )


@router.delete('/{id}', response_model=Message)
async def delete_author(id: int, session: Session, current_user: CurrentUser):
    current_author = await session.scalar(
        select(Author).where(Author.id == id)
    )

    if not current_author:
        raise HTTPException(
            detail='Author not exist', status_code=HTTPStatus.NOT_FOUND
        )

    await session.delete(current_author)
    await session.commit()

    return {'message': 'Author successfully deleted'}
