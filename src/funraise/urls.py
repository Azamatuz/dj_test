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
  
    LoginView, RegisterView, 
    SignUpView,
    #ParentSignUpView, 
    #SchoolSignUpView, 
    #VendorSignUpView,

    profile_view,
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
    
    # path('accounts/register/parent/', ParentSignUpView.as_view(), name='parent_signup'),
    # path('accounts/register/school/', SchoolSignUpView.as_view(), name='school_signup'),
    # path('accounts/register/vendor/', VendorSignUpView.as_view(), name='vendor_signup'),

    path('menu-new/', menu_item_create_view),
    path('menu/', include('vendor.urls')),

    path('event-new/', event_item_create_view),
    path('event/', include('school.urls')),

]
