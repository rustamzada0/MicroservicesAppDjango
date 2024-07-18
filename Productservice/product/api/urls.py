from django.urls import path, include

from . import views

urlpatterns = [

    path('product/', views.ProductViews.as_view()),
    path('product/generic/', views.ProductListCreateView.as_view()),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail')

]
