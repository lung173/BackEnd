from django.db import models
from django.contrib.auth.models import User
from .models import Skill

class SkillEndorsement(models.Model):
    """Model untuk endorsement skill antar mahasiswa"""
    skill = models.ForeignKey(Skill, related_name='endorsements', on_delete=models.CASCADE)
    endorsed_by = models.ForeignKey(User, related_name='skill_endorsements_given', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['skill', 'endorsed_by']  # Satu user hanya bisa endorse 1x per skill
        ordering = ['-created_at']
        verbose_name = 'Skill Endorsement'
        verbose_name_plural = 'Skill Endorsements'
    
    def __str__(self):
        return f"{self.endorsed_by.username} endorsed {self.skill.nama}"
