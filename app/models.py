from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    starting_price = models.FloatField(null=True, blank=True)
    image = models.ImageField(default="No_image_available.png")
    created = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"User: {self.user}, Item: {self.item}, Amount: {self.amount}"

    