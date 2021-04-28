from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Movie,Review
from .forms import CreateReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime

from .forms import CreateUserForm

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
    all_reviews = Review.objects.all()
    context = {
        'reviews':all_reviews
    }
    return render(request, 'reviews.html',context)

def submit_review(request):
    results=Movie.objects.all()
    context={'error':''}
    if request.method == "POST":
        
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            # form.title=form.cleaned_data.get('movie_title')
            # form.stars = form.cleaned_data.get('stars')
            # form.review_text = form.cleaned_data.get('review_text')
            # form.id=request.user.id
            form.save()
            
            context = {'error' : 'created review'}
        else:
            
            context = {'form': form}
    return render(request, 'submit_review.html',{"movies":results})

def profile(request):
    all_reviews = Review.objects.all()
    context = {
        'reviews':all_reviews
    }
    return render(request, 'profile.html',context)

def register(request):
    context = {'error': ''}
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST" and "register" in request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            # messages.success(request, "Account created!")
            user = authenticate(request, username=username, password=password)
            context = {'error' : 'created account'}
        else:
            context = {'form': form}
    return render(request, 'register.html', context)

def signin(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST" and "signin" in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user_auth = authenticate(request, username=username, password=password)
        if user_auth is not None:
            login(request, user_auth)
            return render(request, 'index.html')
        else:
            context['error'] = "Invalid username/password. Please try again."
            # return render(request, 'events/signin.html', context)
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect('index')

def reset_password(request):
    return render(request, 'reset_password.html')