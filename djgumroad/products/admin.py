from django.contrib import admin
from .models import Product, EmailProduct

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name',)
    search_fields = ['name']
    list_filter = ('user',)


admin.site.register(Product, ProductAdmin)
admin.site.register(EmailProduct)