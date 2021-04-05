from django.db import models

# Create your models here.

class Movie(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    synopsis = models.CharField(max_length=2048)
    date = models.DateField()

