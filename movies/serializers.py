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

    def update(self, instance, validated_data):
        if self.context['request'].method == 'PATCH':
            validated_data['name'] = validated_data['name'].lower() if 'name' in validated_data else instance.name
            validated_data['surname'] = validated_data['surname'].lower() if 'surname' in validated_data else instance.surname

        if self.context['request'].method == 'PUT':
            validated_data['name'] = validated_data['name'].lower()
            validated_data['surname'] = validated_data['surname'].lower()

        try:
            director = Director.objects.get(name=validated_data['name'], surname=validated_data['surname'])
            if director.id != instance.id:
                raise serializers.ValidationError({'director': ['Director already exists.']})
        except Director.DoesNotExist:
            director = super().update(instance, validated_data)

        return director


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.PrimaryKeyRelatedField(many=True, queryset=Director.objects.all())

    class Meta:
        model = Movie
        fields = '__all__'
