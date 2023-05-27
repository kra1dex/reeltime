from celery import shared_task
from celery_singleton import Singleton

from movies.models import Movie, UserMovieRelation


@shared_task(base=Singleton)
def set_movie_rating(movie_id):
    movie = Movie.objects.get(id=movie_id)

    movies = UserMovieRelation.objects.filter(movie=movie)
    average_rating = sum([movie.rating for movie in movies]) / len(movies)

    movie.rating = average_rating
    movie.save()


@shared_task
def set_movie_likes(movie_id, like):
    movie = Movie.objects.get(id=movie_id)

    if like:
        movie.likes += 1
    else:
        movie.likes -= 1

    movie.save()
