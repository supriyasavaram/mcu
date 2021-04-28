from django.db import models
from django.contrib.auth.models import User
import datetime

class Person(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class Actor(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.person.name

class Director(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.person.name

class Movie(models.Model):
    title = models.CharField(max_length=150)
    synopsis = models.CharField(max_length=2048)
    year = models.CharField(max_length=10)
    runtime = models.CharField(max_length=32)
    actors = models.ManyToManyField(Actor, through='CharacterPlayed', blank=True)
    directors = models.ManyToManyField(Director, blank=True)

    def add_movie(self, title):
        movie = self.create(title=title)
        return movie
    
    def __str__(self):
        return self.title + " " + self.year

class CharacterPlayed(models.Model):
    character_name = models.CharField(max_length=32)
    actor = models.ForeignKey(Actor, on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.actor.person.name + ' as ' + self.character_name + ' in ' + self.movie.title + ' ' + self.movie.year


# class Superhero(models.Model):
#     name = models.CharField(max_length=32)
#     alter_egos = models.CharField(max_length=150)
#     deceased = models.BooleanField()
#     alignment = models.CharField(max_length=150)

class Review(models.Model):
    stars = models.IntegerField()
    date_written = models.DateTimeField(auto_now_add=True)
    review_text = models.TextField(max_length=2048)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # profile_pic = models.ImageField(default="default_pfp.png", upload_to="profile_pics")
    slug = models.SlugField(unique=False, null=True)
    # bio = models.TextField(null=True, blank=True)

    def __str__(self):
       return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)