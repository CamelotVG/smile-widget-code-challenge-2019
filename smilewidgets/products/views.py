from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .models import ProductPrice, GiftCard
from django.shortcuts import get_object_or_404


class ProductPriceView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        product_code = request.data.get("productCode")
        date = request.data.get("date")
        gift_card_code = request.data.get("giftCardCode", None)
        req_date = datetime.strptime(date, "%Y-%m-%d")
        black_friday_start = datetime(2018, 11, 23)

        if black_friday_start <= req_date <= black_friday_start + timedelta(days=3):
            name = "black_friday"
        elif req_date >= datetime(2019, 1, 1):
            name = "from2019"
        else:
            name = "default"
        price_obj = get_object_or_404(ProductPrice, name=name, product__code=product_code)
        price = price_obj.price
        discount_amount = 0
        if gift_card_code:
            gift = GiftCard.objects.filter(code=gift_card_code, date_start__lte=req_date)
            if gift:
                discount_amount = gift.first().amount
        res = "$" + str((price - discount_amount)/100)
        return Response({"result": {"product price": res}}, status=200)
