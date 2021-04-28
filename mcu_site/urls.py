from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('movies', views.movies, name='movies'),
    path('reviews', views.reviews, name='reviews'),
    path('profile', views.profile, name='profile'),
    path('submit-review', views.submit_review, name='submit_review'),
    path('register', views.register, name='register'),
    path('login', views.signin, name='signin'),
    path('logout', views.signout, name='signout'),
    path('reset-password', views.reset_password, name='reset-password'),
]