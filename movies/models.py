from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"ID: {self.id} | {self.title}"
