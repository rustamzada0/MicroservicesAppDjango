from django.urls import path, include

from . import views

urlpatterns = [

    path('product/', views.ProductViews.as_view()),

]
