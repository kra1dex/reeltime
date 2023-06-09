from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from movies.models import Movie, Director, Genre
from movies.permissions import IsAdminOrPublished
from movies.serializers import DirectorSerializer, MovieSerializer, UserMovieRelationRatingSerializer, \
    UserMovieRelationLikeSerializer, GenreSerializer


class DirectorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

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

    def get_serializer_class(self):
        if 'rating' in self.request.path:
            return UserMovieRelationRatingSerializer
        else:
            return UserMovieRelationLikeSerializer
