from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from products.models import Product, EmailProduct
from django.db.models.signals import post_save

class User(AbstractUser):
    """
    Default custom user model for djgumroad.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(_("email address"), blank=True, unique=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

class UserLibrary(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product , blank=True)

    class Meta:
        verbose_name_plural = 'UserLibraries'
    
    def __str__(self):
        return self.user.email


    

# Signal - for each user create a new UserLibrary

def crate_userlibrary_postsave(sender, instance, created, **kwargs):
    if created:
        UserLibrary.objects.create(user=instance)

        # query all the Product associated with user.email
        products_queryset = EmailProduct.objects.filter(email=instance.email).only('product')
        products_queryset2 = list(EmailProduct.objects.filter(email=instance.email).values('product'))
        print(products_queryset)
        print(products_queryset2)
        for product in products_queryset2:
            print(product['product'])
            instance.userlibrary.products.add(product['product'])


post_save.connect(crate_userlibrary_postsave, sender=User)











