from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response


@api_view(['POST'])
@parser_classes([JSONParser])
def get_price(request):
    data = request.data
    return Response(data)
