from django.contrib import admin
from .models import Person, Actor, Director, Movie, CharacterPlayed, Review, Profile, MovieDetails, AccountDetails

admin.site.register(Person)
admin.site.register(Actor)
admin.site.register(Director)

admin.site.register(Movie)
admin.site.register(CharacterPlayed)
admin.site.register(Review)
admin.site.register(MovieDetails)
admin.site.register(AccountDetails)