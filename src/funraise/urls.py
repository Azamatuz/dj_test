"""funraise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from accounts.views import (
  
    LoginView, 
    RegisterView, 
    SignUpView,
    profile_view,
)

from carts.views import cart_detail_api_view

from parent.views import(
    kid_create_view,
    kid_detail_view,
    kid_list_view,
    kid_update_view,
    kid_delete_view,
    OrderSummaryView,
)

from school.views import(
    event_item_create_view,
)
from vendor.views import(
    menu_item_create_view,
)

from .views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    
	path('accounts/profile/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),

    path('accounts/login/', auth_views.LoginView.as_view()),
    path('accounts/register/', RegisterView.as_view(), name='register'),

    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('cart/', include("carts.urls")),
    
    path('menu-new/', menu_item_create_view),
    path('menu/', include('vendor.urls')),

    path('event-new/', event_item_create_view),
    path('event/', include('school.urls')),

    path('order/', include('parent.urls')),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    
    path('children-new/', kid_create_view),
    path('children/', kid_list_view, name='kidlist'),
    path('children/<str:slug>/', kid_detail_view, name='kid'),
    path('children/<str:slug>/edit/', kid_update_view),
    path('children/<str:slug>/delete/', kid_delete_view),



]
