"""
URL configuration for home project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from auth import views as auth_views
from landing import views as landing_views
from subscriptions import views as subscriptions_views
from checkouts import views as checkouts_views
from .views import (
    home_view, 
    about_view, 
    pw_protected_view, 
    user_only_view,
    staff_only_view,
    
)

from .api import api

urlpatterns = [
    path('api/', api.urls),
    path('', landing_views.landing_dashboard_page_view, name='home'),
    path("checkout/sub-price/<int:price_id>/",
            checkouts_views.product_price_redirect_view, 
            name='sub-price-checkout',
    ),
    path("checkout/start/",
            checkouts_views.checkout_redirect_view, 
            name='stripe-checkout-start',
    ),
    path("checkout/success/",
            checkouts_views.checkout_success_view, 
            name='stripe-checkout-success',
    ),
    path('pricing/', subscriptions_views.subscription_price_view, name='pricing'), # subscription_price_page
    path('pricing/<str:interval>/', subscriptions_views.subscription_price_view, name='pricing_interval'), # subscription_price_page
    path('about/', about_view, name='about'), # about_page
    path('hello-world/', home_view), # hello-world_page
    path('accounts/billing/', subscriptions_views.user_subscription_view, name='user_subscription'), # user_subscription_page
    path('accounts/billing/cancel', subscriptions_views.user_subscription_cancel_view, name='user_subscription_cancel'), # user_subscription_cancel_page
    path('accounts/', include('allauth.urls')), # allauth_urls
    path('protected/user_only', user_only_view),
    path('protected/staff_only', staff_only_view), # staff_only_page
    path('protected', pw_protected_view),
    path('profiles/', include('profiles.urls')),
    path("admin/", admin.site.urls), # admin_page
]
