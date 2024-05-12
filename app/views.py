from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *


def home(request):
    products = Product.objects.all()
    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'app/home.html', context)


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

    try:
        user = User.objects.get(email=email)
    except:
        message.error(request, 'User does not exist, try again!')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        message.error(request, 'Invalid username or password')
    
    context = {'page': page}
    return render(request, 'app/auth/login_register.html', context)


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
        
    return render(request, 'app/auth/login_register.hmtl')


def logout_user(request):
    logout(request)
    return redirect('home')