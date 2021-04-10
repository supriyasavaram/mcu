from django.db import models
from django.db import connections
# Create your models here.

#Movie Details from phpMyAdmin
class MovieDetails(models.Model):
    #id = models.AutoField(primary_key=True,default="")
    title = models.CharField(max_length=255,default="",editable=False)
    director = models.CharField(max_length=255,default="",editable=False)
    year = models.IntegerField()
    

class AccountDetails(models.Model):
    #id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255,default="",editable=False)
    password = models.CharField(max_length=255,default="",editable=False)
