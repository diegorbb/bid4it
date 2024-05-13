from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *


def home(request):
    products = Product.objects.all()
    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'app/home.html', context)


def product_page(request, pk):
    product = get_object_or_404(Product, id=pk)
    
    bids_count = product.bids.count()
    highest_bid = product.bids.aggregate(Max('amount'))['amount__max']

    highest_bid_obj = None
    if highest_bid is not None:
        highest_bid_obj = product.bids.filter(amount=highest_bid).first()

    context = {
        'product': product,
        'highest_bid': highest_bid_obj,
        'bids_count': bids_count,
    }

    return render(request, 'product/product.html', context)



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
    return render(request, 'auth/login_register.html', context)


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
    return redirect('login')