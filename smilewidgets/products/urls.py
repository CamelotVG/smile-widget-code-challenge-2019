from django.contrib import admin
from django.urls import path
from products.views import GetPriceView

urlpatterns = [
    path('', GetPriceView.as_view())
]
