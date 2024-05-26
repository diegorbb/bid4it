from django.contrib import admin
from .models import Product, User, Bid, Category

admin.site.register(Product)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Category)