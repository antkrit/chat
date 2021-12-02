import http
from uuid import uuid4


async def test_404(client):
    client, _ = client
    response = await client.get('/no-such-route')
    assert response.status == http.HTTPStatus.NOT_FOUND


async def test_500(client):
    client, _ = client

    # get index view without setup db must cause 500 error
    response = await client.get('/')
    assert response.status == http.HTTPStatus.INTERNAL_SERVER_ERROR

    # get chat view without data must cause 500 error
    response = await client.get('/chat/{0}'.format(uuid4()))
    assert response.status == http.HTTPStatus.INTERNAL_SERVER_ERROR
