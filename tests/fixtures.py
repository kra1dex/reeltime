import pytest

from movies.models import Director, Movie


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


@pytest.fixture
def movies():
    director1 = Director.objects.create(name='name1', surname='surname1')
    director2 = Director.objects.create(name='name2', surname='surname2')
    director3 = Director.objects.create(name='name3', surname='surname3')

    movie1 = Movie.objects.create(title='title1', description='description1')
    movie1.directors.set([director1, director2])
    movie2 = Movie.objects.create(title='title2', description='description2', status='publish')
    movie2.directors.set([director1, director3])
    movie3 = Movie.objects.create(title='title3', description='description3', status='publish')
    movie3.directors.set([director2])

    return movie1, movie2, movie3
