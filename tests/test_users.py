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
        'username': 'alice',
        'email': 'alice@mader.com',
    }


def test_update_user(client): ...


def test_delete_user(client): ...
