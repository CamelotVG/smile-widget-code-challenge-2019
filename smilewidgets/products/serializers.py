from rest_framework import serializers
from rest_framework.exceptions import NotFound
from products.models import Product


class ProductPriceSerializer(serializers.Serializer):
    productCode = serializers.CharField(required=True, allow_blank=False)
    date = serializers.DateField(required=True)
    giftCardCode = serializers.CharField(required=False)

    def validate_product_code(self, code):
        try:
            return Product.objects.get(code=code)
        except Product.DoesNotExist:
            raise NotFound('Product does not exist')

