from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import ForeignKey


# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

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
    category = models.CharField(max_length=50)
    cost = models.FloatField(validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Listing of {self.product_name} by {self.user} in {self.category} category"

class ProductImages(models.Model):
    Listing = ForeignKey(Listing, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='listing/images/')
