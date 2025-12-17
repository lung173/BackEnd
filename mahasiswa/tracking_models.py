"""
Additional models for tracking and analytics
"""
from django.db import models
from django.contrib.auth.models import User
from .models import Mahasiswa


class ProfileView(models.Model):
    """Track profile views for analytics - unique per user/session"""
    mahasiswa = models.ForeignKey(
        Mahasiswa, 
        related_name='profile_views', 
        on_delete=models.CASCADE
    )
    viewed_by_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="User who viewed (if authenticated)"
    )
    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Session identifier for anonymous users"
    )
    viewed_by_ip = models.GenericIPAddressField(
        null=True, 
        blank=True,
        help_text="IP address of viewer"
    )
    user_agent = models.TextField(blank=True, help_text="Browser user agent")
    referrer = models.URLField(blank=True, null=True, help_text="Referring URL")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Profile View'
        verbose_name_plural = 'Profile Views'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['mahasiswa', '-created_at']),
        ]
        # Ensure one view per user/session per profile
        constraints = [
            models.UniqueConstraint(
                fields=['mahasiswa', 'viewed_by_user'],
                condition=models.Q(viewed_by_user__isnull=False),
                name='unique_user_profile_view'
            ),
            models.UniqueConstraint(
                fields=['mahasiswa', 'session_key'],
                condition=models.Q(session_key__isnull=False),
                name='unique_session_profile_view'
            ),
        ]
    
    def __str__(self):
        viewer = self.viewed_by_user.username if self.viewed_by_user else self.viewed_by_ip
        return f"{self.mahasiswa.nama} viewed by {viewer}"
