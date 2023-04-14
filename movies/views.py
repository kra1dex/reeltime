from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from movies.models import Movie, Director
from movies.serializers import DirectorSerializer, MovieSerializer


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieListCreateAPIView(ListCreateAPIView):
    queryset = Movie.objects.all().prefetch_related('directors')
    serializer_class = MovieSerializer


class MovieRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
