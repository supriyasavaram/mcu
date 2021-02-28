from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('movies', views.movies, name='movies'),
    path('reviews', views.reviews, name='reviews'),
    path('profile', views.profile, name='profile'),
]