from django.shortcuts import render
from product.models import Product
from django.db.models import Q
# Create your views here.

def home_page(request):
    
    context={'products': Product.objects.all()}
    return render(request,"home/index.html",context)

def search_page(request):
    query = request.GET.get('q')
    
    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(product_desc__icontains=query) |
            Q(price__icontains=query)
        )
    else:
        products = Product.objects.none()

    return render(request, 'home/search.html', {'products': products, 'query': query})