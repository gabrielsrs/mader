from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi.security import OAuth2PasswordBearer
from jwt import encode
from pwdlib import PasswordHash

from mader.settings import Settings

pwd_context = PasswordHash.recommended()

settings = Settings()
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: str):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def get_current_user(): ...
