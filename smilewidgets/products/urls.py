from django.urls import path

from .views import ProductPriceView

urlpatterns = [
    path('get-price/', ProductPriceView.as_view(), name='product_price'),
]
