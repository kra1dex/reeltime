from django.db import IntegrityError
from rest_framework import serializers

from movies.models import Movie, Director, UserMovieRelation, Genre
from movies.tasks import set_movie_rating, set_movie_likes, publish_movie


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'director': ['Director already exists.']})

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'director': ['Director already exists.']})


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.PrimaryKeyRelatedField(many=True, queryset=Director.objects.all())
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')

    class Meta:
        model = Movie
        exclude = ['spectators']

    def is_valid(self, *, raise_exception=False):
        self.genres = self.initial_data.pop('genres')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        if 'publish_in' in validated_data:
            publish_movie.delay(self.context['request'])

        movie = super().create(validated_data)

        for genre in self.genres:
            genre_obj, _ = Genre.objects.get_or_create(title=genre)
            movie.genres.add(genre_obj)

        movie.save()
        return movie

    def update(self, instance, validated_data):
        for genre in self.genres:
            genre_obj, _ = Genre.objects.get_or_create(title=genre)
            instance.genres.add(genre_obj)

        instance.save()
        return instance


class UserMovieRelationRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ['rating']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        movie = instance
        rating = validated_data['rating']

        try:
            relation = UserMovieRelation.objects.get(user=user, movie=movie)
            if relation.rating != rating:
                relation.rating = rating
                set_movie_rating.delay(movie.id)
        except UserMovieRelation.DoesNotExist:
            relation = UserMovieRelation.objects.create(user=user, movie=movie, rating=rating)
            set_movie_rating.delay(movie.id)

        relation.save()
        return relation


class UserMovieRelationLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMovieRelation
        fields = ['like']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        movie = instance

        try:
            relation = UserMovieRelation.objects.get(user=user, movie=movie)
            relation.like = False if relation.like else True
        except UserMovieRelation.DoesNotExist:
            relation = UserMovieRelation.objects.create(user=user, movie=movie, like=True)
        relation.save()

        set_movie_likes.delay(movie.id)
        return relation
