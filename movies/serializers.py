from rest_framework import serializers

from movies.models import Movie, Director
from movies.validations import MovieValidation


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MoviePostSerializer(MovieValidation, serializers.ModelSerializer):
    directors = DirectorSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        super(MovieValidation, self).is_valid(raise_exception=raise_exception)
        self.directors = self.validated_data.pop('directors')

    def create(self, validated_data):
        movie = Movie.objects.create(**validated_data)

        for director in self.directors:
            director, _ = Director.objects.get_or_create(name=director['name'], surname=director['surname'])
            movie.directors.add(director)

        return movie


class MoviePutSerializer(MovieValidation, serializers.ModelSerializer):
    directors = DirectorSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        super(MovieValidation, self).is_valid(raise_exception=raise_exception)
        self.directors = self.validated_data.pop('directors')

    def update(self, instance, validated_data):
        movie = super().update(instance, validated_data)

        movie.directors.clear()
        for director in self.directors:
            director, _ = Director.objects.get_or_create(name=director['name'], surname=director['surname'])
            movie.directors.add(director)

        return movie
