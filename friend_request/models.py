from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FriendRequest(models.Model):

    to_user = models.ForeignKey(
        User, related_name='received_friend_requests', on_delete=models.CASCADE)
    from_user = models.ForeignKey(
        User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Friend Request'
        verbose_name_plural = 'Friend Requests'

    def __str__(self):
        return f'to_user {self.to_user}--from_user {self.from_user}'
