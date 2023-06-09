# Generated by Django 4.2 on 2023-06-06 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermovierelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(to='movies.director'),
        ),
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
        migrations.AddConstraint(
            model_name='director',
            constraint=models.UniqueConstraint(fields=('name', 'surname'), name='unique_name_surname'),
        ),
    ]