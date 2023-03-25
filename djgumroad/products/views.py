from django.shortcuts import render
from products.models import Product
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from products.forms import ProductModelForm

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

class ProductCreatevView(LoginRequiredMixin, generic.CreateView):
    template_name = 'product/create_product.html'
    form_class = ProductModelForm

    # send back to the product
    def get_success_url(self):
        return reverse('products:product-detail', kwargs={'slug': self.product.slug})

    # add a user to the product
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        self.product = instance

        return super(ProductCreatevView, self).form_valid(form)

class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'product/update_product.html'
    form_class = ProductModelForm
    model = Product

    # send back to the product
    def get_success_url(self):
        return reverse('products:product-detail', kwargs={'slug': self.product.slug})

    # def get_queryset(self):
    #     return Product.objects.filter(user=self.request.user)
    

    # add a user to the product
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        self.product = instance

        return super(ProductUpdateView, self).form_valid(form)


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'product/delete_product.html'

    def get_success_url(self):
        return reverse('discovery')
    
    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    

    











