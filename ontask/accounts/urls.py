# -*- coding: utf-8 -*-


from django.urls import path, re_path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),

    path('logout/', views.LogoutView.as_view(), name='logout'),

    path(
        'password-change/',
        views.PasswordChangeView.as_view(),
        name='password-change'),

    path(
        'password-reset/',
        views.PasswordResetView.as_view(),
        name='password-reset'),

    path(
        'password-reset-done/',
        views.PasswordResetDoneView.as_view(),
        name='password-reset-done'),

    re_path(
        r'password-reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{'
        '1,13}-[0-9A-Za-z]{1,20})/$$',
        views.PasswordResetConfirmView.as_view(),  # NOQA
        name='password-reset-confirm'),
]
