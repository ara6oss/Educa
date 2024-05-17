# Generated by Django 4.2.7 on 2024-05-17 11:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("lessons", "0010_lesson_unsave_alter_lesson_save"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="save",
            field=models.ManyToManyField(
                blank=True,
                related_name="save_playlist",
                to=settings.AUTH_USER_MODEL,
                verbose_name="AddPlaylist",
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="unsave",
            field=models.ManyToManyField(
                blank=True,
                related_name="remove_playlist",
                to=settings.AUTH_USER_MODEL,
                verbose_name="RemovePlaylist",
            ),
        ),
    ]
