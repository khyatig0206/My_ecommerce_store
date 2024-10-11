from django.urls import reverse
import stripe
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect 
from .models import Profile,Cart,cartItems,Coupon,Order,OrderItem
from django.contrib.auth import authenticate,login,logout
from product.models import ColorVariant, Product, ProductImage, SizeVariant
from django.conf import settings
from django.views import View
import uuid
import time
import datetime
import random

def generate_custom_order_id():
    # Get the current date
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')  # Format: YYYYMMDD
    time_part = str(now.strftime('%H%M%S'))  # Time in hours, minutes, and seconds

    # Add a random number for extra uniqueness
    random_number = random.randint(100, 999)

    # Combine everything into a final order ID
    return f"ORD{date_str}-{time_part}{random_number}"


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
            request.session['user_id'] = user_obj.id
            request.session.save()
            user_id = request.session.get('user_id')
            print("user id is",user_id)

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
        cart_items = cart.cart_items.all()
        
        # Create line items for each product in the cart
        line_items = []
        for cart_item in cart_items:
            product = cart_item.product
            color = cart_item.color_variant.color if cart_item.color_variant else "No color"
            size = cart_item.size_variant.size if cart_item.size_variant else "No size"
            quantity=cart_item.quantity
            # Create the product in Stripe with more detailed info
            stripe_product = stripe.Product.create(
                name=f"{product.product_name}",
                description=f'''Product ID: {product.uid},Product: {product.slug}, Color: {color}, Size: {size}, Quantity: {quantity}''',
                metadata={
                    "product_id": product.uid,
                    "color": color,
                    "size": size,
                    "quantity":quantity
                }
            )

            # Create a price for the product
            stripe_price = stripe.Price.create(
                unit_amount=int(cart_item.get_cartitem_price() * 100),  # Multiply by 100 for cents
                currency="inr",
                product=stripe_product.id,
            )

            # Add this product to the Stripe line items
            line_items.append({
                "price": stripe_price.id,
                "quantity": 1,
            })

        # Create the Stripe session with all the line items
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            metadata={"cart_id": uid},
            mode="payment",
            success_url=request.build_absolute_uri(reverse('success_url', kwargs={'uid': uid})),
            cancel_url=request.build_absolute_uri(reverse('cancel_url')),
        )

        return redirect(session.url)


def buy_now(request, slug):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        messages.info(request, "You need to be logged in to add items to the cart.")
        return redirect('login')
    size_variant = request.GET.get('size_variant')
    color_variant = request.GET.get('color_variant')
    quantity = int(request.GET.get('quantity', 1))  
    product = Product.objects.get(slug=slug)
    user_profile = Profile.objects.get(user=request.user)
    cart, _ = Cart.objects.get_or_create(user=user_profile, is_paid=False)
    cart_item = cartItems.objects.create(cart=cart, product=product,quantity=quantity)

    if size_variant:
        size = SizeVariant.objects.get(size=size_variant)
        cart_item.size_variant = size

    if color_variant:
        color = ColorVariant.objects.get(color=color_variant)
        cart_item.color_variant = color
    else:
        messages.error(request, "Please select a color.")

    cart_item.save()
    return redirect('cart_view')

def success_view(request, uid):
    cart = Cart.objects.get(uid=uid)
    cart.is_paid = True
    cart.save()

    # Generate the custom order ID based on the date and time
    custom_order_id = generate_custom_order_id()

    # Create a new order with the custom order ID
    order = Order.objects.create(
        user=cart.user,
        cart=cart,
        order_id=custom_order_id,  # Custom date-based order ID
        status="Processing",  # Default status
    )

    # Add items from cart to order
    cart_items = cart.cart_items.all()
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            color_variant=item.color_variant,
            size_variant=item.size_variant,
            quantity=item.quantity
        )

    return render(request, 'base/success.html')

def my_orders_view(request):
    profile = Profile.objects.get(user=request.user)
    orders = Order.objects.filter(user=profile)

    return render(request, 'account/my_orders.html', {'orders': orders})


