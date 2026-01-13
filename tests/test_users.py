from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/conta',
        json={
            'username': 'alice',
            'email': 'alice@mader.com',
            'senha': 'alice:mader',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@mader.com',
    }


def test_create_existed_user(client, user):
    response = client.post(
        '/conta',
        json={
            'username': user.username,
            'email': 'alice@mader.com',
            'senha': 'alice:mader',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_update_user(client, user, token):
    response = client.put(
        f'/conta/{user.id}',
        json={
            'username': 'alice',
            'email': 'alice@mader.com',
            'senha': 'Alice1:@mader',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@mader.com',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/conta/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
