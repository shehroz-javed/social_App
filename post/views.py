from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from .models import Post, Like, Comment

User = get_user_model()


class PostView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination()

    def get(self, request, pk=None):

        if pk:
            post = get_object_or_404(Post, id=pk, user=request.user)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)

        posts = Post.objects.filter(user=request.user).order_by('-id')
        paginated_query = self.pagination_class.paginate_queryset(
            posts, request)
        serializer = PostSerializer(paginated_query, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

    def post(self, request):

        has_image = request.data.get('image')
        has_video = request.data.get('video')
        post_type = None
        if has_image:
            post_type = 'Image_type'
        elif has_video:
            post_type = 'Video_type'
        else:
            post_type = 'Simple_type'
        request.data['post_type'] = post_type

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({"Message": "Post created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def delete(self, reqeust, pk):

        post = get_object_or_404(Post, id=pk, user=reqeust.user)
        post.delete()
        return Response({"Message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class LikeView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        user = request.user
        post = get_object_or_404(Post, id=pk)
        like = Like.objects.filter(user=user, post=post).exists()
        if like:
            Like.objects.filter(user=user, post=post).delete()
            return Response({"Message": "Un-like the post successfully"}, status=status.HTTP_200_OK)
        else:
            like = Like.objects.create(user=user, post=post)
            serializer = LikeSerializer(like)
            return Response({"Message": "Like the post successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)


class CommentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        post = get_object_or_404(Post, id=pk)
        request.data['post'] = post.id
        request.data['user'] = request.user.id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Message": "Comment successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):

        comment = get_object_or_404(Comment, id=pk, user=request.user)
        comment.delete()
        return Response({"Message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PostList(APIView):

    pagination_class = PageNumberPagination()

    def get(self, request):

        user_friends = request.user.followed_user.all()
        user_instance = User.objects.filter(follower_user__in=user_friends)

        user_posts = Post.objects.filter(
            user=request.user).order_by('-created_at')
        friend_posts = Post.objects.filter(
            user__in=user_instance).order_by('-created_at')
        all_posts = user_posts | friend_posts

        paginated_queryset = self.pagination_class.paginate_queryset(
            all_posts, request)
        serializer = PostSerializer(paginated_queryset, many=True)

        return self.pagination_class.get_paginated_response(serializer.data)
