from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    # Enviando dados no formato UserSchema
    response = client.post(
        '/users/',
        json={
            'username': 'John Doe',
            'email': 'john@teste.com',
            'password': '123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    # Validando se dados retornaram no formato UserPublic
    assert response.json() == {
        'id': 1,
        'username': 'John Doe',
        'email': 'john@teste.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_users(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'John Doe Updated',
            'email': 'john@teste.com',
            'password': '123',
        },
    )

    assert response.json() == {
        'id': 1,
        'username': 'John Doe Updated',
        'email': 'john@teste.com',
    }


def test_delete_users(client, user):
    response = client.delete('/users/1')

    assert response.json() == {
        'message': 'User deleted',
    }
