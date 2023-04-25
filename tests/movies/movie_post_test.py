from http import HTTPStatus

import pytest
from rest_framework.exceptions import ErrorDetail

from movies.models import Director, Movie


@pytest.mark.django_db
def test_post_movie_admin(client, admin_token):
    assert Movie.objects.count() == 0
    assert Director.objects.count() == 0

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
        'id': response.data['id'],
        'status': 'publish',
        'directors': [director.id],
        'title': 'title',
        'description': 'description',
    }

    assert response.status_code == HTTPStatus.CREATED
    assert response.data == expected_response
    assert Movie.objects.count() == 1
    assert Director.objects.count() == 1


@pytest.mark.django_db
def test_post_without_fields(client, admin_token):
    assert Movie.objects.count() == 0
    assert Director.objects.count() == 0

    data = {}

    response = client.post(
        '/api/v1/movies/',
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {admin_token}'
    )

    expected_response = {
        'directors': [ErrorDetail(string='This field is required.', code='required')],
        'title': [ErrorDetail(string='This field is required.', code='required')],
        'description': [ErrorDetail(string='This field is required.', code='required')]
    }

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data == expected_response
    assert Movie.objects.count() == 0
    assert Director.objects.count() == 0


@pytest.mark.django_db
def test_post_movie_user(client, user_token):
    assert Movie.objects.count() == 0
    assert Director.objects.count() == 0

    response = client.post(
        '/api/v1/movies/',
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {user_token}'
    )

    expected_response = {
        'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')
    }

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.data == expected_response
    assert Movie.objects.count() == 0
    assert Director.objects.count() == 0


@pytest.mark.django_db
def test_post_movie_unauthorized(client):
    assert Movie.objects.count() == 0
    assert Director.objects.count() == 0

    response = client.post(
        '/api/v1/movies/',
        content_type='application/json'
    )

    expected_response = {
        'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')
    }

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == expected_response
    assert Movie.objects.count() == 0
    assert Director.objects.count() == 0
