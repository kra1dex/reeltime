from http import HTTPStatus

import pytest

from movies.serializers import MovieSerializer


@pytest.mark.django_db
def test_get_list_admin(client, admin_token, create_movies):
    response = client.get('/api/v1/movies/', HTTP_AUTHORIZATION=f'Token {admin_token}')

    expected_response = MovieSerializer(list(create_movies), many=True).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_list_user(client, user_token, create_movies):
    response = client.get('/api/v1/movies/', HTTP_AUTHORIZATION=f'Token {user_token}')

    expected_response = MovieSerializer(list(create_movies[1:]), many=True).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response


@pytest.mark.django_db
def test_get_list_unauthorized(client, create_movies):
    response = client.get('/api/v1/movies/')

    expected_response = MovieSerializer(list(create_movies[1:]), many=True).data

    assert response.status_code == HTTPStatus.OK
    assert response.data == expected_response
