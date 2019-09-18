from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from products.serializers import RequestPriceSerializer


@api_view(['POST'])
@parser_classes([JSONParser])
def get_price(request):
    serializer = RequestPriceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    product = data['productCode']
    date = data['date']
    gift_cad = data.get('giftCardCode')
    price = product.calculate_price_for_date(date, gift_cad)
    return Response({'price': price})
