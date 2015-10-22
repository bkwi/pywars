from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import (LoginView, LogoutView, RegisterUserView, UserProfile,
                    ForgotPassword)

urlpatterns = [
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^register/', RegisterUserView.as_view(), name='register'),
    url(r'^forgot-password/', ForgotPassword.as_view(),
        name='forgot_password'),

    url(r'^profile/', UserProfile.as_view(), name='profile'),
]
