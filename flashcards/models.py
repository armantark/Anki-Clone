from django.db import models

# Create your models here.
from django.db import models


class Word(models.Model):
    word = models.CharField(max_length=100)
    definition = models.TextField()
    bin = models.PositiveIntegerField(default=0)
    next_review = models.DateTimeField(null=True, blank=True)
    incorrect_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.word
