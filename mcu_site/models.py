from django.db import models
from django.db import connections
# Create your models here.

#Movie Details from phpMyAdmin
class MovieDetails(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    director = models.CharField(max_length=2048)
    year = models.IntegerField()
    
           
