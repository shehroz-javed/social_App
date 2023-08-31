from django.urls import path
from . views import PostView, LikeView, CommentView, PostList

urlpatterns = [
    path('posts/', PostView.as_view(), name='user-posts-list'),
    path('posts/<int:pk>/', PostView.as_view(), name='user-posts-detail'),
    path('like-or-unlike/<int:pk>/', LikeView.as_view(),
         name='like-or-unlike-post'),
    path('comment/<int:pk>/', CommentView.as_view(), name='comment-post'),
    path('post-feed/', PostList.as_view(), name='post-feed')
]
