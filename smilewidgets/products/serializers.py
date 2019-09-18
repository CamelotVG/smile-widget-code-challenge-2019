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
            raise ValidationError(f"Product with code '{code}' doesn't exist")

    def validate_giftCardCode(self, code):
        try:
            gift_card = GiftCard.objects.get(code=code)
            return gift_card
        except GiftCard.DoesNotExist:
            raise ValidationError(f"Gift card with code '{code}' doesn't exist")
