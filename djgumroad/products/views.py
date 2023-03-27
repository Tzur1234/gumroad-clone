from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from products.forms import ProductModelForm
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from stripe.error import SignatureVerificationError
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()

class ProductListView(generic.ListView):
    template_name = 'discovery.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.all()
    
class ProductDetailView(generic.DetailView):
    template_name = 'product/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })  
        return context
    
    
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
        # return reverse('discovery')
        return reverse('user-products')
    
    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

class CreateCheckoutSessionView(generic.View):
    
    def post(self, request, *args, **kwargs): 

        if settings.DEBUG:
            YOUR_DOMAIN = 'http://127.0.0.1:8000'
        else: 
            YOUR_DOMAIN = 'http://mydomain.com'

        product_id = self.kwargs['pk']
        choosen_product = Product.objects.get(pk=product_id)
        # User identify
        

        if request.user.is_authenticated:
            stripe_customer_id = request.user.stripe_customer_id
            stripe_customer_email = request.user.email
        else:
            stripe_customer_id = None
            stripe_customer_email = None

            
        
        checkout_session = stripe.checkout.Session.create(
            customer_id=stripe_customer_id,
            customer_email=stripe_customer_email,
            line_items=[
                            {
                                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                                 'price_data': {
                                                'currency': 'usd',
                                                'product_data': {
                                                    'name': choosen_product.name,
                                                },
                                                'unit_amount': choosen_product.price,
                                                },
                                'quantity': 1,
                            },
                        ],
            mode='payment',
            success_url=YOUR_DOMAIN + reverse('success'),
            cancel_url=YOUR_DOMAIN + reverse('discovery'),
            metadata={'product_id': product_id}
        )

        return redirect(checkout_session.url, code=303)
       
class SucessStripeView(generic.TemplateView):
    template_name = 'success.html'    

@csrf_exempt
def StripeWebhookView(request): 
    
    CHECKOUT_SESSION_COMPLETED = "checkout.session.completed"
    # Listen for success payment

    payload = request.body    
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    endpoint_secret='whsec_o0T4qLvSeI0kjhpUs2JcHq9F0Ik9VUeY'
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )
        
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    except SignatureVerificationError as e:
        print(e)
        return HttpResponse(status=400)

    if event["type"] == CHECKOUT_SESSION_COMPLETED:
        print(event)
        
        product_id = event["data"]["object"]["metadata"]["product_id"]
        product = Product.objects.get(id=product_id)
        customer_email = event["data"]["object"]["customer_details"]["email"]
        customer_id_stripe = event["data"]["object"]["customer"]
        print('customer_id:', customer_id_stripe)
        print('customer_email:', customer_email)
        print('Try ...')
        try:
            user = User.objects.get(email=customer_email)            
            print('User exists')
            # give access to the product
            user.userlibrary.products.add(product)
            
        except User.DoesNotExist:
            # TODO : handle anownymouse check out
            print('User does not exists')




    return HttpResponse(status=200)


