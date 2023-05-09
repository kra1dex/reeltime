from rest_framework import serializers

from movies.models import Movie, Director, UserMovieRelation


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].lower()
        validated_data['surname'] = validated_data['surname'].lower()

        try:
            Director.objects.get(name=validated_data['name'], surname=validated_data['surname'])
            raise serializers.ValidationError({'director': ['Director already exists.']})
        except Director.DoesNotExist:
            return super().create(validated_data)

    def update(self, instance, validated_data):
        if self.context['request'].method == 'PATCH':
            validated_data['name'] = validated_data['name'].lower() if 'name' in validated_data else instance.name
            validated_data['surname'] = validated_data['surname'].lower() if 'surname' in validated_data else instance.surname
        elif self.context['request'].method == 'PUT':
            validated_data['name'] = validated_data['name'].lower()
            validated_data['surname'] = validated_data['surname'].lower()
        validated_data['biography'] = validated_data['biography'] if 'biography' in validated_data else instance.biography

        try:
            director = Director.objects.get(name=validated_data['name'], surname=validated_data['surname'])
            if director.id != instance.id:
                raise serializers.ValidationError({'director': ['Director already exists.']})
            return super().update(instance, validated_data)
        except Director.DoesNotExist:
            return super().update(instance, validated_data)


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.PrimaryKeyRelatedField(many=True, queryset=Director.objects.all())

    class Meta:
        model = Movie
        exclude = ['spectators']


class UserMovieRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ['rating']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        movie = instance
        rating = validated_data['rating']

        try:
            relation = UserMovieRelation.objects.get(user=user, movie=movie)
            relation.rating = rating
        except UserMovieRelation.DoesNotExist:
            relation = UserMovieRelation.objects.create(user=user, movie=movie, rating=rating)
        relation.save()

        movies = UserMovieRelation.objects.filter(movie=movie)
        average_rating = sum([movie.rating for movie in movies]) / len(movies)
        movie.rating = average_rating
        movie.save()

        return relation
