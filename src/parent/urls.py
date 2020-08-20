from django.urls import path
from .views import(
    add_to_cart,
    remove_from_cart
) 


app_name = 'parent'

urlpatterns = [
    path('add-to-cart/<str:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<str:slug>/', remove_from_cart, name='remove-from-cart')
]
