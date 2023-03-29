from django.contrib import admin
from .models import Product, EmailProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name',)
    search_fields = ['name']
    list_filter = ('user',)

    list_display = ['name', 'user', 'cover']


    fieldsets = (
        
        (("The User"), {"fields": ("user",)}),
        (
            ("Product info"),
            {
                "fields": (
                    'name',
                    'description',
                    'cover',
                    'slug',
                    'active',
                    'price',
                ),
            },
        ),
        (("Product content"), {"fields": ("content_url", "content_file",)}),
    )


# admin.site.register(Product, ProductAdmin)
admin.site.register(EmailProduct)