from .serializers import UserRegisterSerializer, UserProfileSerializer
from .models import Profile

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class Register(APIView):

    def post(self, request):

        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Message": "User Successfully Registered"}, status=status.HTTP_201_CREATED)


class UserProfile(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        profile = Profile.objects.filter(user=user).first()
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):

        user = request.user
        profile = Profile.objects.filter(user=user).first()
        serializer = UserProfileSerializer(
            profile, data=request.data,  partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)

        return Response({"Message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
