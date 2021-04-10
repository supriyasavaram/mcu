from django.shortcuts import render
from .models import MovieDetails
from .models import AccountDetails

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def movies(request):
    all_movies = MovieDetails.objects.all()
    context = {
        'movies':all_movies
    }
    return render(request, 'movies.html',context)

def reviews(request):
    return render(request, 'reviews.html')

def profile(request):
    return render(request, 'profile.html')

def register(request):
    if request.method == 'POST':
            if request.POST.get('username') and request.POST.get('password'):
                post=AccountDetails()
                post.username= request.POST.get('username')
                post.password= request.POST.get('password')
                post.save()
                
                return render(request, 'register.html')  

    else:
        return render(request, 'register.html')

def login(request):
    # all_accounts = AccountDetails.objects.all()
    # context = {
    #     'accounts':all_accounts
    # }
    if request.method == 'POST':
            if AccountDetails.objects.filter(username=request.POST['username'], password=request.POST['password']).exists():
                print("hello")
                return render(request, 'base.html')  
            else:
                return render(request, 'login.html')
            
            

    else:
        return render(request, 'login.html')