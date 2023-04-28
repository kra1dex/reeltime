from http import HTTPStatus

import pytest
from rest_framework.exceptions import ErrorDetail

from movies.models import Movie


@pytest.mark.django_db
def test_patch_admin(client, admin_token, movies):
    assert Movie.objects.count() == 3

    response = client.delete(f'/api/v1/movies/{movies[0].id}/', HTTP_AUTHORIZATION=f'Token {admin_token}')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert Movie.objects.count() == 2


@pytest.mark.django_db
def test_patch_user(client, user_token, movies):
    assert Movie.objects.count() == 3

    response = client.delete(f'/api/v1/movies/{movies[0].id}/', HTTP_AUTHORIZATION=f'Token {user_token}')

    expected_response = {
        'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')
    }

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.data == expected_response
    assert Movie.objects.count() == 3


@pytest.mark.django_db
def test_patch_unauthorized(client, movies):
    assert Movie.objects.count() == 3

    response = client.delete(f'/api/v1/movies/{movies[0].id}/')

    expected_response = {
        'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')
    }

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.data == expected_response
    assert Movie.objects.count() == 3
