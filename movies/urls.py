from django.urls import path, include
from rest_framework import routers

from movies import views

router = routers.DefaultRouter()
router.register('directors', views.DirectorViewSet)
router.register('movies', views.MovieViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
