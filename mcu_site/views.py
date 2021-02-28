from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def movies(request):
    return render(request, 'movies.html')

def reviews(request):
    return render(request, 'reviews.html')

def profile(request):
    return render(request, 'profile.html')