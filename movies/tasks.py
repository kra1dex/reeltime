import time
from datetime import datetime, timedelta

import pytz
from celery import shared_task
from celery_singleton import Singleton
from decouple import config
from django.core.mail import send_mail

from movies.get_timezone import get_timezone
from movies.models import Movie, UserMovieRelation
from users.models import User


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


@shared_task
def publish_movie(movie_id, request_data, meta_data):
    timezone = pytz.timezone(get_timezone(meta_data))

    publish_in = datetime.strptime(request_data['publish_in'], '%Y-%m-%d-%H:%M:%S')
    now = datetime.strptime(datetime.strptime(str(datetime.now(timezone)), '%Y-%m-%d %H:%M:%S.%f%z').strftime('%Y-%m-%d-%H:%M:%S'), '%Y-%m-%d-%H:%M:%S')

    while now < publish_in:
        time.sleep(1)
        now += timedelta(seconds=1)

    movie = Movie.objects.get(id=movie_id)
    movie.status = 'publish'
    movie.save()


@shared_task
def mailing_about_movie(movie_id):
    movie = Movie.objects.get(id=movie_id)
    users = User.objects.all()

    subject = 'New movie available'
    message = f'Movie "{movie.title}" is now available for viewing.'
    from_email = config('EMAIL_HOST_USER')
    recipient_list = [user.email for user in users]

    send_mail(subject, message, from_email, recipient_list)
