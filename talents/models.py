from django.db import models
from mahasiswa.models import Mahasiswa

class Talent(models.Model):
    """Model untuk portfolio/pengalaman mahasiswa"""
    mahasiswa = models.ForeignKey(Mahasiswa, related_name='talents', on_delete=models.CASCADE)
    judul = models.CharField(max_length=200, help_text="Judul project/pengalaman")
    deskripsi = models.TextField(help_text="Deskripsi detail")
    kategori = models.CharField(max_length=100, blank=True, help_text="Contoh: Project, Internship, Competition, etc")
    link_portfolio = models.URLField(blank=True, null=True, help_text="Link ke portfolio/demo")
    gambar = models.ImageField(upload_to='talents/', blank=True, null=True, help_text="Screenshot/gambar project")
    tanggal_mulai = models.DateField(blank=True, null=True)
    tanggal_selesai = models.DateField(blank=True, null=True, help_text="Kosongkan jika masih berlangsung")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Talent/Portfolio'
        verbose_name_plural = 'Talents/Portfolio'

    def __str__(self):
        return f"{self.judul} - {self.mahasiswa.nama}"
