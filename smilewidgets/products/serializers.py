from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import Product, GiftCard, ProductPrice


class ProductPriceSerializer(serializers.Serializer):
    product_code = serializers.CharField(max_length=10)
    date = serializers.DateField(format=None)
    gift_card_code = serializers.CharField(max_length=30, required=False, allow_null=True)

    def validate_product_code(self, value):
        try:
            product = Product.objects.get(code=value)
            return "{}_{}".format(product.id, product.price)
        except Product.DoesNotExist:
            raise ValidationError('Wrong product code')

    def validate(self, attrs):
        """
        After validation attrs['gift_card_code'] will store amount of discount if it exists
        :param attrs:
        :return attrs:
        """
        date = attrs.get('date')
        giftcard_code = attrs.get('gift_card_code')

        if giftcard_code:
            try:
                gift_card = GiftCard.objects.get(code=giftcard_code)
            except GiftCard.DoesNotExist:
                raise ValidationError('Wrong gift card code')

            if gift_card.date_start <= date and (gift_card.date_end is None or gift_card.date_end >= date):
                attrs['gift_card_code'] = gift_card.amount
            else:
                raise ValidationError('Gift card has expired')
        return attrs

    def to_representation(self, instance):
        repr_data = super().to_representation(instance)
        date = repr_data.get('date')
        product_id, product_price = repr_data.get('product_code').split('_')
        giftcard_discount = repr_data.get('gift_card_code')
        giftcard_discount = int(giftcard_discount) if giftcard_discount else 0

        try:
            product_price = ProductPrice.objects.filter(Q(start_date__lte=date, end_date__isnull=True, product_id=product_id) |
                                                        Q(start_date__lte=date, end_date__gt=date, product_id=product_id))\
                                                .latest('start_date')
            price = product_price.price - giftcard_discount
        except ProductPrice.DoesNotExist:
            price = int(product_price) - giftcard_discount

        price = 0 if price < 0 else price

        return {'price': price}
