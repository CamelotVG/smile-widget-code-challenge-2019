from rest_framework import generics
from rest_framework.response import Response

from products.models import ProductPrice, GiftCard, Product
from products.serializers import ProductPriceSerializer


class ProductPriceView(generics.GenericAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_prices = self.get_queryset()

        product_price = product_prices.filter(
            date_start__lte=serializer.validated_data.get('date'),
            date_end__gte=serializer.validated_data.get('date')) \
            .filter(product__code=serializer.validated_data.get('productCode')).first()

        if product_price is not None:
            price = product_price.price
            if serializer.validated_data.get('giftCardCode') is not None:
                gift_card = GiftCard.objects.get(code=serializer.validated_data.get('giftCardCode'))
                price -= gift_card.amount
        else:
            price = Product.objects.get(code=serializer.validated_data.get('productCode')).price

        return Response({'price': price})
