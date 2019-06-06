from rest_framework import serializers
from products.models import ProductPrice, Product, GiftCard
from django.db.models import Q

# https://www.django-rest-framework.org/api-guide/serializers/


class ProductPriceSerializer(serializers.Serializer):
    productCode = serializers.CharField(max_length=30)
    date = serializers.DateField()
    giftCardCode = serializers.CharField(max_length=10, required=False)

    def validate(self, instance):
        errors = {}

        result = Product.objects.filter(
            Q(code=instance['productCode'])).first()
        if not result:
            errors['productCode'] = 'Invalid productCode'

        print("Product", result)

        result = ProductPrice.objects \
            .filter(Q(product_code__code=instance['productCode']),
                    Q(start_date__lte=instance['date']),
                    Q(end_date__gte=instance['date'])) \
            .order_by('-priority') \
            .first()

        # TODO: Check for
        if not result:
            errors['productCode-Price'] = 'Invalid price for productCode for date'

        # TODO: find a better place for this
        instance.gift_discount = 0

        if 'giftCardCode' in instance:
            result = GiftCard.objects \
                .filter(Q(code=instance['giftCardCode']),
                        Q(date_start__lte=instance['date']),
                        Q(date_end__gte=instance['date']) | Q(date_end__isnull=True)) \
                .first()
            if result:
                instance.gift_discount = result.amount
                print(result.amount)
            else:
                errors['giftCardCode'] = 'Invalid giftCardCode for date'

        if errors:
            raise serializers.ValidationError(errors)

        return instance

    def to_representation(self, instance):
        # https://docs.djangoproject.com/en/2.2/topics/db/queries/
        result = ProductPrice.objects \
            .filter(Q(product_code__code=instance['productCode']),
                    Q(start_date__lte=instance['date']),
                    Q(end_date__gte=instance['date'])) \
            .order_by('-priority') \
            .first()

        # TODO: smell test failed.
        price = result.price * ((10000 - instance.gift_discount) / 10000)
        # Bad Math Check
        if price < 0:
            price = 0

        return {'price': int(price)}
