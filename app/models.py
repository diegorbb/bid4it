from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Product(models.Model):
    # seller =
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    starting_price = models.FloatField(null=True, blank=True)
    image = models.ImageField(default="No_image_available.png")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    