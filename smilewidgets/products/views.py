from rest_framework.views import APIView
from rest_framework.response import Response
from products.serializers import ProductPriceSerializer
from djangorestframework_camel_case.util import underscoreize


class GetPriceViewSet(APIView):
    def get(self, request):
        serializer = ProductPriceSerializer(data=underscoreize(request.query_params))
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
