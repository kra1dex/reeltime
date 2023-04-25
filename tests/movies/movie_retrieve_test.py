from http import HTTPStatus

import pytest
from rest_framework.exceptions import ErrorDetail

from movies.serializers import MovieSerializer


@pytest.mark.django_db
def test_get_retrieve_admin(client, admin_token, movies):
    response = client.get(f'/api/v1/movies/{movies[0].id}/', HTTP_AUTHORIZATION=f'Token {admin_token}')

    expected_response = MovieSerializer(movies[0]).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_retrieve_user(client, user_token, movies):
    response = client.get(f'/api/v1/movies/{movies[1].id}/', HTTP_AUTHORIZATION=f'Token {user_token}')

    expected_response = MovieSerializer(movies[1]).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_retrieve_unauthorized(client, movies):
    response = client.get(f'/api/v1/movies/{movies[1].id}/')

    expected_response = MovieSerializer(movies[1]).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_retrieve_user_archive(client, user_token, movies):
    response = client.get('/api/v1/movies/1/', HTTP_AUTHORIZATION=f'Token {user_token}')

    expected_response = {'detail': ErrorDetail(string='Not found.', code='not_found')}

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_retrieve_unauthorized_archive(client, movies):
    response = client.get('/api/v1/movies/1/')

    expected_response = {'detail': ErrorDetail(string='Not found.', code='not_found')}

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.data == expected_response
