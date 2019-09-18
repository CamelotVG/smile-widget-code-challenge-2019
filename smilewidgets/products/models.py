from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')

    def calculate_price_for_date(self, date, gift_card=None):
        final_price = self.price
        product_prices = self.product_prices.filter(date_start__lte=date, date_end__gte=date)
        if product_prices.exists():
            final_price = product_prices.latest('date_start').price
        if gift_card and gift_card.is_active(date):
            final_price -= gift_card.amount
        return round(final_price / 100, 2) if final_price > 0 else 0
    
    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def is_active(self, date):
        return self.date_start <= date \
               and (self.date_end >= date if self.date_end else True)
    
    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)
    
    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)


class ProductPrice(models.Model):
    name = models.CharField(max_length=30)
    date_start = models.DateField()
    date_end = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_prices')
    price = models.PositiveIntegerField(help_text='Price of product in cents')
