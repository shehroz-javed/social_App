# Generated by Django 4.2.3 on 2023-07-14 12:50

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('friend_request', '0003_alter_friendrequest_from_user_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Friend',
            new_name='Friends',
        ),
    ]