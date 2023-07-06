from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase

from movies.models import Movie, Director, Genre
from movies.serializers import MovieSerializer


class MovieCRUDTestCase(APITestCase):
    def setUp(self):
        self.director1 = Director.objects.create(name='director1', surname='director1', biography='director1')
        self.director2 = Director.objects.create(name='director2', surname='director2', biography='director2')

        self.genres = [Genre(title='first'), Genre(title='second'), Genre(title='third')]
        Genre.objects.bulk_create(self.genres)

        # Movie1
        self.movie1 = Movie.objects.create(title='movie1', description='movie1', status='publish')
        directors_for_movie1 = Director.objects.all()[:2]
        genres_for_movie1 = Genre.objects.all()[:1]
        self.movie1.directors.set(directors_for_movie1)
        self.movie1.genres.set(genres_for_movie1)

        # Movie2
        self.movie2 = Movie.objects.create(title='movie2', description='movie2', status='archive')
        directors_for_movie2 = Director.objects.all()[1:2]
        genres_for_movie2 = Genre.objects.all()[1:3]
        self.movie2.directors.set(directors_for_movie2)
        self.movie2.genres.set(genres_for_movie2)

        # publish_in

    def test_get_list_admin(self):
        path = reverse('movie-list-create')
        response = self.client.get(path)

        # выдаёт без второго фильма, потому что у него статус archive. соответсвенно надо накинуть HTTP_AUTHORIZATION

        expected_data = MovieSerializer([self.movie1, self.movie2], many=True).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)
