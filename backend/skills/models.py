from django.db import models
from django.contrib.auth.models import User
from mahasiswa.models import Mahasiswa

class Skill(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, related_name='skills', on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    level = models.CharField(max_length=50, blank=True)  # contoh: Beginner, Intermediate, Expert

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.nama} ({self.mahasiswa.nama})"
    
    def endorsement_count(self):
        """Count total endorsements for this skill"""
        return self.endorsements.count()


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