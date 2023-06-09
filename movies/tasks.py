import time
from datetime import datetime, timedelta

import pytz
from celery import shared_task
from celery_singleton import Singleton

from movies.get_timezone import get_timezone
from movies.models import Movie, UserMovieRelation


@shared_task(base=Singleton)
def set_movie_rating(movie_id):
    movie = Movie.objects.get(id=movie_id)

    movies = UserMovieRelation.objects.filter(movie=movie)
    average_rating = sum([movie.rating for movie in movies]) / len(movies)

    movie.rating = average_rating
    movie.save()


@shared_task(base=Singleton)
def set_movie_likes(movie_id):
    movie = Movie.objects.get(id=movie_id)

    movies = UserMovieRelation.objects.filter(movie=movie)
    movie.likes = sum([movie.like for movie in movies])

    movie.save()


@shared_task(base=Singleton)
def publish_movie(request):
    timezone = pytz.timezone(get_timezone(request))

    publish_in = datetime.strptime(request.data['publish_in'], '%Y-%m-%d-%H:%M:%S')
    now = datetime.strptime(datetime.strptime(str(datetime.now(timezone)), '%Y-%m-%d %H:%M:%S.%f%z').strftime('%Y-%m-%d-%H:%M:%S'), '%Y-%m-%d-%H:%M:%S')

    while now < publish_in:
        time.sleep(1)
        now += timedelta(seconds=1)
