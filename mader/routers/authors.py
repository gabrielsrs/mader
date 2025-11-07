from fastapi import APIRouter

router = APIRouter(prefix='/romancista')

@router.get('/')
def filter_author():
    ...

@router.get('/{id}')
def read_book():
    ...

@router.post('/')
def create_book():
    ...

@router.patch('/{id}')
def update_book():
    ...

@router.delete('/{id}')
def delete_book():
    ...
