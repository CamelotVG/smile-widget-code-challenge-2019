from django.urls import reverse
from rest_framework.test import APITestCase


class ProductPriceAPIViewTestCase(APITestCase):
    fixtures = ['0002_fixtures']

    def test_get_price_not_within_event(self):
        params = {
            'productCode': 'sm_widget',
            'date': '2018-11-23'
        }

        response = self.client.get(reverse('get_price'), params)
        self.assertEqual(response.data['name'], 'Small Widget')
        self.assertEqual(response.data['code'], 'sm_widget')
        self.assertEqual(response.data['price'], 9900)

    def test_get_price_within_event_and_gift_card_code(self):
        params = {
            'productCode': 'big_widget',
            'date': '2019-11-24',
            'giftCardCode': '10OFF'
        }

        response = self.client.get(reverse('get_price'), params)
        self.assertEqual(response.data['name'], 'Big Widget')
        self.assertEqual(response.data['code'], 'big_widget')
        self.assertEqual(response.data['price'], 79000)

    def test_get_price_within_event_and_without_gift_card(self):
        params = {
            'productCode': 'sm_widget',
            'date': '2019-09-18'
        }

        response = self.client.get(reverse('get_price'), params)
        self.assertEqual(response.data['name'], 'Small Widget')
        self.assertEqual(response.data['code'], 'sm_widget')
        self.assertEqual(response.data['price'], 12500)

    def test_get_price_not_found_product(self):
        params = {
            'productCode': 'small_widget',
            'date': '2019-09-18'
        }

        response = self.client.get(reverse('get_price'), params)
        self.assertEqual(response.status_code, 404)

    def test_get_price_not_found_gift_card(self):
        params = {
            'productCode': 'sm_widget',
            'date': '2019-09-18',
            'giftCardCode': '300OFF'
        }

        response = self.client.get(reverse('get_price'), params)
        self.assertEqual(response.status_code, 404)

    def test_get_price_invalid_date_format(self):
        params = {
            'productCode': 'sm_widget',
            'date': '09-18-2019'
        }

        response = self.client.get(reverse('get_price'), params)
        self.assertEqual(response.status_code, 400)
