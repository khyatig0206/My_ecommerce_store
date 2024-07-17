from django.urls import path
from .views import home_page,search_page
urlpatterns = [
    path('',home_page,name='home_page'),
    path('search/',search_page,name='search_page')
]