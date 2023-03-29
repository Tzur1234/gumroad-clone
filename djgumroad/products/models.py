from django.db import models
from django.urls import reverse

def product_image_path(instance, filename):
    return f"product_image/id_{instance.pk}/{filename}"

class Product(models.Model):
    user = models.ForeignKey("users.User",on_delete=models.CASCADE, related_name='products') # the user who created the product
    name = models.CharField(max_length=30)
    description = models.TextField()
    cover = models.ImageField(blank=True, null=True, upload_to=product_image_path)
    slug = models.SlugField()
    active = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=1)

    # content
    content_url = models.URLField(blank=True, null=True, max_length=200)
    content_file = models.URLField(blank=True, null=True, max_length=200)


    def convert_to_dollars(self):
        # return f"{self.price / 100}"
        return "{0:.2f}".format(self.price / 100)

    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"slug": self.slug})
    


    def __str__(self):
        return self.name

class EmailProduct(models.Model):
    email = models.EmailField(max_length=254)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
