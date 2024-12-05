from http import HTTPStatus


def test_create_room(client, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Test Room'
    assert response.json()['description'] == 'A test chat room'


def test_create_room_missing_name(client, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'detail' in response.json()


def test_create_room_missing_description(client, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Test Room'
    assert response.json()['description'] is None


def test_create_room_duplicate(client, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Test Room'
    assert response.json()['description'] == 'A test chat room'

    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert 'detail' in response.json()


def test_get_rooms(client, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Test Room'
    assert response.json()['description'] == 'A test chat room'

    room_name = response.json()['name']
    room_description = response.json()['description']

    response = client.get(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()['rooms'][0]['name'] == room_name
    assert response.json()['rooms'][0]['description'] == room_description


def test_get_empty_rooms(client, token):
    response = client.get(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['rooms']) == 0
