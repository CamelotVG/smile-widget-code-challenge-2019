import datetime

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import ProductPrice, Product, GiftCard
from products.serializers import ProductSerializer


class ProductPriceView(APIView):
    def get(self, request):
        product_code = request.query_params.get('productCode')
        date = request.query_params.get('date')
        gift_card_code = request.query_params.get('giftCardCode')

        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValidationError('Incorrect date format, should be YYYY-MM-DD.')

        product = Product.objects.filter(code=product_code)
        if not product:
            raise NotFound(detail='Product not found.')

        product_data = ProductSerializer(product.first()).data

        product_price = ProductPrice.objects.filter(
            product=product_data['id'], date_start__lte=date,
        ).order_by('-date_start')

        if product_price.filter(date_end__gte=date):
            product_price = product_price.filter(date_end__gte=date).first()
        else:
            product_price = product_price.filter(date_end=None).first()

        if product_price:
            product_data['price'] = product_price.price

        if gift_card_code:
            gift_card = GiftCard.objects.filter(code=gift_card_code).first()
            if not gift_card:
                raise NotFound(detail='Gift Card not found.')
            new_price = product_data['price'] - gift_card.amount
            product_data['price'] = new_price if new_price > 0 else 0

        return Response(product_data)
