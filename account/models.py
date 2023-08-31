from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# User model


class User(AbstractUser):

    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.username}'

# Profile model


def image_size_validate(image):
    max_size = 10*1024*1024
    if image.size > max_size:
        raise ValidationError("Image file size must not be greater than 10 MB")


def image_filename(instance, filename):
    return f'profile_pics/{instance.user.username}-{filename}'


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=254, blank=True)
    image = models.ImageField(upload_to=image_filename,
                              validators=[image_size_validate], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    @property
    def friends(self):
        return self.user.followed_user.prefetch_related('followed')

    def __str__(self):
        return f'{self.user.username}'


class Friends(models.Model):

    follower = models.ForeignKey(
        User, related_name='follower_user', on_delete=models.CASCADE)
    followed = models.ForeignKey(
        User, related_name='followed_user', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'

    def __str__(self):
        return f'{self.follower}'
