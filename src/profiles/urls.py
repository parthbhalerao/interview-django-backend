
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profiles_list_view, name='profiles_list_view'),  # list_page
    path('<str:username>/', views.profile_detail_view), # root_page
]
