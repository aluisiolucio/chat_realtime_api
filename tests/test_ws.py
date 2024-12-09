from http import HTTPStatus

import pytest
from fastapi.websockets import WebSocketDisconnect


def test_websocket_unauthorized(client, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CREATED

    room_id = response.json()['id']

    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect(
            f'/api/v1/chat/{room_id}?token=12345'
        ) as ws:
            ws.receive_json()


def test_websocket_connection(client, client_ws, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Room', 'description': 'A test chat room'},
    )
    assert response.status_code == HTTPStatus.CREATED

    room_id = response.json()['id']

    with client_ws(room_id) as ws1, client_ws(room_id) as ws2:
        ws1.send_json({'content': 'Hello, World!'})

        message_ws2 = ws2.receive_json()
        assert message_ws2['content'] == 'Hello, World!'

        message_ws1 = ws1.receive_json()
        assert message_ws1['content'] == 'User Teste has joined the chat.'


def test_websocket_message_history(client, client_ws, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'History Room',
            'description': 'A room for message history',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    room_id = response.json()['id']

    with client_ws(room_id) as ws1, client_ws(room_id) as ws2:
        ws1.send_json({'content': 'First message'})
        ws1.send_json({'content': 'Second message'})

        message1 = ws2.receive_json()
        message2 = ws2.receive_json()

        assert message1['content'] == 'First message'
        assert message2['content'] == 'Second message'


def test_websocket_broadcast(client, client_ws, token):
    response = client.post(
        '/api/v1/rooms',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Broadcast Room',
            'description': 'A test room for broadcast',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    room_id = response.json()['id']

    with (
        client_ws(room_id) as ws1,
        client_ws(room_id) as ws2,
        client_ws(room_id) as ws3,
    ):
        ws1.send_json({'content': 'Hello from Client 1'})

        message_ws3 = ws3.receive_json()
        message_ws2 = ws2.receive_json()
        message_ws1 = ws1.receive_json()

        assert message_ws1['content'] == 'User Teste has joined the chat.'
        assert message_ws2['content'] == 'User Teste has joined the chat.'
        assert message_ws3['content'] == 'Hello from Client 1'
