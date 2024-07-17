from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display=['color']
    model=ColorVariant

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display=['size','price']
    model=SizeVariant

class ProductImageAdmin(admin.StackedInline):
    model=ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageAdmin]

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)