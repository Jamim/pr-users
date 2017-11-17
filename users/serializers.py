from rest_framework import serializers

from django.contrib.auth import get_user_model


user_model = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'password'
        )
        extra_kwargs = dict(
            password=dict(write_only=True, required=False),
            first_name=dict(required=True, allow_blank=False),
            last_name=dict(required=True, allow_blank=False),
            email=dict(required=True, allow_blank=False),
        )


class NewUserSerializer(UserSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = user_model(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CredentialsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ('id', 'username')
