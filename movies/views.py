from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from movies.models import Movie, Director
from movies.serializers import DirectorSerializer, MovieSerializer, MoviePostSerializer, MoviePutSerializer


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieListCreateAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MoviePostSerializer
        else:
            return MovieSerializer


class MovieRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return MoviePutSerializer
        else:
            return MovieSerializer
