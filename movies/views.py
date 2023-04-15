from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from movies.models import Movie, Director
from movies.permissions import IsAdminOrPublished
from movies.serializers import DirectorSerializer, MovieSerializer


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieListCreateAPIView(ListCreateAPIView):
    queryset = Movie.objects.all().prefetch_related('directors')
    serializer_class = MovieSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAdminOrPublished]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class MovieRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAdminOrPublished]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
