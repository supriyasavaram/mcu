
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Movie, Review
from .models import Review
from .forms import CreateReviewForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Avg
from django.db import connection
import json
from django.http import HttpResponse
from django.core import serializers
import datetime
import csv


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
#all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie')

def stars_reviews(revs):
    star_list=[]
    for rev in revs:
        star_list.append( format_stars(rev.stars) )
    return star_list

def calculate_stars(mvs):
    all_reviews = Review.objects.raw('SELECT * FROM mcu_site_review')
    star_list=[]
    temp=0
    counter=0
    for movi in mvs:
        for rev in all_reviews:
            #print(movi)
            #print('hello')
            #print(rev.title.title)
            if movi.title==rev.title.title:
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
    sortby = None
    if request.method == "POST":
        sortby = request.POST.get('sortby')
    if(sortby is not None):
        print(sortby)
        if(sortby == "yeardesc"):
            all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY year DESC')
        elif(sortby == "sortaz"):
            all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY title ASC')
        elif(sortby == "sortza"):
            all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY title DESC')
        else: 
            all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY year ASC')
    else: 
            all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY year ASC')
    #all_movies = Movie.objects.all()
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT * FROM mcu_site_movie ORDER BY year ASC')
    #     columns = cursor.description
    #     all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT * FROM mcu_site_characterplayed')
    #     rows = cursor.description
    #     all_people= [{rows[index][0]:row for index, row in enumerate(value)} for value in cursor.fetchall()]
    zipstuff=zip(all_movies,calculate_stars(all_movies))
    context = {
        'movies': zipstuff,
        #'stars': calculate_stars(all_movies) #format_stars(4.5)
    }
    return render(request, 'movies.html', context)

def search(request):
    if request.method == "POST":
        searchquery = request.POST.get('searchquery', None)
    context = {
        'search': searchquery
    }
    if(searchquery is not None and len(searchquery)>0):
        s='%'+searchquery+'%'
        all_movies = Movie.objects.raw("SELECT * FROM mcu_site_movie WHERE title LIKE %s", [s])
        #with connection.cursor() as cursor:
        #    s='%'+searchquery+'%'
        #    cursor.execute("SELECT * FROM mcu_site_movie WHERE title LIKE %s", [s]) # lol sql injection here? yike
        #    columns = cursor.description
        #    all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        if(len(all_movies)>0):
            zipstuff=zip(all_movies,calculate_stars(all_movies))
            print(zipstuff)
            context = {
                'movies': zipstuff,
                'search': searchquery,
            }
    return render(request, 'movies.html', context)

def reviews(request, m_title=None):
    if request.method == "POST":
        title = request.POST.get('delete_review', None)
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM mcu_site_review WHERE author_id=%s AND title_id=%s', [request.user.id, title])

    #all_reviews = Review.objects.all()
    if m_title is None:
        movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s', [request.user.id])
        #movie = Movie.objects.raw('SELECT id, title, year FROM mcu_site_movie WHERE id=%s LIMIT 1', [m_id])[0]

        zipstuff=zip(movie_reviews,stars_reviews(movie_reviews))
        context = {
            'curr_reviews':movie_reviews,
            'reviews': zipstuff,
        }
        #all_reviews = Review.objects.raw('SELECT * FROM mcu_site_review')
        #zipstuff=zip(all_reviews,stars_reviews(all_reviews))
        #context = {
        #    'reviews': zipstuff
        #}
    else:
        movie_reviews = Review.objects.raw("SELECT * FROM mcu_site_review WHERE title_id=%s", [m_title])
        #movie = Movie.objects.raw('SELECT id, title, year FROM mcu_site_movie WHERE id=%s LIMIT 1', [m_id])[0] 
        with connection.cursor() as cursor:
            #m_title = "'"+m_title+"'"
            #print(m_title)
            cursor.execute("SELECT title, year FROM mcu_site_movie WHERE title=%s LIMIT 1", [m_title])
            columns = cursor.description
            movie = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            movie = movie[0]
        zipstuff=zip(movie_reviews,stars_reviews(movie_reviews))
        context = {
            'curr_reviews':movie_reviews,
            'reviews': zipstuff,
            'movie': movie,
        }
    return render(request, 'reviews.html', context)


