from django.contrib import admin
from .models import Skill, SkillEndorsement

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['nama', 'mahasiswa', 'level', 'get_endorsement_count']
    list_filter = ['level']
    search_fields = ['nama', 'mahasiswa__nama']
    
    def get_endorsement_count(self, obj):
        return obj.endorsement_count()
    get_endorsement_count.short_description = 'Endorsements'


@admin.register(SkillEndorsement)
class SkillEndorsementAdmin(admin.ModelAdmin):
    list_display = ['skill', 'endorsed_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['skill__nama', 'endorsed_by__username']
    date_hierarchy = 'created_at'
