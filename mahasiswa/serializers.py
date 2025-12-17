from rest_framework import serializers
from .models import Mahasiswa, Pengalaman
from skills.serializers import SkillSerializer
from talents.serializers import TalentSerializer


class PengalamanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengalaman
        fields = ['id', 'posisi', 'organisasi', 'tahun_mulai', 'tahun_selesai', 'deskripsi']


class MahasiswaSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    talents = TalentSerializer(many=True, read_only=True)
    pengalaman = PengalamanSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Mahasiswa
        fields = [
            'id', 'user', 'username', 'nama', 'nim', 'prodi', 'angkatan', 'fakultas',
            'email', 'telepon', 'alamat', 'foto_profil', 'bio', 'tanggal_lahir', 'is_active',
            'linkedin', 'github', 'instagram', 'website',
            'skills', 'pengalaman', 'talents', 'views_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'views_count', 'created_at', 'updated_at']
        extra_kwargs = {
            'nama': {'required': False},
            'nim': {'required': False},
            'prodi': {'required': False},
            'email': {'required': False},
        }
    
    def validate_nim(self, value):
        """Skip NIM validation if updating own profile"""
        # Skip if NIM not provided (partial update)
        if not value:
            return value
            
        # If this is an update (instance exists)
        if self.instance:
            # If NIM hasn't changed, skip validation
            if self.instance.nim == value:
                return value
        
        # Check if NIM already exists for different user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            existing = Mahasiswa.objects.filter(nim=value).exclude(user=request.user).first()
            if existing:
                raise serializers.ValidationError('NIM ini sudah digunakan oleh mahasiswa lain.')
        else:
            # For create without auth context, check globally
            if Mahasiswa.objects.filter(nim=value).exists():
                raise serializers.ValidationError('NIM ini sudah terdaftar.')
        
        return value
    
    def __init__(self, *args, **kwargs):
        """Override init to make all fields optional for updates"""
        super().__init__(*args, **kwargs)
        
        # If this is an update (instance exists), make ALL fields optional
        if self.instance is not None:
            for field_name, field in self.fields.items():
                field.required = False
                # Only set allow_blank for fields that support it (CharField, TextField, etc.)
                if hasattr(field, 'allow_blank'):
                    field.allow_blank = True
    
    def validate(self, data):
        """Custom validation - require fields only on CREATE"""
        # If this is an update (instance exists), skip required field validation
        if self.instance:
            return data
            
        # If this is a create operation (no instance), require basic fields
        required_fields = ['nama', 'nim', 'prodi', 'email']
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            raise serializers.ValidationError({
                field: ['Bidang ini harus diisi.'] for field in missing
            })
        return data

class MahasiswaListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    skills_count = serializers.SerializerMethodField()
    talents_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Mahasiswa
        fields = [
            'id', 'nama', 'nim', 'prodi', 'angkatan', 'fakultas', 'email',
            'foto_profil', 'bio', 'is_active', 'skills_count', 
            'talents_count', 'views_count', 'created_at'
        ]
    
    def get_skills_count(self, obj):
        return obj.skills.count()
    
    def get_talents_count(self, obj):
        return obj.talents.count()