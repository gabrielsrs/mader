from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models import User
from mader.schemas import (
    PublicUser,
    UserSchema,
)
from mader.security import get_current_user, get_password_hash

router = APIRouter(prefix='/conta', tags=['users'])
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PublicUser)
async def create_user(user: UserSchema, session: Session):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                datail='Username already exists',
                status_code=HTTPStatus.CONFLICT,
            )

        if db_user.email == user.email:
            raise HTTPException(
                datail='Email already exists', status_code=HTTPStatus.CONFLICT
            )

    new_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.senha),
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.put('/{id}')
def update_user(
    id: int, user: UserSchema, session: Session, current_user: CurrentUser
): ...


@router.delete('/{id}')
def delete_user(id: int, session: Session, current_user: CurrentUser): ...
