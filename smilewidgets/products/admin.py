from django.contrib import admin
from .models import Product, GiftCard, ProductPrice

# Register your models here.
admin.site.register(Product)
admin.site.register(GiftCard)
admin.site.register(ProductPrice)
