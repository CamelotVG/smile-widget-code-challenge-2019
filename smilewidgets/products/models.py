from django.db import models
from django.db.models import Min, Q


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)

    def get_price(self, date, product_code, gift_code):
        start_date_prices = ProductPrice.objects.filter(date_start__lte=date, product__code__iexact=product_code)
        price = start_date_prices.filter(
            Q(date_end__isnull=True) | Q(date_end__gt=date)
        ).aggregate(Min('new_price'))['new_price__min']
        if price is None:
            price = self.price

        if gift_code:
            gift_card_amount = GiftCard.objects.get(code__iexact=gift_code).amount
            price -= gift_card_amount

        if price < 0:
            return 0

        return price / 100


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)


class ProductPrice(models.Model):
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_prices')
    new_price = models.PositiveIntegerField(help_text='New price of product in cents')
