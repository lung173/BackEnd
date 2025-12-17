from django.urls import path
from . import views
from .cv_generator import download_cv

urlpatterns = [
    path('', views.MahasiswaListCreateView.as_view(), name='mahasiswa-list'),
    path('latest/', views.MahasiswaLatestView.as_view(), name='mahasiswa-latest'),
    path('most-viewed/', views.MahasiswaMostViewedView.as_view(), name='mahasiswa-most-viewed'),
    path('my-profile/', views.get_current_user_profile, name='my-profile'),
    path('profile-completion/', views.profile_completion_status, name='profile-completion'),
    path('<int:pk>/download-cv/', download_cv, name='mahasiswa-download-cv'),
    path('<int:pk>/qr-code/', views.generate_qr_code, name='mahasiswa-qr-code'),
    path('<int:pk>/view/', views.track_profile_view, name='mahasiswa-track-view'),
    path('<int:pk>/recommendations/', views.get_recommendations, name='mahasiswa-recommendations'),
    path('<int:pk>/toggle-status/', views.toggle_mahasiswa_status, name='mahasiswa-toggle-status'),
    path('<int:pk>/', views.MahasiswaDetailView.as_view(), name='mahasiswa-detail'),
]