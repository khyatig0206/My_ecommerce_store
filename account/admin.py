from django.contrib import admin
from .models import Cart, Profile,cartItems,Coupon,OrderItem,Order
# Register your models here.
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(cartItems)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(OrderItem)