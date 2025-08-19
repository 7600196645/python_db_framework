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
<<<<<<< HEAD
from django.urls import path,include
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('patient_form/', views.patient_form, name='patient_form'),
    
]

=======
from django.urls import path, include
from myapp import views

urlpatterns = [
   path('dashboard/', views.dashboard, name='dashboard'),
   path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
   path('login/', views.login, name='login'),
   path('register/', views.register, name='register'),
   path('logout/', views.logout_view, name='logout'),
   path('forget_password/', views.forget_password, name='forget_password'),
   path('otp/', views.otp, name='otp'),
   path('reset_password/', views.reset_password, name='reset_password'),
   path('password_change/', views.pd_change, name='password_change'),
   path('manage_profile/', views.manage_profile, name='manage_profile'),
   path('search_artist/', views.search_artist, name='search_artist'),
   path('artist/<int:user_id>/', views.artist_profile, name='artist_profile'),
   path('booking/', views.booking, name='booking'),
   path('review/', views.review, name='review'),
   path('upload_media/', views.upload_media, name='upload_media'),
   path('bookings/', views.bookings_page, name='bookings'),
   path('book-artist/<int:artist_id>/', views.book_artist, name='book_artist'),
   path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
   path('artist-bookings/', views.artist_bookings, name='artist_bookings'),
   path('artcancel-booking/<int:booking_id>/', views.artcancel_booking, name='artcancel_booking'),
   path('manage_booking/', views.manage_booking, name='manage_booking'),
   path('reviews/', views.feedback_reviews, name='feedback_reviews'),
   path('artist-feedbacks/', views.feedback_by_artist_list, name='feedback_by_artist_list'),
   path('add_artist/', views.add_artist, name='add_artist'),
   path('adminpanel/users/', views.manage_users, name='manage_artist_customer'),
   path('adminpanel/user/view/<int:user_id>/', views.admin_view_user, name='admin_view_user'),
   path('adminpanel/user/edit/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
   path('adminpanel/user/delete/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
   path('adminpanel/bookings/', views.view_all_bookings, name='view_all_bookings'),
   path('adminpanel/reviews/', views.view_all_reviews, name='view_all_reviews'),
   path('adminpanel/approve-artist/', views.approve_artist, name='approve_artist'),
   path('adminpanel/feedbacks/', views.view_all_feedbacks, name='view_all_feedback'),


]
>>>>>>> 58fe60e7d81f7bfbd5bbf72179b00ddf9e542bfb
