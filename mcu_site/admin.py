from django.contrib import admin
from .models import MovieDetails
from .models import AccountDetails

# Register your models here.
admin.site.register(MovieDetails)
admin.site.register(AccountDetails)
