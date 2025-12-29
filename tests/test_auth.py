from http import HTTPStatus


def test_authentication(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'


def test_authentication_with_non_existed_user(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'alice@mader.com', 'password': '123567'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_unauthorized_user(client, user):
    response = client.put(
        f'/conta/{user.id}',
        json={
            'username': 'alice',
            'email': 'alice@mader.com',
            'password': '1234',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh-token', headers={'Authorization': f'Bearer {token}'}
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'
