import asyncio
import sys

from fastapi import FastAPI

from mader.routers import auth, authors, books, users

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(authors.router)
