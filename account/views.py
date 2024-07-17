from django.urls import reverse
import stripe
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect 
from .models import Profile,Cart,cartItems,Coupon
from django.contrib.auth import authenticate,login,logout
from product.models import ColorVariant, Product, ProductImage, SizeVariant
from django.conf import settings
from django.views import View

def login_page(request):
    if request.method == 'POST':  
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            messages.warning(request, "You do not have an account.")
            return HttpResponseRedirect(request.path_info)
        
        if not user.profile.is_email_verified:
            messages.warning(request, "Your email is not verified.")
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username=email, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect('/')  

        messages.warning(request, "Invalid Credentials.") 
        return HttpResponseRedirect(request.path_info)
        
    return render(request, 'account/login.html')



def register_page(request):
    if request.method == 'POST': 
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():
            messages.warning(request, "An account already exists with this email.")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Registration successful. An email has been sent.")
        return HttpResponseRedirect(request.path_info)
        
    return render(request, 'account/register.html')



def logout_view(request):
    logout(request)
    return redirect('/')
    


def activate_email(request,email_token):
        try:
            user=Profile.objects.get(email_token=email_token)
            user.is_email_verified=True
            user.save()
            return redirect('/')
        except Exception as e:
            return HttpResponse("Invalid email token. Email can't be verified.")
        


def cart_view(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        try:
            cart = Cart.objects.get(is_paid=False, user=user_profile)
        except Cart.DoesNotExist:
            cart = None

        cart_items_with_images = []
        if cart:
            for item in cart.cart_items.all():
                if item.color_variant:
                    product_image = item.product.product_images.filter(color=item.color_variant).first()
                else:
                    product_image = item.product.product_images.first()

                item_image_url = product_image.image.url if product_image else None
                cart_items_with_images.append({
                    'item': item,
                    'image_url': item_image_url
                })
        
        context = {
            'cart': cart,
            'cart_items_with_images': cart_items_with_images
        }
        if request.method=="POST":
            coupon=request.POST.get('coupon')
            try:
                coupon_obj=Coupon.objects.get(coupon_code__icontains = coupon)
                if cart.coupon:
                    messages.info(request, "Coupon already Used.")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
                if cart.get_cart_price() < coupon_obj.minimum_amount:
                    messages.info(request, f"Amount should exceed ₹{coupon_obj.minimum_amount}")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                if coupon_obj.is_expired:
                    messages.warning(request,"Coupon has Expired")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                

                cart.coupon=coupon_obj
                cart.save()
                messages.success(request, "Coupon Applied.")

                
            except Coupon.DoesNotExist:
                messages.info(request, "Coupon Does not Exist.")


        
        return render(request, 'account/cart.html', context)

    else:
        messages.info(request, "You need to be logged in to view the cart.")
        return redirect('login')
    

def remove_item(request,uid):
    try:
        cart_item=cartItems.objects.get(uid=uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    

def remove_coupon(request,uid):
    cart=Cart.objects.get(uid=uid)
    cart.coupon=None
    cart.save()
    messages.info(request, "Coupon removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout_session(request, uid):
    if request.method == "POST":
        cart = Cart.objects.get(uid=uid)
        profile = Profile.objects.get(user=request.user)

        # Create a product in Stripe (if it doesn't exist yet)
        product = stripe.Product.create(
            name="Your Product Name",
            description="Description of your product",
            metadata={"cart_id": uid}
        )

        # Create a price for the product
        price = stripe.Price.create(
            unit_amount=int(cart.get_cart_price() * 100),  # Multiply by 100 for cents
            currency="inr",
            product=product.id,
        )

        # Create the Stripe session with the line item using the price ID
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price.id,
                    "quantity": profile.get_cart_count(),
                }
            ],
            metadata={"cart_id": uid},
            mode="payment",
            success_url=request.build_absolute_uri(reverse('success_url', kwargs={'uid': uid})),
            cancel_url=request.build_absolute_uri(reverse('cancel_url')),
        )

        return redirect(session.url)
    
def success_view(request,uid):
    cart=Cart.objects.get(uid=uid)
    cart.is_paid=True
    cart.save()
    return render(request, 'base/success.html')

