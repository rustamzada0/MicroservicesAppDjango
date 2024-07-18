import requests
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from ..models import Product
from .serializers import ProductSerializer

def check_access_token(access_token): # utils.py -de saxlaya bilerik
    url = 'http://localhost:8000/account/api/token/verify/'
    # headers = {'Authorization': f'Bearer {access_token}'} lazim deyil cunki verify edende bodyde gonderirik
    response = requests.post(url, data={'token': access_token}) #headers=headers

    if response.status_code == 200:
        print("Salam")
        return True
    else:
        print("Salam 400")
        return False


class ProductViews(APIView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
    
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = token.split()[1]

        if check_access_token(token):
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)


class ProductDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        token = request.headers.get('Authorization')
        if not token:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = token.split()[1]  # Bearer token_string'den token'ı alın

        if check_access_token(token):
            print("Salam")
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        token = request.headers.get('Authorization')
        if not token:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        token = token.split()[1]  # Bearer token_string'den token'ı alın

        if check_access_token(token):
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

# ########################## 2-ci version ########################## (GENERICS)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission

class TokenRequiredMixin(BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        if not token:
            self.message = "Authentication credentials were not provided."
            return False
        
        token = token.split()[1]  # Bearer token_string'den token'ı alın

        if not check_access_token(token):
            self.message = "Invalid token."
            return False

        return True


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [TokenRequiredMixin]






