from django import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ViewProducts, ProductDetail

urlpatterns = [
    path('products', ViewProducts.as_view()),
    path('products/<int:pk>/', ProductDetail.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)
