import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from mader.app import app
from mader.database import get_session
from mader.models import Author, Book, User, table_registry
from mader.security import get_password_hash


@pytest_asyncio.fixture
async def client(session):
    def get_session_overrride():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_overrride

        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope='session')
async def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        yield create_async_engine(postgres.get_connection_url())


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = 'testtest'
    new_user = UserFactory(password=get_password_hash(password))

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    new_user.clean_password = password

    return new_user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']


@pytest_asyncio.fixture
async def author(session: AsyncSession):
    new_author = AuthorFactory()

    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)

    return new_author


@pytest_asyncio.fixture
async def other_author(session: AsyncSession):
    new_author = AuthorFactory(name='other_author')

    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)

    return new_author


@pytest_asyncio.fixture
async def book(session: AsyncSession, author):
    new_book = BookFactory(author_id=author.id)

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book


@pytest_asyncio.fixture
async def other_book(session: AsyncSession):
    new_book = BookFactory(title='other_book')

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}:{obj.email}')


class AuthorFactory(factory.Factory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f'author{n}')


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    year = factory.Sequence(lambda n: 2000 + n)
    title = factory.LazyAttribute(lambda obj: f'Title{obj.year}')
    author_id = 1
