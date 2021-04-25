from django.contrib import admin
from .models import Person, Actor, Director, Movie, CharacterPlayed, Review, Profile

admin.site.register(Person)
admin.site.register(Actor)
admin.site.register(Director)

admin.site.register(Movie)
admin.site.register(CharacterPlayed)
admin.site.register(Review)
# admin.site.register(Profile)