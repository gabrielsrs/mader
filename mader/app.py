import asyncio
import sys

from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException

from mader.handlers import custom_http_exception_handler
from mader.routers import auth, authors, books, users

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

app.add_exception_handler(
    StarletteHTTPException, custom_http_exception_handler
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(authors.router)
