import pytest


@pytest.fixture
@pytest.mark.django_db
def admin_token(client, django_user_model):
    username = 'admin'
    password = 'password'

    django_user_model.objects.create_user(
        username=username,
        password=password,
        is_staff=True
    )

    response = client.post(
        '/auth/token/login/',
        {'username': username, 'password': password},
        content_type='application/json'
    )
    return response.data['auth_token']


@pytest.fixture
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = 'user'
    password = 'password'

    django_user_model.objects.create_user(
        username=username,
        password=password
    )

    response = client.post(
        '/auth/token/login/',
        {'username': username, 'password': password},
        content_type='application/json'
    )
    return response.data['auth_token']
