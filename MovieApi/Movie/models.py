from django.db import models

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    director = models.CharField(max_length=100)