from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mader.database import get_session
from mader.models import User
from mader.schemas import Token
from mader.security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

Session = Annotated[AsyncSession, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
async def token(form_data: OAuth2Form, session: Session):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            detail='Incorrect email or password',
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            detail='Incorrect email or password',
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh-token', response_model=Token)
def refresh_token(user: Annotated[User, Depends(get_current_user)]):

    new_access_token = create_access_token(data={'sub': user.email})
    return {'access_token': new_access_token, 'token_type': 'Bearer'}
