import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Review, Movie
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


    
class CreateReviewForm(forms.ModelForm):
    class Meta:
        title=forms.ModelChoiceField(Movie.objects.all())
        author_id=title=forms.ModelChoiceField(User.objects.all())
        model = Review
        fields = ['title','stars','review_text','author']

