from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from mahasiswa.models import Mahasiswa
from mahasiswa.serializers import MahasiswaSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_check(request):
    """Check if user is admin"""
    return Response({
        'is_admin': request.user.is_staff or request.user.is_superuser,
        'username': request.user.username
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_get_all_mahasiswa(request):
    """Get all mahasiswa profiles for admin"""
    mahasiswa = Mahasiswa.objects.all().select_related('user').prefetch_related('skills', 'pengalaman')
    
    # Filter by search query if provided
    search = request.GET.get('search', '')
    if search:
        mahasiswa = mahasiswa.filter(
            nama__icontains=search
        ) | mahasiswa.filter(
            nim__icontains=search
        ) | mahasiswa.filter(
            prodi__icontains=search
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        mahasiswa = mahasiswa.filter(is_active=True)
    elif status_filter == 'inactive':
        mahasiswa = mahasiswa.filter(is_active=False)
    
    # Order by
    order_by = request.GET.get('order_by', '-created_at')
    mahasiswa = mahasiswa.order_by(order_by)
    
    serializer = MahasiswaSerializer(mahasiswa, many=True)
    return Response({
        'count': mahasiswa.count(),
        'results': serializer.data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_toggle_mahasiswa_status(request, pk):
    """Toggle is_active status for a mahasiswa profile"""
    try:
        mahasiswa = Mahasiswa.objects.get(pk=pk)
        mahasiswa.is_active = not mahasiswa.is_active
        mahasiswa.save()
        
        return Response({
            'success': True,
            'is_active': mahasiswa.is_active,
            'message': f'Profile {"activated" if mahasiswa.is_active else "deactivated"} successfully'
        })
    except Mahasiswa.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_statistics(request):
    """Get admin dashboard statistics"""
    total_mahasiswa = Mahasiswa.objects.count()
    active_mahasiswa = Mahasiswa.objects.filter(is_active=True).count()
    inactive_mahasiswa = Mahasiswa.objects.filter(is_active=False).count()
    total_users = User.objects.count()
    
    from skills.models import Skill
    total_skills = Skill.objects.count()
    
    return Response({
        'total_mahasiswa': total_mahasiswa,
        'active_mahasiswa': active_mahasiswa,
        'inactive_mahasiswa': inactive_mahasiswa,
        'total_users': total_users,
        'total_skills': total_skills
    })
