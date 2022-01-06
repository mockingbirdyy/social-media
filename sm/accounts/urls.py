from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_dashboard/<int:user_id>/', views.user_dashboard, name='user_dashboard'),
    path('Edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('phone_login/', views.phone_login, name='phone_login'),
]