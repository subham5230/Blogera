from django.db import models

# Create your models here.

PRIORITY = [
    ('H', "High"),
    ('M', "Medium"),
    ('L', "Low"),
]

class Question(models.Model):
    title = models.CharField(max_length=60)
    question = models.CharField(max_length=400)
    priority = models.CharField(max_length=1, choices=PRIORITY)

    def __str__(self):
        return self.title