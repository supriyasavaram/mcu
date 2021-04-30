
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Movie, Review
from .forms import CreateReviewForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Avg
from django.db import connection
import datetime


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')

def format_stars(num):
    whole = int(num)
    lst = []
    counter = 5
    for i in range(whole):
        lst.append("Whole")
        num -= 1
        counter -= 1
    if .33 < num < .67:
        lst.append("Half")
        counter -= 1
    for i in range(counter):
        lst.append("None")
    return lst

#added to work on fixing stars
all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie')

def stars_reviews(revs):
    star_list=[]
    for rev in revs:
        star_list.append(format_stars(rev.stars))
    return star_list

def calculate_stars(mvs):
    all_reviews = Movie.objects.raw('SELECT * FROM mcu_site_review')
    star_list=[]
    temp=0
    counter=0
    for movi in mvs:
        for rev in all_reviews:
            if movi.id==rev.title_id:
                temp+=rev.stars
                counter+=1
        if counter!=0:
            star_list.append(format_stars(temp/counter))
        else:
            star_list.append(format_stars(0))
        temp=0
        counter=0
    return star_list 
    #all_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE title_id=%s', [m_id])

def movies(request):
    #all_movies = Movie.objects.all()
    all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie')
    zipstuff=zip(all_movies,calculate_stars(all_movies))
    
    context = {
        'movies': zipstuff,
        #'stars': calculate_stars(all_movies) #format_stars(4.5)
    }
    return render(request, 'movies.html', context)


def reviews(request, m_id=None):
    #all_reviews = Review.objects.all()
    if m_id is None:
        all_reviews = Review.objects.raw('SELECT * FROM mcu_site_review')
        zipstuff=zip(all_reviews,stars_reviews(all_reviews))
        context = {
            'reviews': zipstuff
        }
    else:
        movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE title_id=%s', [m_id])
        movie = Movie.objects.raw('SELECT id, title, year FROM mcu_site_movie WHERE id=%s LIMIT 1', [m_id])[0] 
        #with connection.cursor() as cursor:
        #    cursor.execute('SELECT title, year FROM mcu_site_movie WHERE id=%s LIMIT 1', [m_id])
        #    movie = cursor.fetchone() #returns a tuple of the title, year
        #    movie_title = movie[0]
        #    movie_year = movie[1]
        zipstuff=zip(movie_reviews,stars_reviews(movie_reviews))
        context = {
            'curr_reviews':movie_reviews,
            'reviews': zipstuff,
            'movie': movie,
        }
    return render(request, 'reviews.html', context)


def submit_review(request, m_id=None):
    #results = Movie.objects.all()
    movie = None
    if m_id is not None:
        movie = Movie.objects.raw('SELECT * FROM mcu_site_movie WHERE id=%s', [m_id])[0]
        results = Movie.objects.raw('SELECT * FROM mcu_site_movie WHERE NOT id=%s', [m_id])
    else:
        results = Movie.objects.raw('SELECT * FROM mcu_site_movie')
    #context = {'error': ''}
    if request.method == "POST":

        form = CreateReviewForm(request.POST)
        if form.is_valid():
            #review = Review.objects.raw('SELECT * FROM mcu_site_review WHERE id=%s AND title_id=%s', [request.user.id, form.cleaned_data.get('title')])
            review = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s AND title_id=%s;', [request.user.id, form.data.get('title')])
            if (len(review)>0):
                # feels both roundabout AND sketchy, but it seems to work. Does an UPDATE instead of an INSERT if the review already exists.
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE mcu_site_review SET stars=%s, review_text=%s WHERE author_id=%s AND title_id=%s', [form.cleaned_data.get('stars'), form.cleaned_data.get('review_text'), request.user.id, form.data.get('title')])
            else:
                # form.title=form.cleaned_data.get('movie_title')
                # form.stars = form.cleaned_data.get('stars')
                # form.review_text = form.cleaned_data.get('review_text')
                # form.id=request.user.id
                form.save()

            context = {'error': 'created review'}
        else:

            context = {'form': form}
    return render(request, 'submit_review.html', {"movies": results, "movie":movie})


def profile(request):
    #all_reviews = Review.objects.all()
    user_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s', [request.user.id])
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(id) FROM mcu_site_review WHERE author_id=%s', [request.user.id])
        reviews_count = cursor.fetchone()[0] #this can be done easily because of Django html builtins, but using SQL seems more appropriate
    context = {
        'reviews': user_reviews,
        'reviews_count': reviews_count,
    }
    return render(request, 'profile.html', context)


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
            context = {'error': 'created account'}
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

def settings(request):
    if request.method == "POST":

        form = CreateReviewForm(request.POST)
        if form.is_valid():
            # form.title=form.cleaned_data.get('movie_title')
            # form.stars = form.cleaned_data.get('stars')
            # form.review_text = form.cleaned_data.get('review_text')
            # form.id=request.user.id
            form.save()

            context = {'error': 'created review'}
        else:

            context = {'form': form}
    return render(request, 'settings.html')
