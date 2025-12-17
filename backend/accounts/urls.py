from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views, admin_views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # Admin endpoints
    path('admin/check/', admin_views.admin_check, name='admin_check'),
    path('admin/mahasiswa/', admin_views.admin_get_all_mahasiswa, name='admin_mahasiswa'),
    path('admin/mahasiswa/<int:pk>/toggle/', admin_views.admin_toggle_mahasiswa_status, name='admin_toggle_status'),
    path('admin/statistics/', admin_views.admin_statistics, name='admin_statistics'),
]
