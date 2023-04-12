from rest_framework.viewsets import ModelViewSet

from movies.models import Movie, Director
from movies.serializers import MovieSerializer, DirectorSerializer


class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
