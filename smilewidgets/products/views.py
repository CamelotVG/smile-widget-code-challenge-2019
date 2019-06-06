from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from products.serializer import ProductPriceSerializer


# Create your views here.

class GetPriceView(APIView):
    
    def get(self, request):
        serializer = ProductPriceSerializer(data=request.data)
        # if serializer.is_valid() == False: 
        #     Response(print(serializer.error
        serializer.is_valid(raise_exception=True)
        
        print(serializer.validated_data)
        return Response(serializer.data, status=200)