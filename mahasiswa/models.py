from django.db import models
from django.contrib.auth.models import User

class Mahasiswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mahasiswa_profile')
    nama = models.CharField(max_length=100)
    nim = models.CharField(max_length=20, unique=True)
    prodi = models.CharField(max_length=100)
    angkatan = models.CharField(max_length=10, blank=True, help_text="Tahun angkatan")
    fakultas = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    telepon = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)
    foto_profil = models.ImageField(upload_to='profil/', blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Deskripsi singkat tentang diri")
    tanggal_lahir = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Profil aktif/nonaktif")
    
    # Social media links
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True, help_text="Personal website/portfolio")
    
    # Statistics
    views_count = models.IntegerField(default=0, help_text="Jumlah profile views")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mahasiswa'
        verbose_name_plural = 'Mahasiswa'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['prodi']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.nama} ({self.nim})"
    
    def increment_views(self):
        """Increment profile view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Pengalaman(models.Model):
    """Model untuk pengalaman kerja/magang mahasiswa"""
    mahasiswa = models.ForeignKey(Mahasiswa, related_name='pengalaman', on_delete=models.CASCADE)
    posisi = models.CharField(max_length=200, help_text="Posisi/jabatan")
    organisasi = models.CharField(max_length=200, help_text="Nama perusahaan/organisasi")
    tahun_mulai = models.CharField(max_length=10, help_text="Tahun mulai")
    tahun_selesai = models.CharField(max_length=10, blank=True, help_text="Tahun selesai (kosong jika masih berlangsung)")
    deskripsi = models.TextField(blank=True, help_text="Deskripsi pengalaman")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-tahun_mulai']
        verbose_name = 'Pengalaman'
        verbose_name_plural = 'Pengalaman'
    
    def __str__(self):
        return f"{self.posisi} at {self.organisasi} ({self.mahasiswa.nama})"


class ProfileView(models.Model):
    """Track unique profile views per user/session"""
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
        viewer = self.viewed_by_user.username if self.viewed_by_user else self.session_key[:8] if self.session_key else self.viewed_by_ip
        return f"{self.mahasiswa.nama} viewed by {viewer}"