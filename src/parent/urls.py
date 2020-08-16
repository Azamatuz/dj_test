from django.urls import path
from .views import(
    add_to_cart
) 


app_name = 'parent'

urlpatterns = [
    path('add_to_cart/slug', add_to_cart, name='add_to_cart')
]
