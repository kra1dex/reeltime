# Generated by Django 4.2 on 2023-05-08 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0003_usermovierelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner_movies', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movie',
            name='spectators',
            field=models.ManyToManyField(related_name='spectators_movies', through='movies.UserMovieRelation', to=settings.AUTH_USER_MODEL),
        ),
    ]
