from django.shortcuts import render
from .models import *


def home(request):
    products = Product.objects.all()
    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'app/home.html', context)