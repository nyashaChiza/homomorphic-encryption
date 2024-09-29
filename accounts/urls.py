from django.urls import include, path
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='account/login.html'), name='accounts_login'),
    path('logout/', views.custom_logout, name='accounts_logout'),
    path('detail/<int:pk>/', views.AccountDetailView.as_view(), name='account_detail'),
    path('profile/update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='accounts_reset_password'),
    path('password/reset/done', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='accounts_reset_password_done'),
]