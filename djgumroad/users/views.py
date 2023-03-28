from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
import stripe
from django.conf import settings

stripe.api_key = 'sk_test_51MprlpESXHNK1nmVZs7f7dMBFCKvpSUUI7ir0f9ELX7ed9Xplj3ht4bqCflY23T97tK8X6TwwsEDCURfESNLw5CC00CAVcMBF0'

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


# Redirect to create account page
class StripeAccountLinkView(LoginRequiredMixin, RedirectView):
    permanent = False
    my_domain = 'http://localhost:8000'
    if not settings.DEBUG:
        my_domain = 'https://domain.com'
    

    def get_redirect_url(self):
        # Retrieve link generate "Connect Account"
        account_link = stripe.AccountLink.create(
            account=self.request.user.customer_account_id, #account id 
            refresh_url=self.my_domain + reverse('stripe-account-link'), 
            return_url=self.my_domain + reverse('user-products'),
            type="account_onboarding", 
            )
        print(account_link)
        return account_link['url']



        


