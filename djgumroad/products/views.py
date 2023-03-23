from django.shortcuts import render
from products.models import Product
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(generic.ListView):
    template_name = 'discovery.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.all()
    
class ProductDetailView(generic.DetailView):
    template_name = 'product/detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.all()

class UserProductsView(LoginRequiredMixin, generic.ListView):
    template_name = 'my_products.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)