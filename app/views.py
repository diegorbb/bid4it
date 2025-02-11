from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max, F, Value, Case, When
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
from .models import *
from .forms import *


def home(request):
    products = Product.objects.filter(archived=False).order_by('-created')[:8]
    product_count = products.count()

    product_has_bids = []

    for product in products:
        highest_bid = product.bids.aggregate(Max('amount'))['amount__max']
        if product.end_date:
            remaining_time = product.end_date - timezone.now()
            days = remaining_time.days
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
        else:
            remaining_time = None
            days = hours = minutes = None
        product_has_bids.append({
            'product': product,
            'highest_bid': highest_bid if highest_bid is not None else 0,
            'remaining_time': remaining_time,
            'days': days,
            'hours': hours,
            'minutes': minutes,
        })

    context = {
        'product_count': product_count,
        'product_has_bids': product_has_bids,
    }
    return render(request, 'app/home.html', context)


def listings(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = Product.objects.filter(category=category, archived=False).order_by('-created')
    else:
        products = Product.objects.filter(archived=False).order_by('-created')
        
    count = products.count()
    product_has_bids = []

    for product in products:
        highest_bid = product.bids.aggregate(Max('amount'))['amount__max']
        starting_price = product.starting_price
        product_has_bids.append({
            'product': product,
            'highest_bid': highest_bid if highest_bid is not None else 0,
            'starting_price': starting_price,
        })

    context = {
        'products': products,
        'product_has_bids': product_has_bids,
        'count': count,
        'category': category if category_id else None,
        'categories': categories,
    }

    return render(request, 'product/listings.html', context)


def product_page(request, pk):
    product = get_object_or_404(Product, id=pk)
    bids = product.bids.all().order_by('-amount')
    bids_count = product.bids.count()
    highest_bid_amount = bids.first().amount if bids.exists() else None
    highest_bid = bids.first() if bids.exists() else None
    starting_price = product.starting_price

    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data['amount']
            min_bid = starting_price if highest_bid_amount is None else highest_bid_amount + Decimal('2.00')

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
        'now': timezone.now(),
    }
    return render(request, 'product/product.html', context)


@login_required(login_url='login')
def list_product(request):
    if request.method == 'POST':
        form = ListProduct(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            duration = int(form.cleaned_data['duration'])
            product.seller = request.user
            product.save()
            product.set_end_date(duration)
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


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def user_bids(request, pk):
    user = get_object_or_404(User, id=pk)
    bids = user.bids.all()

    context = {'bids': bids}

    return render(request, 'user/user_bids.html', context)


@login_required(login_url='login')
def user_listings(request, pk):
    user = get_object_or_404(User, id=pk)
    listings = Product.objects.filter(seller=user, archived=False)
    arch_listings = Product.objects.filter(seller=user, archived=True)

    context = {'listings': listings, 'arch_listings': arch_listings}

    return render(request, 'user/user_listings.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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