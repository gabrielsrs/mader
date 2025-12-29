from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models import User
from mader.schemas import Message, PublicUser, UserSchema
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
                detail='Username already exists',
                status_code=HTTPStatus.CONFLICT,
            )

        if db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists', status_code=HTTPStatus.CONFLICT
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


@router.put('/{id}', response_model=PublicUser)
async def update_user(
    id: int, user: UserSchema, session: Session, current_user: CurrentUser
):
    if id != current_user.id:
        raise HTTPException(
            detail='User do not have access to make this change',
            status_code=HTTPStatus.FORBIDEN,
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.senha)

        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            detail='Username or Email already exists',
            status_code=HTTPStatus.CONFLICT,
        )


@router.delete('/{id}', response_model=Message)
async def delete_user(id: int, session: Session, current_user: CurrentUser):
    if id != current_user.id:
        raise HTTPException(
            detail='User do not have access to make this change',
            status_code=HTTPStatus.FORBIDEN,
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
