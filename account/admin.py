from django.contrib import admin
from .models import Cart, Profile,cartItems,Coupon
# Register your models here.
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(cartItems)
admin.site.register(Coupon)