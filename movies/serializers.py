from rest_framework import serializers

from movies.models import Movie, Director


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class MovieCreateSerializer(serializers.ModelSerializer):
    directors = DirectorSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        super().is_valid()
        self.directors = self.validated_data.pop('directors')

    def create(self, validated_data):
        movie = Movie.objects.create(**validated_data)

        for director in self.directors:
            director, _ = Director.objects.get_or_create(name=director['name'], surname=director['surname'])
            movie.directors.add(director)

        return movie
