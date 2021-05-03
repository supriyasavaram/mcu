
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Movie, Person
#from .models import Review
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

def stars_reviews(revs):
    star_list=[]
    for rev in revs:
        star_list.append( format_stars(rev['stars']) ) #making this work with dict, so that we can separate out Reviews model...
    return star_list

def calculate_stars(mvs):
    star_list=[]
    temp=0
    counter=0
    for movi in mvs:
            #print(movi)
            #print('hello')
            #print(rev.title.title)
            temp=movi['stars']
            star_list.append(format_stars(temp))
    return star_list 

def add_stars_lists(mvs):
    star_list=[]
    for movi in mvs:
        temp=movi['stars']
        movi['stars'] = format_stars(temp)
    return mvs

def add_director_lists(mvs):
    star_list=[]
    for m in mvs:
        mtitle = m.get('title')
        with connection.cursor() as cursor:
            cursor.execute('SELECT first_name, last_name FROM mcu_site_person NATURAL JOIN (SELECT person_id as id, movie_title FROM mcu_site_directs WHERE movie_title=%s) AS T', [mtitle])
            columns = cursor.description
            directors = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        m['dirs'] = directors
    return mvs

def add_appears_lists(characters):
    for c in characters:
        cname = c.get('character_name')
        with connection.cursor() as cursor:
            cursor.execute('SELECT movie_title, year FROM mcu_site_appearsin NATURAL JOIN (SELECT title AS movie_title, year FROM mcu_site_movie) AS T WHERE character_name=%s ORDER BY year ASC', [cname])
            columns = cursor.description
            appearsin = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        c['appearsin'] = appearsin
    return characters

