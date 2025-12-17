from django.contrib import admin
from .models import Talent

@admin.register(Talent)
class TalentAdmin(admin.ModelAdmin):
    list_display = ['judul', 'mahasiswa']
    search_fields = ['judul', 'deskripsi', 'mahasiswa__nama']
