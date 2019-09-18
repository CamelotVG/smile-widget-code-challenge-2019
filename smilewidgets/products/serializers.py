from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import Product, GiftCard


class RequestPriceSerializer(serializers.Serializer):
    productCode = serializers.CharField(max_length=10)
    date = serializers.DateField()
    giftCardCode = serializers.CharField(max_length=30, required=False)

    def validate_productCode(self, code):
        try:
            product = Product.objects.get(code=code)
            return product
        except Product.DoesNotExist:
            raise ValidationError("Product with code '{}' doesn't exist".format(code))

    def validate_giftCardCode(self, code):
        try:
            gift_card = GiftCard.objects.get(code=code)
            return gift_card
        except GiftCard.DoesNotExist:
            raise ValidationError("Gift card with code '{}' doesn't exist".format(code))