def movies(request):
    sortby = None
    if request.method == "POST":
        sortby = request.POST.get('sortby')
    if(sortby is not None):
        print(sortby)
        if(sortby == "yeardesc"):
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mcu_site_movie ORDER BY year DESC')
                columns = cursor.description
                all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY year DESC')
        elif(sortby == "ratingdesc"):
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mcu_site_movie ORDER BY stars DESC')
                columns = cursor.description
                all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY stars DESC')
        elif(sortby == "ratingasc"):
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mcu_site_movie ORDER BY stars ASC')
                columns = cursor.description
                all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY stars ASC')
        elif(sortby == "sortaz"):
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mcu_site_movie ORDER BY title ASC')
                columns = cursor.description
                all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY title ASC')
        elif(sortby == "sortza"):
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mcu_site_movie ORDER BY title DESC')
                columns = cursor.description
                all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY title DESC')
        else: 
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mcu_site_movie ORDER BY year ASC')
                columns = cursor.description
                all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY year ASC')
    else:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM mcu_site_movie ORDER BY year ASC')
            columns = cursor.description
            all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        #all_movies = Movie.objects.raw('SELECT * FROM mcu_site_movie ORDER BY year ASC')
    #all_movies = Movie.objects.all()
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT * FROM mcu_site_movie ORDER BY year ASC')
    #     columns = cursor.description
    #     all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT * FROM mcu_site_characterplayed')
    #     rows = cursor.description
    #     all_people= [{rows[index][0]:row for index, row in enumerate(value)} for value in cursor.fetchall()]
    all_movies = add_director_lists(all_movies)
    zipstuff=zip(all_movies,calculate_stars(all_movies))
    context = {
        'movies': zipstuff,
        'sortable': True,
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
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM mcu_site_movie WHERE title LIKE %s', [s])
            columns = cursor.description
            all_movies= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
        #all_movies = Movie.objects.raw("SELECT * FROM mcu_site_movie WHERE title LIKE %s", [s])

        if(len(all_movies)>0):
            zipstuff=zip(all_movies,calculate_stars(all_movies))
            print(zipstuff)
            context = {
                'movies': zipstuff,
                'search': searchquery,
            }
    return render(request, 'movies.html', context)

def reviews(request, m_title=None):
    movie_reviews=None
    if request.method == "POST":    # deleting a review written by you
        title = request.POST.get('delete_review', None)
        author = request.POST.get('delete_user', None)
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM mcu_site_review WHERE author_id=%s AND title_id=%s', [author, title])
        sortby = request.POST.get('sortby', None)
        if(sortby is not None and m_title is None):
            if(sortby == "ratingasc"):
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T ORDER BY stars ASC')
                    columns = cursor.description
                    movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review ORDER BY stars ASC')
            elif(sortby == "ratingdesc"):
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T ORDER BY stars DESC')
                    columns = cursor.description
                    movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review ORDER BY stars DESC')
            elif(sortby == "dateasc"):
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T ORDER BY date_written ASC')
                    columns = cursor.description
                    movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review ORDER BY date_written ASC')
            elif(sortby == "datedesc"):
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T ORDER BY date_written DESC')
                    columns = cursor.description
                    movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review ORDER BY date_written DESC')
        elif(sortby is not None):
            if(sortby == "ratingasc"):
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T WHERE title_id=%s ORDER BY stars ASC', [m_title])
                    columns = cursor.description
                    movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE title_id=%s ORDER BY stars ASC', [m_title])
            elif(sortby == "ratingdesc"):
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T WHERE title_id=%s ORDER BY stars DESC', [m_title])
                    columns = cursor.description
                    movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE title_id=%s ORDER BY stars DESC', [m_title])
            elif(sortby == "dateasc"):
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T WHERE title_id=%s ORDER BY date_written ASC', [m_title])
                    columns = cursor.description
                    movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE title_id=%s ORDER BY date_written ASC', [m_title])
            elif(sortby == "datedesc"):
                with connection.cursor() as cursor:
                    cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T WHERE title_id=%s ORDER BY date_written DESC', [m_title])
                    columns = cursor.description
                    movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE title_id=%s ORDER BY date_written DESC', [m_title])
    #all_reviews = Review.objects.all()
    if m_title is None:
        if(movie_reviews is None):
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T ORDER BY date_written DESC')
                columns = cursor.description
                movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review ORDER BY date_written DESC')
        #movie = Movie.objects.raw('SELECT id, title, year FROM mcu_site_movie WHERE id=%s LIMIT 1', [m_id])[0]

        zipstuff=zip(movie_reviews,stars_reviews(movie_reviews))
        context = {
            'curr_reviews':movie_reviews,
            'reviews': zipstuff,
        }
    else:
        if(movie_reviews is None):
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T WHERE title_id=%s ORDER BY date_written DESC', [m_title])
                columns = cursor.description
                movie_reviews= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE title_id=%s ORDER BY date_written DESC', [m_title])
        #movie = Movie.objects.raw('SELECT id, title, year FROM mcu_site_movie WHERE id=%s LIMIT 1', [m_id])[0] 
        with connection.cursor() as cursor:
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
    context=dict()
    movie = None
    #context = {'error': ''}
    if request.method == "POST":
        form = CreateReviewForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM mcu_site_review WHERE author_id=%s AND title_id=%s;', [request.user.id, form.data.get('title')])
                columns = cursor.description
                review= [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #review = Review.objects.raw('SELECT * FROM mcu_site_review WHERE id=%s AND title_id=%s', [request.user.id, form.cleaned_data.get('title')])
            #review = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s AND title_id=%s;', [request.user.id, form.data.get('title')])
            if (len(review)>0): # feels both roundabout AND sketchy, works. UPDATE instead of an INSERT if review already exists.
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE mcu_site_review SET stars=%s, review_text=%s WHERE author_id=%s AND title_id=%s', [form.cleaned_data.get('stars'),  form.cleaned_data.get('review_text'), request.user.id, form.data.get('title')])
            else:
                obj = form.save(commit=False)
                try:
                    obj.save()
                except:
                    context['error'] = 'You can not write a review for a movie that is not out yet!'
        else:
            context ['error']= 'Please make sure all fields are filled!'
            print("invalid input")
            
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

            cursor.execute('SELECT * FROM mcu_site_review WHERE author_id=%s AND title_id=%s LIMIT 1', [request.user.id, m_title])
            columns = cursor.description
            myreview = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #myreview = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s AND title_id=%s LIMIT 1', [request.user.id, m_title])
            if(len(myreview)>0):
                context["oldreview"] = myreview[0]
    else:
        #results = Movie.objects.raw('SELECT * FROM mcu_site_movie')
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM mcu_site_movie')
            columns = cursor.description
            results = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    
    context["movies"] = results
    context["movie"] = movie
    return render(request, 'submit_review.html', context)

def profile(request):
    if request.method == "POST":
        title = request.POST.get('delete_review', None)
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM mcu_site_review WHERE author_id=%s AND title_id=%s', [request.user.id, title])
    with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM mcu_site_review NATURAL JOIN (SELECT username AS author, id AS author_id FROM auth_user) AS T WHERE author_id=%s', [request.user.id])
            columns = cursor.description
            user_reviews = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    #all_reviews = Review.objects.all()
    #user_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s', [request.user.id])
    
    with connection.cursor() as cursor:
        cursor.execute('SELECT COUNT(title_id) FROM mcu_site_review WHERE author_id=%s', [request.user.id])
        reviews_count = cursor.fetchone()[0] #this can be done easily because of Django html builtins, but using SQL seems more appropriate
    #movie_reviews = Review.objects.raw('SELECT * FROM mcu_site_review WHERE author_id=%s', [request.user.id])
    #movie = Movie.objects.raw('SELECT id, title, year FROM mcu_site_movie WHERE id=%s LIMIT 1', [m_id])[0] 
        
    zipstuff=zip(user_reviews,stars_reviews(user_reviews))
    context = {
        'reviews': zipstuff,
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
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            form.save()
            # messages.success(request, "Account created!")
            user = authenticate(request, username=user_name, password=password)
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

def people(request, p_id=None):
    if(p_id is not None):
        context = dict()
        p = Person.objects.raw('SELECT * FROM mcu_site_person WHERE id=%s',[p_id])[0]
        context['person'] = p
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM mcu_site_movie WHERE title in ( SELECT movie_title AS title FROM mcu_site_directs WHERE person_id=%s)', [p_id])
            
            #cursor.execute('SELECT * FROM mcu_site_movie WHERE title in ( SELECT movie_title AS title FROM mcu_site_directs NATURAL JOIN (SELECT id AS director_id, num_directed, person_id FROM mcu_site_director) AS T WHERE person_id=%s)', [p_id])
            columns = cursor.description
            movies_directed=[{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            if(len(movies_directed)>0):
                context['directed'] = add_stars_lists(movies_directed)
                
                cursor.execute('SELECT num_directed FROM mcu_site_director WHERE person_id=%s',[p_id])
                columns = cursor.description
                num_directed=[{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                context['numdirected'] = num_directed[0]

            #cursor.execute('SELECT character_name, alignment FROM mcu_site_actor NATURAL JOIN (SELECT actor_id AS id, character_name FROM mcu_site_plays) AS T WHERE person_id=%s', [p_id])
            cursor.execute('SELECT character_name, alignment FROM mcu_site_character NATURAL JOIN (SELECT character_name FROM mcu_site_plays WHERE person_id=%s) AS T2', [p_id])
            #cursor.execute('SELECT character_name, alignment FROM mcu_site_character NATURAL JOIN (SELECT character_name FROM mcu_site_actor NATURAL JOIN (SELECT actor_id AS id, character_name FROM mcu_site_plays) AS T1 WHERE person_id=%s) AS T2', [p_id])
            columns = cursor.description
            characters_played=[{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            #print(add_appears_lists(characters_played))
            if(len(characters_played)>0):
                context['played'] = add_appears_lists(characters_played)

                cursor.execute('SELECT agency FROM mcu_site_actor WHERE person_id=%s',[p_id])
                columns = cursor.description
                agency=[{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
                agency = agency[0]
                if(len(agency['agency'])>0):
                    context['agency'] = agency[0]
        template = 'person.html'
    else:
        sortby = None
        if request.method == "POST":
            sortby = request.POST.get('sortby')
        if(sortby is not None):
            print(sortby)
            if(sortby == "fndesc"):
                all_actorsdirectors = Person.objects.raw('SELECT * FROM mcu_site_person ORDER BY first_name DESC')
            elif(sortby == "lnasc"):
                all_actorsdirectors = Person.objects.raw('SELECT * FROM mcu_site_person ORDER BY last_name ASC')
            elif(sortby == "lndesc"):
                all_actorsdirectors = Person.objects.raw('SELECT * FROM mcu_site_person ORDER BY last_name DESC')
            elif(sortby == "actors"):
                all_actorsdirectors = Person.objects.raw('SELECT * FROM mcu_site_person WHERE id IN (SELECT person_id AS id FROM mcu_site_actor) ORDER BY first_name ASC')
            elif(sortby == "directors"):
                all_actorsdirectors = Person.objects.raw('SELECT * FROM mcu_site_person WHERE id IN (SELECT person_id AS id FROM mcu_site_director) ORDER BY first_name ASC')
            else: 
                all_actorsdirectors = Person.objects.raw('SELECT * FROM mcu_site_person ORDER BY first_name ASC')
        else: 
            all_actorsdirectors = Person.objects.raw('SELECT * FROM mcu_site_person ORDER BY first_name ASC')
        directors = Person.objects.raw('SELECT * FROM mcu_site_person WHERE id IN (SELECT person_id AS id FROM mcu_site_director)')
        actors = Person.objects.raw('SELECT * FROM mcu_site_person WHERE id IN (SELECT person_id AS id FROM mcu_site_actor)')
        
        template = 'people.html'
        context = {
            'everybody': all_actorsdirectors,
            'directors': directors,
            'actors': actors,
        }
    return render(request, template, context)