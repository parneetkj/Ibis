"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from lessons import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page, name ='home_page'),
    path('feed/', views.feed, name='feed'),
    path('new_request/', views.new_request, name='new_request'),
    path('update_request/<int:id>', views.update_request, name='update_request'),
    path('delete_request/<int:id>', views.delete_request, name='delete_request'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('pending_requests/', views.pending_requests, name='pending_requests'),
    path('new_booking/<int:id>', views.new_booking, name='new_booking'),
    path('update_booking/<int:id>', views.update_booking, name='update_booking'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('bookings/', views.bookings, name='bookings'),
]
