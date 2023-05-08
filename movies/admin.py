from django.contrib import admin

from movies.models import Director, Movie, UserMovieRelation

admin.site.register(Director)
admin.site.register(Movie)
admin.site.register(UserMovieRelation)
