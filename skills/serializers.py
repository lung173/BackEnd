from rest_framework import serializers
from .models import Skill, SkillEndorsement

class SkillEndorsementSerializer(serializers.ModelSerializer):
    endorsed_by_username = serializers.CharField(source='endorsed_by.username', read_only=True)
    
    class Meta:
        model = SkillEndorsement
        fields = ['id', 'skill', 'endorsed_by', 'endorsed_by_username', 'created_at']
        read_only_fields = ['endorsed_by', 'created_at']


class SkillSerializer(serializers.ModelSerializer):
    endorsement_count = serializers.SerializerMethodField()
    endorsements = SkillEndorsementSerializer(many=True, read_only=True)
    
    def get_endorsement_count(self, obj):
        return obj.endorsement_count()
    
    class Meta:
        model = Skill
        fields = ['id', 'mahasiswa', 'nama', 'level', 'endorsement_count', 'endorsements']