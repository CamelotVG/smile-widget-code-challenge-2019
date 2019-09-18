from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')
    
    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


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
    event_name = models.CharField(max_length=40, help_text='Name of event')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Product',
        related_name='product_prices'
    )
    price = models.PositiveIntegerField(help_text='Special price of product in cents')
