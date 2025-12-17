from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Skill, SkillEndorsement
from .serializers import SkillSerializer, SkillEndorsementSerializer

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def endorse_skill(request, pk):
    """Endorse a skill - mahasiswa can endorse other students' skills"""
    try:
        skill = Skill.objects.get(pk=pk)
    except Skill.DoesNotExist:
        return Response({'error': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Prevent self-endorsement
    try:
        if skill.mahasiswa.user == request.user:
            return Response({
                'error': 'Cannot endorse your own skill',
                'detail': 'You cannot endorse your own skills'
            }, status=status.HTTP_400_BAD_REQUEST)
    except:
        pass  # User doesn't have mahasiswa profile, allow endorsement
    
    # Create or check existing endorsement
    endorsement, created = SkillEndorsement.objects.get_or_create(
        skill=skill,
        endorsed_by=request.user
    )
    
    if not created:
        return Response({
            'message': 'Already endorsed',
            'detail': 'You have already endorsed this skill'
        }, status=status.HTTP_200_OK)
    
    serializer = SkillEndorsementSerializer(endorsement)
    return Response({
        'message': 'Skill endorsed successfully',
        'endorsement': serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_endorsement(request, pk):
    """Remove endorsement from a skill"""
    try:
        skill = Skill.objects.get(pk=pk)
        endorsement = SkillEndorsement.objects.get(skill=skill, endorsed_by=request.user)
        endorsement.delete()
        return Response({'message': 'Endorsement removed'}, status=status.HTTP_200_OK)
    except Skill.DoesNotExist:
        return Response({'error': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)
    except SkillEndorsement.DoesNotExist:
        return Response({'error': 'Endorsement not found'}, status=status.HTTP_404_NOT_FOUND)

