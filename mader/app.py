from fastapi import FastAPI
from mader.routers import auth, users, books, authors

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(authors.router)
