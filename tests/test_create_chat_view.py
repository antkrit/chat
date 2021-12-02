import http
from src.services import ChatService


async def test_chat_creating(client, upgrade_and_populate_db):
    client, app = client
    async with app['db'].acquire() as conn:
        chats = await ChatService.get_chats(conn)
        num_of_chats_on_start = len(chats)

        response = await client.get('/create')
        assert response.status == http.HTTPStatus.OK

        response = await client.post('/create', data={'name': 'New chat'})
        assert response.status == http.HTTPStatus.OK
        chats = await ChatService.get_chats(conn)
        assert len(chats) == num_of_chats_on_start

        response = await client.post('/create', data={'name': 'Test', 'description': 'some text'})
        assert response.status == http.HTTPStatus.OK
        chats = await ChatService.get_chats(conn)
        assert len(chats) != num_of_chats_on_start
