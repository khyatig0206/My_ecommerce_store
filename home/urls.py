from django.urls import path
from .views import home_page,search_page,handle_request
urlpatterns = [
    path('',home_page,name='home_page'),
    path('search/',search_page,name='search_page'),
    path('handle-request/', handle_request, name='handle_request'),

]