import json
from http import HTTPStatus

from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from movies.models import Movie, Director, Genre
from movies.serializers import MovieSerializer, DirectorSerializer, GenreSerializer
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

    # def test_post_admin(self):
    #     self.assertEqual(Movie.objects.count(), 2)
    #     self.assertEqual(Genre.objects.count(), 3)
    #
    #     json_data = json.dumps({
    #         'status': 'publish',
    #         'title': 'test',
    #         'description': 'test',
    #         'directors': [self.director1.id],
    #         'genres': ['first', 'second'],
    #     })
    #
    #     path = reverse('movie-list-create')
    #     response = self.client.post(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)
    #
    #     # проверить овнера
    #     # сделать с publish_in
    #
    #     self.assertEqual(response.status_code, HTTPStatus.CREATED)
    #     self.assertEqual(Movie.objects.count(), 3)
    #     self.assertEqual(Genre.objects.count(), 3)

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

    def test_get_retrieve_admin(self):
        # Publish
        path = reverse('movie-retrieve-update-destroy', args=[self.movie1.id])
        response = self.client.get(path, HTTP_AUTHORIZATION=self.admin_bearer)

        expected_data = MovieSerializer(self.movie1).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

        # Archive
        path = reverse('movie-retrieve-update-destroy', args=[self.movie2.id])
        response = self.client.get(path, HTTP_AUTHORIZATION=self.admin_bearer)

        expected_data = MovieSerializer(self.movie2).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

    def test_get_retrieve_user(self):
        # Publish
        path = reverse('movie-retrieve-update-destroy', args=[self.movie1.id])
        response = self.client.get(path, HTTP_AUTHORIZATION=self.user_bearer)

        expected_data = MovieSerializer(self.movie1).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

        # Archive
        path = reverse('movie-retrieve-update-destroy', args=[self.movie2.id])
        response = self.client.get(path, HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Not found.', code='not_found')})

    def test_get_retrieve_unauthorized(self):
        # Publish
        path = reverse('movie-retrieve-update-destroy', args=[self.movie1.id])
        response = self.client.get(path)

        expected_data = MovieSerializer(self.movie1).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

        # Archive
        path = reverse('movie-retrieve-update-destroy', args=[self.movie2.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Not found.', code='not_found')})

    def test_put_admin(self):
        json_data = json.dumps({
            'status': 'publish',
            'title': 'test',
            'description': 'test',
            'directors': [self.director1.id],
            'genres': ['first', 'second'],
        })

        path = reverse('movie-retrieve-update-destroy', args=[self.movie2.id])
        response = self.client.put(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['status'], 'publish')
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['description'], 'test')
        self.assertEqual(response.data['directors'], [self.director1.id])
        self.assertEqual(response.data['genres'], ['first', 'second'])
        self.assertEqual(response.data['owner'], self.admin.id)

    def test_put_user(self):
        path = reverse('movie-retrieve-update-destroy', args=[self.movie2.id])
        response = self.client.put(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_put_unauthorized(self):
        path = reverse('movie-retrieve-update-destroy', args=[self.movie2.id])
        response = self.client.put(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_patch_admin(self):
        json_data = json.dumps({
            'status': 'archive',
            'description': 'test',
            'genres': ['fourth', 'third'],
        })

        path = reverse('movie-retrieve-update-destroy', args=[self.movie1.id])
        response = self.client.patch(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['status'], 'archive')
        self.assertEqual(response.data['title'], 'movie1')
        self.assertEqual(response.data['description'], 'test')
        self.assertEqual(response.data['directors'], [self.director1.id, self.director2.id])
        self.assertEqual(response.data['genres'], ['third', 'fourth'])
        self.assertEqual(response.data['owner'], self.admin.id)

    def test_patch_user(self):
        path = reverse('movie-retrieve-update-destroy', args=[self.movie1.id])
        response = self.client.patch(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_patch_unauthorized(self):
        path = reverse('movie-retrieve-update-destroy', args=[self.movie1.id])
        response = self.client.patch(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_delete_admin(self):
        self.assertEqual(Movie.objects.count(), 2)

        path = reverse('movie-retrieve-update-destroy', args=[self.movie1.id])
        response = self.client.delete(path, HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 1)

    def test_delete_user(self):
        self.assertEqual(Movie.objects.count(), 2)
        path = reverse('movie-retrieve-update-destroy', args=[self.movie1.id])
        response = self.client.delete(path, HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})
        self.assertEqual(Movie.objects.count(), 2)

    def test_delete_unauthorized(self):
        self.assertEqual(Movie.objects.count(), 2)
        path = reverse('movie-retrieve-update-destroy', args=[self.movie1.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})
        self.assertEqual(Movie.objects.count(), 2)


class DirectorCRUDTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.user = User.objects.create_user(username='user', password='password', email='user@gmail.com')

        self.director1 = Director.objects.create(name='director1', surname='director1', biography='director1')
        self.director2 = Director.objects.create(name='director2', surname='director2', biography='director2')

        # Auth
        admin_token = self.client.post('/api/v1/token/', data=json.dumps({'username': 'admin', 'password': 'password'}), content_type='application/json').data
        self.admin_bearer = f"Bearer {admin_token['access']}"

        user_token = self.client.post('/api/v1/token/', data=json.dumps({'username': 'user', 'password': 'password'}), content_type='application/json').data
        self.user_bearer = f"Bearer {user_token['access']}"

    def test_get_list(self):
        path = reverse('director-list')
        response = self.client.get(path)

        expected_data = DirectorSerializer([self.director1, self.director2], many=True).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

    def test_post_admin(self):
        self.assertEqual(Director.objects.count(), 2)
        json_data = json.dumps({
            'name': 'test',
            'surname': 'test',
            'biography': 'test',
        })

        path = reverse('director-list')
        response = self.client.post(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Director.objects.count(), 3)

    def test_post_admin_duplicate(self):
        self.assertEqual(Director.objects.count(), 2)
        json_data = json.dumps({
            'name': 'director1',
            'surname': 'director1',
            'biography': 'director1',
        })

        path = reverse('director-list')
        response = self.client.post(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, {'director': [ErrorDetail(string='Director already exists.', code='invalid')]})

    def test_post_user(self):
        path = reverse('director-list')
        response = self.client.post(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_post_unauthorized(self):
        path = reverse('director-list')
        response = self.client.post(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_get_retrieve(self):
        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.get(path)

        expected_data = DirectorSerializer(self.director1).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

    def test_put_admin(self):
        json_data = json.dumps({
            'name': 'test',
            'surname': 'test',
            'biography': 'test',
        })

        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.put(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['surname'], 'test')
        self.assertEqual(response.data['biography'], 'test')

    def test_put_user(self):
        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.put(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_put_unauthorized(self):
        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.put(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_patch_admin(self):
        json_data = json.dumps({
            'name': 'test',
        })

        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.patch(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['surname'], 'director1')
        self.assertEqual(response.data['biography'], 'director1')

    def test_patch_user(self):
        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.patch(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_patch_unauthorized(self):
        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.patch(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_delete_admin(self):
        self.assertEqual(Director.objects.count(), 2)
        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.delete(path, HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Director.objects.count(), 1)

    def test_delete_user(self):
        self.assertEqual(Director.objects.count(), 2)
        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.delete(path, HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_delete_unauthorized(self):
        self.assertEqual(Director.objects.count(), 2)
        path = reverse('director-detail', args=[self.director1.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})


class GenreCRUDTestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin', password='password', is_staff=True)
        self.user = User.objects.create_user(username='user', password='password', email='user@gmail.com')

        self.genre1 = Genre.objects.create(title='genre1', description='genre1')
        self.genre2 = Genre.objects.create(title='genre2')

        # Auth
        admin_token = self.client.post('/api/v1/token/', data=json.dumps({'username': 'admin', 'password': 'password'}), content_type='application/json').data
        self.admin_bearer = f"Bearer {admin_token['access']}"

        user_token = self.client.post('/api/v1/token/', data=json.dumps({'username': 'user', 'password': 'password'}), content_type='application/json').data
        self.user_bearer = f"Bearer {user_token['access']}"

    def test_get_list(self):
        path = reverse('genre-list')
        response = self.client.get(path)

        expected_data = GenreSerializer([self.genre1, self.genre2], many=True).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

    def test_post_admin(self):
        path = reverse('genre-list')

        json_data = json.dumps({
            'title': 'test',
            'description': 'test',
        })

        response = self.client.post(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['description'], 'test')

        json_data = json.dumps({
            'title': 'test',
        })

        response = self.client.post(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, {'title': [ErrorDetail(string='genre with this title already exists.', code='unique')]})

        json_data = json.dumps({
            'title': 'test1',
        })

        response = self.client.post(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.data['title'], 'test1')
        self.assertEqual(response.data['description'], None)

    def test_post_user(self):
        path = reverse('genre-list')
        response = self.client.post(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_post_unauthorized(self):
        path = reverse('genre-list')
        response = self.client.post(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_get(self):
        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.get(path)

        expected_data = GenreSerializer(self.genre1).data

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, expected_data)

    def test_put_admin(self):
        json_data = json.dumps({
            'title': 'test',
            'description': 'test',
        })

        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.put(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['description'], 'test')

    def test_put_user(self):
        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.put(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_put_unauthorized(self):
        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.put(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_patch_admin(self):
        json_data = json.dumps({
            'title': 'test',
        })

        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.patch(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['description'], 'genre1')

        json_data = json.dumps({
            'title': 'test',
        })

        path = reverse('genre-detail', args=[self.genre2.id])
        response = self.client.patch(path, data=json_data, content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, {'title': [ErrorDetail(string='genre with this title already exists.', code='unique')]})

    def test_patch_user(self):
        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.patch(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_patch_unauthorized(self):
        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.patch(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    def test_delete_admin(self):
        self.assertEqual(Genre.objects.count(), 2)
        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.delete(path, HTTP_AUTHORIZATION=self.admin_bearer)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 1)

    def test_delete_user(self):
        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.delete(path, data='', content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})

    def test_delete_unauthorized(self):
        path = reverse('genre-detail', args=[self.genre1.id])
        response = self.client.delete(path, data='', content_type='application/json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})


class UserMovieRelationTestCase(APITestCase):
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

        # Auth
        admin_token = self.client.post('/api/v1/token/', data=json.dumps({'username': 'admin', 'password': 'password'}), content_type='application/json').data
        self.admin_bearer = f"Bearer {admin_token['access']}"

        user_token = self.client.post('/api/v1/token/', data=json.dumps({'username': 'user', 'password': 'password'}), content_type='application/json').data
        self.user_bearer = f"Bearer {user_token['access']}"

    def test_like(self):
        path = reverse('movie-like', args=[self.movie1.id])

        movie = Movie.objects.get(id=self.movie1.id)
        self.assertEqual(movie.likes, 0)

        response = self.client.put(path, HTTP_AUTHORIZATION=self.admin_bearer)
        self.assertEqual(response.data['like'], True)

        response = self.client.put(path, HTTP_AUTHORIZATION=self.admin_bearer)
        self.assertEqual(response.data['like'], False)

        response = self.client.put(path, HTTP_AUTHORIZATION=self.admin_bearer)
        self.assertEqual(response.data['like'], True)

        response = self.client.put(path, HTTP_AUTHORIZATION=self.user_bearer)
        self.assertEqual(response.data['like'], True)

        movie.refresh_from_db()
        self.assertEqual(movie.likes, 2)

    def test_like_unauthorized(self):
        path = reverse('movie-like', args=[self.movie1.id])
        response = self.client.put(path)

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})

    # def test_rating(self):
    #     path = reverse('movie-rating', args=[self.movie1.id])
    #
    #     movie = Movie.objects.get(id=self.movie1.id)
    #     self.assertEqual(movie.rating, None)
    #
    #     response = self.client.put(path, data=json.dumps({'rating': 5}), content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)
    #     self.assertEqual(response.data['rating'], 5)
    #
    #     response = self.client.put(path, data=json.dumps({'rating': 2}), content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)
    #     self.assertEqual(response.data['rating'], 2)
    #
    #     response = self.client.put(path, data=json.dumps({'rating': 4}), content_type='application/json', HTTP_AUTHORIZATION=self.user_bearer)
    #     self.assertEqual(response.data['rating'], 4)
    #
    #     movie.refresh_from_db()
    #     self.assertEqual(movie.rating, 3)
    #
    #     response = self.client.put(path, data=json.dumps({'rating': 4}), content_type='application/json', HTTP_AUTHORIZATION=self.admin_bearer)
    #     self.assertEqual(response.data['rating'], 4)
    #
    #     movie.refresh_from_db()
    #     self.assertEqual(movie.rating, 4)

    def test_rating_unauthorized(self):
        path = reverse('movie-rating', args=[self.movie1.id])
        response = self.client.put(path)

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')})
