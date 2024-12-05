from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/api/v1/users',
        json={
            'username': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json()
    assert 'username' in response.json()
    assert response.json()['username'] == 'alice@example.com'


def test_create_user_with_invalid_data(client):
    response = client.post(
        '/api/v1/users',
        json={
            'username': '',
            'password': '',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'detail' in response.json()


def test_create_user_with_duplicated(client, user):
    response = client.post(
        '/api/v1/users',
        json={
            'username': user.username,
            'password': user.clean_password,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert 'detail' in response.json()
