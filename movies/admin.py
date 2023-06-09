from django.contrib import admin

from movies.models import Director, Movie, UserMovieRelation, Genre

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(UserMovieRelation)
admin.site.register(Genre)
