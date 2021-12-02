import http


async def test_index(client, upgrade_and_populate_db):
    client, _ = client
    response = await client.get('/')
    assert response.status == http.HTTPStatus.OK
