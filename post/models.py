from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

User = get_user_model()

# Post model


def image_size_validate(image):
    max_size = 10*1024*1024
    if image.size > max_size:
        raise ValidationError("Image size must not be greater then 10 MB")


def video_size_validate(video):
    max_size = 50*1024*1024
    if video.size > max_size:
        raise ValidationError("Video size must not be greater than 50 MB")


def image_filename(instance, filename):
    return f'post_pics/{instance.user.username}-{filename}'


def video_filename(instance, filename):
    return f'post_videos/{instance.user.username}-{filename}'


class Post(models.Model):

    class PostType(models.TextChoices):
        SIMPLE = "Simple_type"
        IMAGE = "Image_type"
        VIDEO = "Video_type"

    user = models.ForeignKey(
        User, related_name='post_user', on_delete=models.CASCADE)
    description = models.CharField(max_length=254)
    image = models.ImageField(upload_to=image_filename,
                              validators=[image_size_validate], blank=True)
    video = models.FileField(upload_to=video_filename, validators=[
                             video_size_validate, FileExtensionValidator(['mp4'])], blank=True)
    post_type = models.CharField(max_length=20,
                                 choices=PostType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.description}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

# Like model


class Like(models.Model):

    user = models.ForeignKey(
        User, related_name='like_user', on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='like_post', on_delete=models.CASCADE)

    def __ste__(self):
        return f'{self.user}-{self.post}'

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

# Comment model


class Comment(models.Model):

    user = models.ForeignKey(
        User, related_name='comment_user', on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='comment_post', on_delete=models.CASCADE)
    comment = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.comment}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
