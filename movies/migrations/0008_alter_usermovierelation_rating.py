# Generated by Django 4.2 on 2023-05-10 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_alter_movie_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermovierelation',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Bad'), (2, 'Normal'), (3, 'Good'), (4, 'Fine'), (5, 'Incredible')], null=True),
        ),
    ]