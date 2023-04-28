from http import HTTPStatus

import pytest
from rest_framework.exceptions import ErrorDetail

from movies.serializers import MovieSerializer


@pytest.mark.django_db
def test_get_retrieve_admin_publish(client, admin_token, movie_publish):
    response = client.get(f'/api/v1/movies/{movie_publish.id}/', HTTP_AUTHORIZATION=f'Token {admin_token}')

    expected_response = MovieSerializer(movie_publish).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_retrieve_admin_archive(client, admin_token, movie_archive):
    response = client.get(f'/api/v1/movies/{movie_archive.id}/', HTTP_AUTHORIZATION=f'Token {admin_token}')

    expected_response = MovieSerializer(movie_archive).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_retrieve_user_publish(client, user_token, movie_publish):
    response = client.get(f'/api/v1/movies/{movie_publish.id}/', HTTP_AUTHORIZATION=f'Token {user_token}')

    expected_response = MovieSerializer(movie_publish).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_retrieve_user_archive(client, user_token, movie_archive):
    response = client.get(f'/api/v1/movies/{movie_archive.id}/', HTTP_AUTHORIZATION=f'Token {user_token}')

    expected_response = {'detail': ErrorDetail(string='Not found.', code='not_found')}

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_retrieve_unauthorized_publish(client, movie_publish):
    response = client.get(f'/api/v1/movies/{movie_publish.id}/')

    expected_response = MovieSerializer(movie_publish).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_retrieve_unauthorized_archive(client, movie_archive):
    response = client.get(f'/api/v1/movies/{movie_archive.id}/')

    expected_response = {'detail': ErrorDetail(string='Not found.', code='not_found')}

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.data == expected_response
