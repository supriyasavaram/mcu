from django.shortcuts import render
from .models import Movie

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def movies(request):
    all_movies = Movie.objects.all()
    context = {
        'movies':all_movies
    }
    return render(request, 'movies.html', context)

def reviews(request):
    return render(request, 'reviews.html')

def profile(request):
    return render(request, 'profile.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def reset_password(request):
    return render(request, 'reset_password.html')