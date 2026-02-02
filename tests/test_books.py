from http import HTTPStatus


def test_get_book_by_title(client, book):
    response = client.get(f'/livro/?titulo={book.title[0]}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'livros': [
            {
                'id': book.id,
                'year': int(book.year),
                'title': book.title,
                'author_id': book.author_id,
            }
        ]
    }


def test_get_book_by_title_without_book(client):
    response = client.get('/livro/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'livros': []}


def test_get_non_existed_page(client):
    response = client.get('/livro/?page=2')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'livros': []}


def test_get_book_by_id(client, book):
    response = client.get(f'/livro/{book.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'year': int(book.year),
        'title': book.title,
        'author_id': book.author_id,
    }


def test_get_non_existed_book_by_id(client):
    response = client.get('/livro/10')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'message': 'Book not found'}


def test_create_book(client, token, author):
    response = client.post(
        '/livro',
        json={
            'ano': 1973,
            'titulo': 'Cafe Da Manha dos Campeoes',
            'romancista_id': author.id,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    response.status_code = HTTPStatus.CREATED
    response.json() == {
        'id': 1,
        'year': 1973,
        'title': 'Cafe Da Manha dos Campeoes',
        'author_id': author.id,
    }


def test_create_book_with_existed_title(client, token, author, book):
    response = client.post(
        '/livro',
        json={
            'ano': 1973,
            'titulo': book.title,
            'romancista_id': author.id,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    response.status_code = HTTPStatus.CONFLICT
    response.json() == {'message': f'{book.title} already exist'}


def test_update_book(client, book, token):
    response = client.patch(
        f'/livro/{book.id}',
        json={
            'ano': 1973,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': book.id,
        'year': 1973,
        'title': book.title,
        'author_id': book.author_id,
    }


def test_update_non_existed_book(client, token, book):
    response = client.patch(
        '/livro/10',
        json={'ano': 1999},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'message': 'Book not exist'}


def test_update_book_with_existed_title(client, token, book, other_book):
    other_title = other_book.title
    response = client.patch(
        f'/livro/{book.id}',
        json={'titulo': other_title},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'message': f'{other_title} already exist'}


def test_delete_book(client, book, token):
    response = client.delete(
        f'/livro/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Book deleted'}


def test_delete_non_existed_book(client, token):
    response = client.delete(
        '/livro/10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'message': 'Book not exist'}
