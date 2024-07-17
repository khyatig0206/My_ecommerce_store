from django.shortcuts import redirect, render
from .models import ColorVariant, Product
# Create your views here.
from account.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def get_product(request,slug):
    product=Product.objects.get(slug=slug)
    context={'product':product}
    if request.GET.get('size'):
        size = request.GET.get('size')
        price = product.get_product_price_by_size(size)
        
        context['updated_price']=price
        context['selected_size']=size

    if request.GET.get('color'):
        color = request.GET.get('color')
        selected_color_variant = ColorVariant.objects.get(color=color)
        context['selected_color'] = color
        context['product_images'] = product.product_images.filter(color=selected_color_variant)
    else:
        context['product_images'] = product.product_images.all()

    return render(request,"products/product.html",context=context)



def add_to_cart(request, slug):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        messages.info(request, "You need to be logged in to add items to the cart.")
        return redirect('login')
    size_variant = request.GET.get('size_variant')
    color_variant = request.GET.get('color_variant')
    product = Product.objects.get(slug=slug)
    user_profile = Profile.objects.get(user=request.user)
    cart, _ = Cart.objects.get_or_create(user=user_profile, is_paid=False)
    cart_item = cartItems.objects.create(cart=cart, product=product)

    if size_variant:
        size = SizeVariant.objects.get(size=size_variant)
        cart_item.size_variant = size
    if color_variant:
        color = ColorVariant.objects.get(color=color_variant)
        cart_item.color_variant = color
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))