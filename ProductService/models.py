from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import ForeignKey


# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username

      
class ProductCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Listing(models.Model):
    user = ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='listings')
    product_name = models.CharField(max_length=100)
    product_desc = models.TextField(default="", blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='listings')
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Listing of {self.product_name} by {self.user} in {self.category} category"


def get_image_upload_path(instance, filename):
    return f'listing/images/{instance.listing.id}/{filename}'

class ProductImages(models.Model):
    listing = ForeignKey(Listing, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to=get_image_upload_path)
