from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import FriendRequest
from .serializers import FriendRequestSerializer, AllFriendSerializer

from account.models import Friends

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class SendFriendRequest(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        to_user = get_object_or_404(User, id=pk)
        existing_request = FriendRequest.objects.filter(
            to_user=to_user, from_user=request.user).first()
        if existing_request is not None:
            return Response({"Message": "Friend request already exists"}, status=status.HTTP_409_CONFLICT)

        friend_request = FriendRequest.objects.create(
            to_user=to_user, from_user=request.user)
        serializer = FriendRequestSerializer(friend_request)
        return Response({"Message": "Friend request send successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):

        to_user = get_object_or_404(User, id=pk)
        friend_request = FriendRequest.objects.filter(
            to_user=to_user, from_user=request.user).first()
        if not friend_request:
            return Response({"Message": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)
        friend_request.delete()
        return Response({"Message": "Friend request cancelled successfully"}, status=status.HTTP_204_NO_CONTENT)


class AcceptFriendRequest(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        from_user = get_object_or_404(User, id=pk)

        friend_request = FriendRequest.objects.filter(
            to_user=request.user, from_user=from_user).first()
        serializer = FriendRequestSerializer(friend_request)
        if not friend_request:
            return Response({"Message": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        user1 = friend_request.to_user
        user2 = from_user
        Friends.objects.create(followed=user2, follower=user1)
        Friends.objects.create(followed=user1, follower=user2)
        friend_request.delete()
        return Response({'Message': 'Friend Request accepted successfully', "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, pk):

        user = get_object_or_404(User, pk=pk)
        friend_request = FriendRequest.objects.filter(
            to_user=request.user, from_user=user).first()
        if not friend_request:
            return Response({"Message": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)
        friend_request.delete()
        return Response({"Message": "Friend request cancelled successfully"}, status=status.HTTP_204_NO_CONTENT)


class AllFriend(APIView):

    def get(self, request):
        user = request.user
        friends = user.followed_user.prefetch_related('followed')
        serializer = AllFriendSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):

        user = request.user
        friend = get_object_or_404(User, id=pk)
        Friends.objects.filter(followed=user, follower=friend).delete()
        Friends.objects.filter(followed=friend, follower=user).delete()

        return Response({"Message": "Unfriend successfully"}, status=status.HTTP_200_OK)
