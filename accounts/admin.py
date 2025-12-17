from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_mahasiswa', 'is_admin']
    list_filter = ['is_mahasiswa', 'is_admin']
    search_fields = ['user__username', 'user__email']