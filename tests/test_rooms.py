from http import HTTPStatus


def test_create_room(client, token, user):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Test Room'
    assert response.json()['description'] == 'A test chat room'
    assert response.json()['creator_id'] == str(user.id)


def test_create_room_missing_name(client, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert 'detail' in response.json()


def test_create_room_missing_description(client, token, user):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Test Room'
    assert response.json()['description'] is None
    assert response.json()['creator_id'] == str(user.id)


def test_create_room_duplicate(client, token, user):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Test Room'
    assert response.json()['description'] == 'A test chat room'
    assert response.json()['creator_id'] == str(user.id)

    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert 'detail' in response.json()


def test_get_rooms(client, token, user):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Test Room'
    assert response.json()['description'] == 'A test chat room'
    assert response.json()['creator_id'] == str(user.id)

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
    assert response.json()['rooms'][0]['creator_id'] == str(user.id)


def test_get_empty_rooms(client, token):
    response = client.get(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['rooms']) == 0


def test_history_room_without_messages(client, token, user):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )

    room_id = response.json()['id']

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Test Room'
    assert response.json()['description'] == 'A test chat room'
    assert response.json()['creator_id'] == str(user.id)

    response = client.get(
        f'/api/v1/rooms/{room_id}/history',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['room_id'] == room_id
    assert response.json()['messages'] == []
    assert response.json()['pagination']['current_page'] == 1
    assert response.json()['pagination']['page_size'] == 10  # noqa: PLR2004
    assert response.json()['pagination']['total_pages'] == 0
    assert response.json()['pagination']['total_messages'] == 0
