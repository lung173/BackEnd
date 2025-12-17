from rest_framework import serializers
from .models import Talent

class TalentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talent
        fields = '__all__'
