from django.urls import path, reverse, include
from . import views

app_name="products"
urlpatterns = [
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail')
]
