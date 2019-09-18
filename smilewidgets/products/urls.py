from django.urls import path, include

from products import views

api_urlpatterns = [
    path('get-price', views.get_price, name='get_product_price')
]

urlpatterns = [
    path('api/', include(api_urlpatterns))
]
