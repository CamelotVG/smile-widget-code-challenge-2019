from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductPriceSerializer
from .models import Product


class GetPricesEndpoint(APIView):
    def get(self, request):
        product_code = request.query_params.get('product_code')
        date = parse_date(request.query_params.get('date'))
        gift_code = request.query_params.get('gift_code')

        if not date:
            raise ValidationError({'date': 'Wrong format of the date.'})

        request_serializer = ProductPriceSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)

        product = Product.objects.get(code__iexact=product_code)
        price = product.get_price(date, product_code, gift_code)

        return Response(price)
