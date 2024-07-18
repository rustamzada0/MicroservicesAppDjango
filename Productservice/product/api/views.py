import requests
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Product
from .serializers import ProductSerializer

def check_access_token(access_token):
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




# class ProductListCreateView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def post(self, request, *args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
#         token = token.split()[1]
#         print(token)

#         if not check_access_token(token):
#             return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)


# class ProductListCreateView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def create(self, request, *args, **kwargs):
#         print(request.headers)
#         print(request)
#         token = request.headers.get('Authorization')
#         print(token)
#         if not token:
#             return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
#         token = token.split()[1] 

#         if not check_access_token(token):
#             return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


