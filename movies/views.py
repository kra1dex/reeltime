from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from movies.models import Movie, Director
from movies.permissions import IsAdminOrPublished
from movies.serializers import DirectorSerializer, MovieSerializer, UserMovieRelationSerializer


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


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


class UserMovieRelationAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Movie.objects.all()
    serializer_class = UserMovieRelationSerializer
