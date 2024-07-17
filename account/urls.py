from django.urls import path
from account.views import login_page, register_page,activate_email,cart_view,logout_view,remove_item,remove_coupon,checkout_session,success_view
from product.views import add_to_cart
urlpatterns = [
    path('login/',login_page,name='login'),
    path('logout/',logout_view,name='logout'),
    path('register/',register_page,name='register'),
    path('activate/<email_token>',activate_email,name='activate_email'),
    path('cart-view/',cart_view,name='cart_view'),
    path('add-to-cart/<slug>',add_to_cart,name='add-to-cart'),
    path('remove/<uid>',remove_item,name='remove_item'),
    path('remove_coupon/<uid>',remove_coupon,name='remove_coupon'),
    path('checkout_session/<uid>',checkout_session,name='checkout_session'),
    path('success/<uid>', success_view, name='success_url'),
    path('cancel/', cart_view, name='cancel_url'),
]