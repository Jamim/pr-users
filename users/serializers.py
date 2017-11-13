from rest_framework import serializers

from django.contrib.auth import get_user_model


user_model = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = user_model(**validated_data)
        user.set_password(password)
        user.save()
        return user
