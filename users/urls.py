from django.urls import path, include
from .views import register, profile
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

user_pattern = ([
                    path('register/', register, name='register'),
                    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
                    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
                    path('profile/', profile, name='profile'),
                ], 'user')

urlpatterns = [
    path('user/', include(user_pattern, namespace='user')),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', RedirectView.as_view(pattern_name='user:login'), name='login'),

    # password reset..
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
