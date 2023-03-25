from django.urls import path, reverse, include
from . import views

app_name="products"
urlpatterns = [
    path('<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path("product/update/<slug>/", views.ProductUpdateView.as_view(), name="product-update"),
    path("product/delete/<int:pk>/", views.ProductDeleteView.as_view(), name="product-delete"),
]
