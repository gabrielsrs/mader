from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from mader.database import get_session
from mader.models import User
from mader.schemas import Token
from mader.security import create_access_token, verify_password

router = APIRouter(prefix='/auth')

Session = Annotated[AsyncSession, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
async def token(form_data: OAuth2Form, session: Session):
    user = await session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise HTTPException(
            datail='Incorrect email or password',
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            datail='Incorrect email or password',
            status_code=HTTPStatus.UNAUTHORIZED,
        )

    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh-token')
def refresh_token(): ...
