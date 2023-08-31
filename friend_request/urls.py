from django.urls import path
from .views import SendFriendRequest, AcceptFriendRequest, AllFriend

urlpatterns = [
    path('send-or-cancel/<int:pk>/', SendFriendRequest.as_view(),
         name='send-or-cancel-friend-request'),
    path('accept-or-delete/<int:pk>/', AcceptFriendRequest.as_view(),
         name='accept-or-delete-friend-request'),
    path('all-friend/', AllFriend.as_view(), name='all-friend'),
    path('delete-friend/<int:pk>/', AllFriend.as_view(), name='delete-friend')
]
