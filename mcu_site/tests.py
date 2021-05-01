from django.test import TestCase, Client
from .models import *
from .forms import *

class ReviewTest(TestCase):
    def test_standardReview(self):
        form = CreateReviewForm(data = {
            'title': 'Iron Man',
            'stars': '4',
            'review_text': 'Iron man good',
            'author': 'Me',
        })
        self.assertTrue(form.is_valid())
    def test_wrongReview(self):
        form = CreateReviewForm(data = {
            'title': 'Iron Man',
            'stars': '-1',
            'review_text': 'Iron man good',
            'author': 'Me',
        })
        self.assertFalse(form.is_valid())
    def test_standardReview(self):
        form = CreateReviewForm(data = {
            'title': 'Guardians of the Galaxy',
            'stars': '0',
            'review_text': 'nostalgia go brrr',
            'author': 'Me',
        })
        self.assertTrue(form.is_valid())
    def test_blankReview(self):
        form = CreateReviewForm(data = {
            'title': '',
            'stars': '4',
            'review_text': 'Iron man good',
            'author': 'Me',
        })
        self.assertFalse(form.is_valid())
class UserTest(TestCase):
    def test_standardUser(self):
        form = UserCreationForm(data = {
            'first_name': 'Tim',
            'last_name': 'Nigro',
            'username': 'tnigro',
            'email': 'tjn5hb@virginia.edu',
            'password1': 'password',
            'password2': 'lol',
        })
        self.assertTrue(form.is_valid())
    def test_invalidUser(self):
        form = UserCreationForm(data = {
            'first_name': 'Tim',
            'last_name': 'Nigro',
            'username': '',
            'email': 'tjn5hb@virginia.edu',
            'password1': 'password',
            'password2': 'lol',
        })
        self.assertFalse(form.is_valid())