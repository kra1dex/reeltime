# Generated by Django 4.2 on 2023-06-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='movies.genre'),
        ),
    ]