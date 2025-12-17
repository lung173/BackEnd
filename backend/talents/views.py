from rest_framework import generics
from .models import Talent
from .serializers import TalentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class TalentListCreateView(generics.ListCreateAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class TalentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Talent.objects.all()
    serializer_class = TalentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
