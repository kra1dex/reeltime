from rest_framework.serializers import ModelSerializer

from movies.models import Movie, Director


class DirectorSerializer(ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
