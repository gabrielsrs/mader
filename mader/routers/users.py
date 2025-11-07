
from fastapi import APIRouter

router = APIRouter(prefix='/conta')

@router.post("/")
def create_user():
    ...

@router.put("/{id}")
def update_user():
    ...

@router.delete("/{id}")
def delete_user():
    ...
