from rest_framework import serializers

from account.models import Friends, User
from .models import FriendRequest


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ['id', 'to_user', 'from_user', 'created_at']


class AllFriendSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='follower.id')
    username = serializers.CharField(source='follower.username')

    class Meta:
        model = Friends
        fields = ['user_id', 'username',]
