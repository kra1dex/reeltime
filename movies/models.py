from django.db import models


class Director(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    # biography = models.CharField(max_length=500)

    def __str__(self):
        return f"ID: {self.id} | {self.name} {self.surname}"


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    directors = models.ManyToManyField(Director)

    def __str__(self):
        return f"ID: {self.id} | {self.title}"
