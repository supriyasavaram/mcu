from django.shortcuts import render
from .models import MovieDetails

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def movies(request):
    all_movies = MovieDetails.objects.all()
    context = {
        'movies':all_movies
    }
    return render(request, 'movies.html',context)

def reviews(request):
    return render(request, 'reviews.html')

def profile(request):
    return render(request, 'profile.html')