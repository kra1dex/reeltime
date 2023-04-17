import pytest
from rest_framework.exceptions import ErrorDetail

from movies.models import Director


@pytest.mark.django_db
def test_post_movie_admin(client, admin_token):
    director = Director.objects.create(name='name1', surname='surname1')

    data = {
        'status': 'publish',
        'directors': [director.id],
        'title': 'title',
        'description': 'description',
    }

    response = client.post(
        '/api/v1/movies/',
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {admin_token}'
    )

    expected_response = {
        'id': 1,
        'status': 'publish',
        'directors': [director.id],
        'title': 'title',
        'description': 'description',
    }

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_post_movie_user(client, user_token):

    response = client.post(
        '/api/v1/movies/',
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {user_token}'
    )

    expected_response = {
        'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')
    }

    assert response.status_code == 403
    assert response.data == expected_response


@pytest.mark.django_db
def test_post_movie_unauthorized(client):

    response = client.post(
        '/api/v1/movies/',
        content_type='application/json'
    )

    expected_response = {
        'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')
    }

    assert response.status_code == 401
    assert response.data == expected_response
