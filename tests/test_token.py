from http import HTTPStatus


def test_login(client, user):
    response = client.post(
        '/api/v1/auth/login',
        data={'username': user.username, 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()


def test_refresh_token(client, token):
    response = client.post(
        '/api/v1/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['name'] == 'Teste'
    assert data['token_type'] == 'bearer'
