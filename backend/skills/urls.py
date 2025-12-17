from django.urls import path
from . import views

urlpatterns = [
    path('', views.SkillListCreateView.as_view(), name='skill-list'),
    path('<int:pk>/', views.SkillDetailView.as_view(), name='skill-detail'),
    path('<int:pk>/endorse/', views.endorse_skill, name='skill-endorse'),
    path('<int:pk>/remove-endorsement/', views.remove_endorsement, name='skill-remove-endorsement'),
]
