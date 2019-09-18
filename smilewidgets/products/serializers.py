from django.utils.dateparse import parse_date

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import GiftCard, Product


class ProductPriceSerializer(serializers.Serializer):
    date = serializers.DateField()
    product_code = serializers.CharField(max_length=10)
    gift_code = serializers.CharField(max_length=30, required=False)

    def validate_gift_code(self, code):
        try:
            gift_card = GiftCard.objects.get(code__iexact=code)
        except GiftCard.DoesNotExist:
            raise ValidationError('Wrong gift card code.')

        date = parse_date(self.initial_data['date'])
        if gift_card.date_start >= date:
            raise ValidationError('Wrong date provided for gift card.')
        elif gift_card.date_end is not None and gift_card.date_end < date:
            raise ValidationError('Gift card already expired.')

        return gift_card

    def validate_product_code(self, code):
        try:
            product = Product.objects.get(code__iexact=code)
            return product
        except Product.DoesNotExist:
            raise ValidationError('Wrong product code.')
