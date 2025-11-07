from fastapi import APIRouter

router = APIRouter(prefix='/auth')

@router.post('/token')
def token():
    ...

@router.post('/refresh-token')
def refresh_token():
    ...

