from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from base.emails import send_account_activation_email
from base.models import BaseModel
from django.db.models.signals import post_save
import uuid
from product.models import Product,ColorVariant,SizeVariant,ProductImage

class Coupon(BaseModel):
    coupon_code=models.CharField(max_length=10)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField(default=1000)
    minimum_amount=models.IntegerField(default=7000)
    def __str__(self) -> str:
        return self.coupon_code
    
class Profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_email_verified=models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    profile_img=models.ImageField(upload_to="profile")

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}" 
    
    def get_cart_count(self):
        return cartItems.objects.filter(cart__user=self,cart__is_paid=False).count()

class Cart(BaseModel):
    user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='carts')
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    is_paid=models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.user.first_name} {self.user.user.last_name}" 
    
    def get_cart_price(self):
        cart_items = self.cart_items.all()
        price = []
        for item in cart_items:
            item_price = item.get_cartitem_price() 
            price.append(item_price)
        
        total_price = sum(price)
        if self.coupon and self.coupon.minimum_amount < total_price:
            return total_price - self.coupon.discount_price
        
        return total_price

class cartItems(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    color_variant=models.ForeignKey(ColorVariant,on_delete=models.SET_NULL,null=True,blank=True)
    size_variant=models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.product.product_name}-{self.cart.user.user.email}"
    
    def get_cartitem_price(self):
        price=[self.product.price]

        if self.size_variant:
            price.append(self.size_variant.price)
        return sum(price)*(self.quantity)



class Order(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="orders")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default="Processing") 

    def __str__(self):
        return f"Order {self.order_id} for {self.user.user.email}"

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} pcs"



# The @receiver decorator links the send_email_token function to the post_save signal of the User model.
@receiver(post_save,sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        if created:
            email_token=str(uuid.uuid4())
            Profile.objects.create(user=instance,email_token=email_token)
            email=instance.email
            send_account_activation_email(email,email_token)
    except Exception as e:
        print(e)

    
    

    