def submit_review(request, m_title=None):
    #results = Movie.objects.all()
    movie = None
    if m_title is not None:
        #movie = Movie.objects.raw('SELECT * FROM mcu_site_movie WHERE id=%s', [m_id])[0]
        #results = Movie.objects.raw('SELECT * FROM mcu_site_movie WHERE NOT id=%s', [m_id])
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM mcu_site_movie WHERE title=%s', [m_title])
            columns = cursor.description
            movie = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            movie = movie[0]

            cursor.execute('SELECT * FROM mcu_site_movie WHERE NOT title=%s', [m_title])
            columns = cursor.description
            results = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]

            #form = CreateReviewForm(initial={'title':m_title, 'stars': 1,'review_text':"blah blah",'author':request.user.id })
    else:
        #results = Movie.objects.raw('SELECT * FROM mcu_site_movie')
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM mcu_site_movie')
            columns = cursor.description
            results = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    #context = {'error': ''}
    if request.method == "POST":

        form = CreateReviewForm(request.POST)
        if form.is_valid():
            #review = Review.objects.raw('SELECT * FROM mcu_site_review WHERE id=%s AND title_id=%s', [request.user.id, form.cleaned_data.get('title')])
            review = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s AND title_id=%s;', [request.user.id, form.data.get('title')])
            if (len(review)>0):
                # feels both roundabout AND sketchy, but it seems to work. Does an UPDATE instead of an INSERT if the review already exists.
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE mcu_site_review SET stars=%s, review_text=%s WHERE author_id=%s AND title_id=%s', [form.cleaned_data.get('stars'),  form.cleaned_data.get('review_text'), request.user.id, form.data.get('title')])
            else:
                # form.title=form.cleaned_data.get('movie_title')
                # form.stars = form.cleaned_data.get('stars')
                # form.review_text = form.cleaned_data.get('review_text')
                # form.id=request.user.id
                form.save()
                #with connection.cursor() as cursor:
                #    cursor.execute("INSERT INTO mcu_site_review (id,stars,date_written,review_text,author_id,title_id) VALUES (%s,%s,'%s','%s',%s,'%s')", [5, form.cleaned_data.get('stars'), datetime.now(), form.cleaned_data('review_text'), request.user.id, form.data.get('title')] )
                    #cursor.execute('INSERT mcu_site_review SET stars=%s, review_text=%s WHERE author_id=%s AND title_id=%s', [form.cleaned_data.get('stars'), form.cleaned_data.get('review_text'), request.user.id, form.data.get('title')])
                

            context = {'error': 'created review'}
            print("form made")
        else:
            print("failed")
            context = {'form': form}
    return render(request, 'submit_review.html', {"movies": results, "movie":movie})

def profile(request):
    if request.method == "POST":
        title = request.POST.get('delete_review', None)
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM mcu_site_review WHERE author_id=%s AND title_id=%s', [request.user.id, title])
    #all_reviews = Review.objects.all()
    user_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s', [request.user.id])
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(id) FROM mcu_site_review WHERE author_id=%s', [request.user.id])
        reviews_count = cursor.fetchone()[0] #this can be done easily because of Django html builtins, but using SQL seems more appropriate
    #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s', [request.user.id])
    #movie = Movie.objects.raw('SELECT id, title, year FROM mcu_site_movie WHERE id=%s LIMIT 1', [m_id])[0] 
        
    zipstuff=zip(user_reviews,stars_reviews(user_reviews))
    context = {
        'reviews': zipstuff
        # 'reviews_count': reviews_count,
        
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


def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Movie_database'+str(datetime.datetime.now())+'.csv'

    writer=csv.writer(response)
    all_movies = []
    string=""
    if request.method == "POST":
        print("hello")
        string = request.POST.get('sql')

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM mcu_site_'+string)
        columns = cursor.description
        all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    
    header_list=[]
    for header in all_movies[0].keys():
        header_list.append(header.upper())
    writer.writerow(header_list)
    blank_list=[]
    for mov in all_movies:
        
        for thing in mov.values():
            blank_list.append(thing)
        writer.writerow(blank_list)
        blank_list=[]
    return response
