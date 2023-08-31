from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from .models import Profile

User = get_user_model()
# create profile on post_save user model


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
