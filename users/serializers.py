from django.contrib.auth import password_validation
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers


class CustomUserCreateSerializer(UserCreateSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, attrs):
        password_validation.validate_password(attrs['password'])

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        del attrs['password2']

        return attrs
