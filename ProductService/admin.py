from django.contrib import admin

from ProductService.models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Listing)
admin.site.register(ProductImages)
admin.site.register(ProductCategory)