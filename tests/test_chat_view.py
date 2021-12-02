import json
import http
from uuid import uuid4
from aiohttp.web import WSMsgType
from src.services import ChatService


async def test_msg_sending(client, upgrade_and_populate_db):
    client, app = client

    async with app['db'].acquire() as conn:
        chats = await ChatService.get_chats(conn)

    user1, user2, text_to_send = 'test', 'test1', 'hi'
    ws1 = await client.ws_connect('/chat/{0}?username={1}'.format(chats[0].uuid, user1))
    ws2 = await client.ws_connect('/chat/{0}?username={1}'.format(chats[0].uuid, user2))

    ack_msg1 = await ws1.receive()
    assert ack_msg1.type == WSMsgType.TEXT
    assert json.loads(ack_msg1.data)['body'] == '{0} joined'.format(user2)

    await ws1.send_str(text_to_send)
    received_msg = await ws2.receive()
    received_data = json.loads(received_msg.data)
    assert received_data['body'] == text_to_send
    assert received_data['author'] == user1


async def test_chat_access(client, upgrade_and_populate_db):
    client, app = client

    async with app['db'].acquire() as conn:
        chats = await ChatService.get_chats(conn)

    response = await client.get('/chat/{uuid}'.format(uuid=chats[0].uuid), data={'username': 'test'})
    assert response.status == http.HTTPStatus.OK

    response = await client.get('/chat/{uuid}'.format(uuid=uuid4()), data={'username': 'test'})
    assert response.status == http.HTTPStatus.NOT_FOUND

    response = await client.get('/chat/{uuid}'.format(uuid='wrong-uuid', data={'username': 'test'}))
    assert response.status == http.HTTPStatus.NOT_FOUND

    user1, user2, text_to_send = 'test', 'test1', 'hi'
    ws1 = await client.ws_connect('/chat/{0}?username={1}'.format(chats[0].uuid, user1))
    await client.ws_connect('/chat/{0}?username={1}'.format(chats[0].uuid, user1))

    ack_msg = await ws1.receive()
    assert ack_msg.type == WSMsgType.CLOSE

    ws1 = await client.ws_connect('/chat/{0}?username={1}'.format(chats[0].uuid, user1))
    ws2 = await client.ws_connect('/chat/{0}?username={1}'.format(chats[0].uuid, user2))

    await ws1.close()
    ack_msg = await ws2.receive()
    assert ack_msg.type == WSMsgType.TEXT
    assert json.loads(ack_msg.data)['body'] == '{0} disconnected'.format(user1)
