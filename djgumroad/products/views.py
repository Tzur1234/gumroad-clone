from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product, EmailProduct
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

# Shows all the products at all
class ProductListView(generic.ListView):
    template_name = 'discovery.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.all()
    
class ProductDetailView(generic.DetailView):
    template_name = 'product/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.get_object()
        has_access = False
        if self.request.user.is_authenticated:
            if product in self.request.user.userlibrary.products.all():
                has_access = True
        context.update({
            "has_access": has_access
        })
        return context
    
    
    def get_queryset(self):
        return Product.objects.all()

# Shows all user's created products
class UserProductsView(LoginRequiredMixin, generic.ListView):
    template_name = 'my_products.html'
    context_object_name = 'products'
    
    def get_queryset(self):

        return Product.objects.filter(user=self.request.user)

    # Did the user has already created Stripe account?
    def get_context_data(self, **kwargs):
        context = super(UserProductsView, self).get_context_data(**kwargs)

        account = stripe.Account.retrieve(self.request.user.customer_account_id)
        details_submitted = account["details_submitted"]
        print('details_submitted ???: ',details_submitted)
        context.update({
            "details_submitted": details_submitted
        })

        return context

    
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

        
        product_id = self.kwargs['pk']
        choosen_product = Product.objects.get(pk=product_id)
        # User identify
        

        if request.user.is_authenticated:
            stripe_customer_id = request.user.stripe_customer_id
            stripe_customer_email = request.user.email
        else:
            stripe_customer_id = None
            stripe_customer_email = None

        if settings.READ_DOT_ENV_FILE:
            YOUR_DOMAIN = 'http://localhost:8000'
            product_images_url = ['https://media.istockphoto.com/id/1291049124/photo/concept-for-debugging-and-fixing-errors-in-the-code.jpg?s=2048x2048&w=is&k=20&c=1xecIrsSNhtav7KAgB5majTkXUd147WfRWXyYSgqwWw=']
        else: 
            YOUR_DOMAIN = 'https://djgumroad-app-xmuhn.ondigitalocean.app'
            product_images_url = [YOUR_DOMAIN + '/media/' + choosen_product.cover.url]

        # user id
        if request.user.stripe_customer_id == None:
            # Create user id 
            customer_creation = 'always'
        else:
            # Dont Create new user id
            customer_creation = "if_required"

        
        print('user email', stripe_customer_email )
        print('user customer_id', stripe_customer_id )
        print('product_images_url', product_images_url )

        checkout_session = stripe.checkout.Session.create(
            
            customer_email=stripe_customer_email,
            line_items=[
                            {
                                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                                 'price_data': {
                                                'currency': 'usd',
                                                'product_data': {
                                                    'name': choosen_product.name,
                                                    'images': product_images_url
                                                },
                                                'unit_amount': choosen_product.price,
                                                },
                                'quantity': 1,
                            },
                        ],
            # data about fee and paying destination
            payment_intent_data={
                                    "application_fee_amount": 100,
                                    "transfer_data": {"destination": choosen_product.user.customer_account_id}, # User paying destination
                                },
            mode='payment',
            customer_creation=customer_creation,
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
    ACCOUNT_WAS_PAID = "account.updated"
    # Listen for success payment

    payload = request.body    
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    # endpoint_secret=settings.STRIPE_WEBHOOK_SECRET
    endpoint_secret= settings.STRIPE_ENDPOINT_SECRET
    

    # print('endpoint_secret: ', endpoint_secret)
    
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
        
        print("The customer has paid !!!!!!!!!!!!!!!!!")
        
        product_id = event["data"]["object"]["metadata"]["product_id"]
        product = Product.objects.get(id=product_id)
        customer_email = event["data"]["object"]["customer_details"]["email"]
        stripe_customer_id = event["data"]["object"]["customer"]
        print('customer_id:', stripe_customer_id)
        print('customer_email:', customer_email)
        print('Try ...')
        try:
            user = User.objects.get(email=customer_email)            
            print('User exists')
            # give access to the product
            user.userlibrary.products.add(product)
            if stripe_customer_id:
                user.stripe_customer_id = stripe_customer_id
                user.save()
            
        except User.DoesNotExist:
            # TODO : handle anownymouse check out
            print('User does not exists')
            # Create a EmailProduct
            EmailProduct.objects.create(email=customer_email, product=product)

            # send an email to the user
            send_mail(
            "You have successfuly bought the product !",
            "Please sign in to your app",
            "test2gmail.com",
            [customer_email]
        )

        # if the money was transferd to the customer
    
    if event["type"] == ACCOUNT_WAS_PAID:
        print("The money was transfered  succesfuly !")




    return HttpResponse(status=200)

# Bought products
class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'    


