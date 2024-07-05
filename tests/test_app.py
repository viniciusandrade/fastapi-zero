from http import HTTPStatus

from fast_zero.schemas import UserPublic


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


def test_update_users(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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


def test_delete_users(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {
        'message': 'User deleted',
    }


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
