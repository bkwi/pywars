from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import LoginView, LogoutView, RegisterUserView

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^register/', RegisterUserView.as_view(), name='register'),
]
