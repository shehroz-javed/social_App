from rest_framework import serializers

from .models import User, Profile
from friend_request.serializers import AllFriendSerializer


class UserRegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError(
                'Password and Confirm Password does not match')
        return data

    def create(self, data):
        return User.objects.create_user(**data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    friends = AllFriendSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'bio', 'image', 'user', 'friends']
