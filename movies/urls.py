from django.urls import path, include
from rest_framework import routers

from movies import views

router = routers.DefaultRouter()
router.register('directors', views.DirectorViewSet)
router.register('genres', views.GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Movies
    path('movies/', views.MovieListCreateAPIView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', views.MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie-retrieve-update-destroy'),

    # UserMovieRelation
    path('rating/<int:pk>/', views.UserMovieRelationAPIView.as_view(), name='movie-rating'),
    path('like/<int:pk>/', views.UserMovieRelationAPIView.as_view(), name='movie-like'),
]
