"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile1'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout, name='logout'),
    path('password_change/', views.password_change_view, name='password_change'),
    path('password_change_done/', views.pass_change_done, name='password_change_done'),
    path('doctor_info/', views.doctor_info, name='doctor_info'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('doctor_update/<int:pk>/', views.doctor_update, name='doctor_update'),
    path('doctor_delete/<int:pk>/', views.doctor_delete, name='doctor_delete'),
    path('index/', views.index, name='index'),
    path('add/', views.add_doctor, name='add_doctor'),
    path('delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('update/<int:id>/', views.update_doctor, name='update_doctor'),
    path('appoinment/', views.appoinment, name='appoinment'),
    path('success/', views.payment_success, name='payment_success'),
    path('map/', views.doctor_map, name='doctor_map'),
]

