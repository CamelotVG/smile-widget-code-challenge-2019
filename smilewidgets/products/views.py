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
    return Response({'price': data['productCode'].price})
