"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from app.views import logoutview
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/library/', permanent=True)),
    path('library/', include('app.urls', namespace='app')),
    
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(next_page='app:dashboard'), name='logout'),
    path('accounts/logout/', logoutview, name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        success_url='/accounts/password_change/done/'
    ), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
]