from django.urls import path
from . import views

urlpatterns = [
    path('', views.TalentListCreateView.as_view(), name='talent-list'),
    path('<int:pk>/', views.TalentDetailView.as_view(), name='talent-detail'),
]
