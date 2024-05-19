from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *


def home(request):
    products = Product.objects.filter(archived=False)
    product_count = products.count()

    product_has_bids = []

    for product in products:
        highest_bid = product.bids.aggregate(Max('amount'))['amount__max']
        product_has_bids.append({
            'product': product,
            'highest_bid': highest_bid if highest_bid is not None else 0,
        })

    context = {
        'product_count': product_count,
        'product_has_bids': product_has_bids,
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


def list_product(request):
    if request.method == 'POST':
        form = ListProduct(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('home')
    else:
        form = ListProduct()

    context = {'form': form}
    return render(request, 'product/list_product.html', context)


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


def user_bids(request, pk):
    user = get_object_or_404(User, id=pk)
    bids = user.bids.all()

    context = {'bids': bids}

    return render(request, 'user/user_bids.html', context)


def user_listings(request, pk):
    user = get_object_or_404(User, id=pk)
    listings = Product.objects.filter(seller=user, archived=False)

    context = {'listings': listings}

    return render(request, 'user/user_listings.html', context)


def archive_listing(request, pk):
    listing = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        form = ArchiveListingForm(request.POST)
        if form.is_valid():
            if request.user == listing.seller:
                listing.archived = True
                listing.save()
            return redirect('user-listings', pk=request.user.pk)
    else:
        form = ArchiveListingForm()

    return render(request, 'user/archive_listing.html', {'form': form, 'listing': listing})