from django.urls import path

from products.views import GetPriceViewSet

urlpatterns = [
    path('', GetPriceViewSet.as_view(), name='get-price'),
]
