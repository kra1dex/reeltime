from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Director(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    biography = models.CharField(max_length=500)

    class Meta:
        constraints = [UniqueConstraint(fields=['name', 'surname'], name='unique_name_surname')]

    def __str__(self):
        return f'ID: {self.id} | {self.name} {self.surname}'


class Movie(models.Model):
    STATUS = [
        ('publish', 'publish'),
        ('archive', 'archive'),
    ]

    status = models.CharField(choices=STATUS, default='archive', max_length=7)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    directors = models.ManyToManyField(Director)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    likes = models.PositiveIntegerField(default=0, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owner_movies')
    spectators = models.ManyToManyField(User, through='UserMovieRelation', related_name='spectators_movies')

    def __str__(self):
        return f'ID: {self.id} | {self.title}'


class UserMovieRelation(models.Model):
    RATING = [
        (1, 'Bad'),
        (2, 'Normal'),
        (3, 'Good'),
        (4, 'Fine'),
        (5, 'Incredible')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING, null=True)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'ID: {self.id} | {self.movie.title}. {self.user.username}'
