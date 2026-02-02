from http import HTTPStatus


def test_get_author_by_name(client, author):
    response = client.get(f'/romancista/?nome={author.name[0]}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'romancistas': [{'id': author.id, 'name': author.name}]
    }


def test_get_author_by_name_without_user(client):
    response = client.get('/romancista/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'romancistas': []}


def test_get_non_existed_page(client):
    response = client.get('/romancista/?page=2')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'romancistas': []}


def test_get_author_by_id(client, author):
    response = client.get(f'/romancista/{author.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': author.id, 'name': author.name}


def test_get_non_existed_author_by_id(client):
    response = client.get('/romancista/10')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'message': 'Author not found'}


def test_create_author(client, token):
    response = client.post(
        '/romancista',
        json={'nome': 'Clarice'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'id': 1, 'name': 'clarice'}


def test_create_user_with_existed_name(client, token, author):
    response = client.post(
        '/romancista',
        json={'nome': f'{author.name}'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'message': f'{author.name} already exist'}


def test_update_author(client, token, author):
    response = client.patch(
        f'/romancista/{author.id}',
        json={'nome': 'Clarice'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': 1, 'name': 'clarice'}


def test_update_non_existed_author(client, token, author):
    response = client.patch(
        '/romancista/10',
        json={'nome': 'Clarice'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'message': 'Author not exist'}


def test_update_author_with_existed_name(client, token, author, other_author):
    other_name = other_author.name
    response = client.patch(
        f'/romancista/{author.id}',
        json={'nome': f'{other_name}'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'message': f'{other_name} already exist'}


def test_delete_author(client, token, author):
    response = client.delete(
        f'/romancista/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Author successfully deleted'}


def test_delete_non_existed_author(client, token):
    response = client.delete(
        '/romancista/10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'message': 'Author not exist'}
