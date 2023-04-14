from django.urls import path, include
from rest_framework import routers

from movies import views

router = routers.DefaultRouter()
router.register('directors', views.DirectorViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('movies/', views.MovieListCreateAPIView.as_view(), name='movie-list-create'),
    path('movies/<int:pk>/', views.MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie-retrieve-update-destroy'),
]
