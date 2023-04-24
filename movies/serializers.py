from rest_framework import serializers

from movies.models import Movie, Director


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

    def create(self, validated_data):
        try:
            Director.objects.get(name=validated_data['name'], surname=validated_data['surname'])
            raise serializers.ValidationError({'director': ['Director already exists.']})
        except Director.DoesNotExist:
            director = Director.objects.create(name=validated_data['name'], surname=validated_data['surname'])

        return director


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.PrimaryKeyRelatedField(many=True, queryset=Director.objects.all())

    class Meta:
        model = Movie
        fields = '__all__'
