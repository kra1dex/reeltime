import pytest

from movies.models import Movie, Director


@pytest.mark.django_db
def test_movies_list(client):
    director = Director.objects.create(name='name', surname='surname')
    movie = Movie.objects.create(title='title', description='description')
    movie.directors.set([director])

    expected_response = [{
        'id': movie.pk,
        'directors': [1],
        'title': 'title',
        'description': 'description',
    }]

    response = client.get('/api/v1/movies/')

    assert response.status_code == 200
    assert response.data == expected_response
