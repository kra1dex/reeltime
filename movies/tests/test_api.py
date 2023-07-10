import json
from http import HTTPStatus

from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from movies.models import Movie, Director, Genre
from movies.serializers import MovieSerializer, DirectorSerializer
from users.models import User


class MovieCRUDTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.user = User.objects.create_user(username='user', password='password', email='user@gmail.com')

        self.director1 = Director.objects.create(name='director1', surname='director1', biography='director1')
        self.director2 = Director.objects.create(name='director2', surname='director2', biography='director2')

        self.genres = [Genre(title='first'), Genre(title='second'), Genre(title='third')]
        Genre.objects.bulk_create(self.genres)

        # Movie1
        self.movie1 = Movie.objects.create(title='movie1', description='movie1', status='publish', owner=self.admin)
        directors_for_movie1 = Director.objects.all()[:2]
        genres_for_movie1 = Genre.objects.all()[:1]
        self.movie1.directors.set(directors_for_movie1)
        self.movie1.genres.set(genres_for_movie1)

        # Movie2
        self.movie2 = Movie.objects.create(title='movie2', description='movie2', status='archive', owner=self.admin)
        directors_for_movie2 = Director.objects.all()[1:2]
        genres_for_movie2 = Genre.objects.all()[1:3]
        self.movie2.directors.set(directors_for_movie2)
        self.movie2.genres.set(genres_for_movie2)

        # Auth
        admin_token = self.client.post('/api/v1/token/', data=json.dumps({'username': 'admin', 'password': 'password'}), content_type='application/json').data
        self.admin_bearer = f"Bearer {admin_token['access']}"

        user_token = self.client.post('/api/v1/token/', data=json.dumps({'username': 'user', 'password': 'password'}), content_type='application/json').data
        self.user_bearer = f"Bearer {user_token['access']}"

    def test_get_list_admin(self):
        path = reverse('movie-list-create')
        response = self.client.get(path, HTTP_AUTHORIZATION=self.admin_bearer)

        expected_data = MovieSerializer([self.movie1, self.movie2], many=True).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

    def test_get_list_user(self):
        path = reverse('movie-list-create')
        response = self.client.get(path, HTTP_AUTHORIZATION=self.user_bearer)

        expected_data = MovieSerializer([self.movie1], many=True).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

    def test_get_list_unauthorized(self):
        path = reverse('movie-list-create')
        response = self.client.get(path)

        expected_data = MovieSerializer([self.movie1], many=True).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

    def test_post_admin(self):
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(Genre.objects.count(), 3)

        json_data = json.dumps({
            'status': 'publish',
            'title': 'test',
            'description': 'test',
            'directors': [self.director1.id],
            'genres': ['first', 'second'],
        })

        path = reverse('movie-list-create')

        response = self.client.post(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        # проверить овнера
        # сделать с publish_in

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Movie.objects.count(), 3)
        self.assertEqual(Genre.objects.count(), 3)

    def test_post_user(self):
        path = reverse('movie-list-create')
        response = self.client.post(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_post_unauthorized(self):
        path = reverse('movie-list-create')
        response = self.client.post(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})


class DirectorCRUDTestCase(APITestCase):
    def setUp(self):
        self.director1 = Director.objects.create(name='director1', surname='director1', biography='director1')
        self.director2 = Director.objects.create(name='director2', surname='director2', biography='director2')

    def test_get_list(self):
        path = reverse('director-list')
        response = self.client.get(path)

        expected_data = DirectorSerializer([self.director1, self.director2], many=True).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)
