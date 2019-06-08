from django.shortcuts import render
from .models import GiftCard, ProductPrice
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json


# helper func to check if eligible black friday dates
def is_black_friday(date):
    allowed_dates = ('11-23', '11-24', '11-25')
    return date.strftime("%m-%d") in allowed_dates


@csrf_exempt
def product_price(request):
    if request.method == 'POST':
        # get args from request
        payload = json.loads(request.body)
        productCode = payload['productCode']
        date = datetime.strptime(payload['date'], "%Y-%m-%d")
        try:
            giftCardCode = payload['giftCardCode']
        except:
            giftCardCode = None
        giftCardAmount = 0

        # check if within black friday dates
        if is_black_friday(date):
            product = ProductPrice.objects.filter(name="Black Friday", productCode=productCode).first()
        # check if 2019 prices apply
        elif date.strftime("%Y") == '2019':
            product = ProductPrice.objects.filter(name="2019", productCode=productCode).first()
        # original pricing
        else:
            product = ProductPrice.objects.filter(name="Standard", productCode=productCode).first()

        if giftCardCode is not None:
            # get amount for gift card if is after start date
            giftCard = GiftCard.objects.filter(code=giftCardCode, date_start__lte=date).first()

            if giftCard is not None:
                # check if there is an end date, then check if we passed it
                if giftCard.date_end is None or giftCard.date_end >= date.date():
                    giftCardAmount = giftCard.amount

        # don't let price be negative
        price = max(product.price - giftCardAmount, 0)

        # setup response format
        try:
            response = json.dumps([{
                'Product': product.productCode,
                'Type': product.name,
                'Price': price
            }])
        except:
            response = json.dumps([{'Error': 'Error getting price'}])
        # return json
        return HttpResponse(response, content_type='text/json')
