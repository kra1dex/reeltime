from http import HTTPStatus

import pytest
from rest_framework.exceptions import ErrorDetail

from movies.models import Director


@pytest.mark.django_db
def test_put_admin(client, admin_token, movies):
    director4 = Director.objects.create(name='name4', surname='surname4')

    data = {
        'status': 'publish',
        'directors': [movies[0].directors.first().id, director4.id],
        'title': 'new_title',
        'description': 'new_description',
    }

    response = client.put(
        f'/api/v1/movies/{movies[0].id}/',
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {admin_token}'
    )

    expected_response = {
        'id': movies[0].id,
        'status': 'publish',
        'directors': [movies[0].directors.first().id, director4.id],
        'title': 'new_title',
        'description': 'new_description',
    }

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_put_without_fields(client, admin_token, movies):
    data = {}

    response = client.put(
        f'/api/v1/movies/{movies[0].id}/',
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


@pytest.mark.django_db
def test_put_user(client, user_token, movies):
    data = {}

    response = client.put(
        f'/api/v1/movies/{movies[0].id}/',
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {user_token}'
    )

    expected_response = {
        'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')
    }

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.data == expected_response


@pytest.mark.django_db
def test_put_unauthorized(client, movies):
    data = {}

    response = client.put(
        f'/api/v1/movies/{movies[0].id}/',
        data,
        content_type='application/json'
    )

    expected_response = {
        'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')
    }

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == expected_response
