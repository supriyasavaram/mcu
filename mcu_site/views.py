from django.shortcuts import render
from .models import Movie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
    return render(request, 'reviews.html')

def profile(request):
    return render(request, 'profile.html')

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

def login(request):
    return render(request, 'login.html')

def reset_password(request):
    return render(request, 'reset_password.html')