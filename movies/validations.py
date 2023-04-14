from rest_framework import serializers


class MovieValidation(serializers.ModelSerializer):
    def is_valid(self, *, raise_exception=False):
        super().is_valid()

        if self.errors:
            raise serializers.ValidationError(self.errors)
