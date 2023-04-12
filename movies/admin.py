from django.contrib import admin

from movies.models import Movie, Director

admin.site.register(Movie)
admin.site.register(Director)
