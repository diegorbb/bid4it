from django.db import models


class Product(models.Model):
    # seller =
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    image = models.ImageField(default="No_image_available.png")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    