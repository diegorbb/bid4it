from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
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


# def product_page(request, pk):
#     product = get_object_or_404(Product, id=pk)

    
#     bids_count = product.bids.count()
#     highest_bid = product.bids.aggregate(Max('amount'))['amount__max']

#     highest_bid_obj = None
#     if highest_bid is not None:
#         highest_bid_obj = product.bids.filter(amount=highest_bid).first()

#     context = {
#         'product': product,
#         'highest_bid': highest_bid_obj,
#         'bids_count': bids_count,
#     }

#     return render(request, 'product/product.html', context)

def product_page(request, pk):
    product = get_object_or_404(Product, id=pk)
    bids = product.bids.all().order_by('-amount')
    bids_count = product.bids.count()
    highest_bid = bids.first().amount if bids.exists() else None
    starting_price = product.starting_price

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['amount']
            min_bid = starting_price if highest_bid is None else highest_bid + Decimal('2.00')

            if bid < min_bid:
                messages.error(request, f'Your bid must be at least £{min_bid}.')
            else:
                new_bid = Bid(user=request.user, item=product, amount=bid)
                new_bid.save()
                messages.success(request, 'Your bid has been placed successfully!')
                return redirect('product-page', pk=pk)
    else:
        form = BidForm()

    context = {
        'product': product,
        'bids': bids,
        'bids_count': bids_count,
        'highest_bid': highest_bid,
        'starting_price': starting_price,
        'form': form,
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
            messages.error(request, 'User does not exist, try again!')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
    
    context = {'page': page}
    return render(request, 'auth/login_register.html', context)


def register_page(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  # Set the email as the username
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        form = MyUserCreationForm()
    
    return render(request, 'auth/login_register.html', {'form': form})


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


def edit_listing(request, pk):

    listing = Product.objects.get(id=pk)
    form = ListingForm(instance=listing)

    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('user-listings', pk=request.user.pk)
    
    context = {'form': form}

    return render(request, 'user/edit_listing.html', context)