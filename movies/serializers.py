from rest_framework import serializers

from movies.models import Movie, Director


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

        try:
            director = Director.objects.get(name=validated_data['name'], surname=validated_data['surname'])
            if director.id != instance.id:
                raise serializers.ValidationError({'director': ['Director already exists.']})
        except Director.DoesNotExist:
            return super().update(instance, validated_data)


class MovieSerializer(serializers.ModelSerializer):
    directors = serializers.PrimaryKeyRelatedField(many=True, queryset=Director.objects.all())

    class Meta:
        model = Movie
        fields = '__all__'
