from django.test import TestCase, Client
from django.urls import reverse
import json

from .models import ProductPrice, Product, GiftCard

client = Client()


class ProductPriceViewTest(TestCase):
    def setUp(self):
        product_big = Product.objects.create(
            name="Big Widget",
            code="big_widget"
        )
        product_small = Product.objects.create(
            name="Small Widget",
            code="small_widget"
        )
        GiftCard.objects.create(
            code="10OFF",
            amount=1000,
            date_start="2018-07-01",
            date_end=None
        )
        ProductPrice.objects.create(
            name="default",
            price=100000,
            product=product_big
        )
        ProductPrice.objects.create(
            name="default",
            price=9900,
            product=product_small
        )
        ProductPrice.objects.create(
            name="from2019",
            price=125000,
            product=product_big
        )
        ProductPrice.objects.create(
            name="black_friday",
            price=80000,
            product=product_big
        )

    def test_get_price_big_product(self):
        data = {
            "productCode": "big_widget",
            "date": "2018-11-20",
        }
        response = client.post(reverse('get-price'), data=json.dumps(data), content_type='application/json')
        response_content = json.loads(response.content)['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['product price'], '$1000.0')

    def test_get_price_small_product(self):
        data = {
            "productCode": "small_widget",
            "date": "2018-11-20",
        }
        response = client.post(reverse('get-price'), data=json.dumps(data), content_type='application/json')
        response_content = json.loads(response.content)['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['product price'], '$99.0')

    def test_get_price_with_gift_card(self):
        data = {
            "productCode": "big_widget",
            "date": "2018-11-20",
            "giftCardCode": "10OFF",
        }
        response = client.post(reverse('get-price'), data=json.dumps(data), content_type='application/json')
        response_content = json.loads(response.content)['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['product price'], '$990.0')

    def test_get_price_black_friday(self):
        data = {
            "productCode": "big_widget",
            "date": "2018-11-23",
        }
        response = client.post(reverse('get-price'), data=json.dumps(data), content_type='application/json')
        response_content = json.loads(response.content)['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['product price'], '$800.0')

    def test_get_price_2019(self):
        data = {
            "productCode": "big_widget",
            "date": "2019-01-10",
        }
        response = client.post(reverse('get-price'), data=json.dumps(data), content_type='application/json')
        response_content = json.loads(response.content)['result']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content['product price'], '$1250.0')
