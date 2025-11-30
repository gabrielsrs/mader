import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from mader.models import User
from dataclasses import asdict

@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    new_user = User(username='test', email='test', password='test')

    session.add(new_user)
    await session.commit()

    user = await session.scalar(select(User).where(User.username == 'test'))

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test',
        'password': 'test',
    }
