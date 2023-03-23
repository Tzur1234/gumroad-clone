from django.db import models

def product_image_path(instance, filename):
    return f"product_image/id_{instance.id}/{filename}"

class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    cover = models.ImageField(blank=True, null=True, upload_to=product_image_path)
    slug = models.SlugField()

    # content
    content_url = models.URLField(blank=True, null=True, max_length=200)
    content_file = models.URLField(blank=True, null=True, max_length=200)

    price = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    
