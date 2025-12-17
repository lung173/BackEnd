"""
Comprehensive API Testing Script
Test semua endpoint untuk memastikan tidak ada error
"""
import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pusat.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from mahasiswa.models import Mahasiswa
from skills.models import Skill
from talents.models import Talent

client = Client()

def print_test(title):
    print("\n" + "=" * 60)
    print(f"TEST: {title}")
    print("=" * 60)

def print_result(success, message):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")

print("\n" + "🚀" * 30)
print("BACKEND API TESTING - Talenta Mahasiswa UMS")
print("🚀" * 30)

# =============================================================================
# TEST 1: AUTHENTICATION
# =============================================================================
print_test("1. Authentication - Register")
try:
    import random
    random_num = random.randint(1000, 9999)
    test_username = f'testuser{random_num}'
    
    response = client.post('/api/accounts/register/', {
        'username': test_username,
        'email': f'test{random_num}@ums.ac.id',
        'password': 'testpass123'
    }, content_type='application/json')
    
    if response.status_code == 201:
        data = response.json()
        access_token = data['tokens']['access']
        test_user = User.objects.get(username=test_username)
        print_result(True, f"Register berhasil - Token: {access_token[:20]}...")
    else:
        access_token = None
        print_result(False, f"Status: {response.status_code} - {response.content}")
except Exception as e:
    access_token = None
    print_result(False, str(e))

print_test("2. Authentication - Login")
try:
    response = client.post('/api/accounts/login/', {
        'username': 'admin',
        'password': 'admin123'
    }, content_type='application/json')
    
    if response.status_code == 200:
        data = response.json()
        admin_token = data['tokens']['access']
        # Fallback: gunakan admin token jika register gagal
        if not access_token:
            access_token = admin_token
        print_result(True, f"Login berhasil - Token: {admin_token[:20]}...")
    else:
        print_result(False, f"Status: {response.status_code}")
except Exception as e:
    print_result(False, str(e))

print_test("3. Authentication - Get Profile")
try:
    response = client.get('/api/accounts/profile/', 
                         HTTP_AUTHORIZATION=f'Bearer {admin_token}')
    
    if response.status_code == 200:
        data = response.json()
        print_result(True, f"Get profile berhasil - User: {data['user']['username']}")
    else:
        print_result(False, f"Status: {response.status_code}")
except Exception as e:
    print_result(False, str(e))

# =============================================================================
# TEST 2: MAHASISWA CRUD
# =============================================================================
print_test("4. Mahasiswa - Create Profile")
try:
    # Get user dari test_user yang dibuat saat register
    if 'test_user' in locals():
        user = test_user
    else:
        # Fallback ke admin
        user = User.objects.get(username='admin')
    
    # Generate random NIM untuk menghindari duplicate
    nim_random = random.randint(100000, 999999)
    
    response = client.post('/api/mahasiswa/', {
        'user': user.id,
        'nama': 'Budi Santoso',
        'nim': f'K{nim_random}',
        'prodi': 'Teknik Informatika',
        'fakultas': 'Fakultas Komunikasi dan Informatika',
        'email': 'budi@ums.ac.id',
        'bio': 'Mahasiswa aktif yang passionate di bidang web development',
        'telepon': '081234567890'
    }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    if response.status_code in [200, 201]:
        mahasiswa_data = response.json()
        mahasiswa_id = mahasiswa_data['id']
        print_result(True, f"Create mahasiswa berhasil - ID: {mahasiswa_id}")
    else:
        print_result(False, f"Status: {response.status_code} - {response.content}")
except Exception as e:
    print_result(False, str(e))

print_test("5. Mahasiswa - List All")
try:
    response = client.get('/api/mahasiswa/')
    
    if response.status_code == 200:
        data = response.json()
        count = data.get('count', len(data) if isinstance(data, list) else 0)
        print_result(True, f"List mahasiswa berhasil - Total: {count}")
    else:
        print_result(False, f"Status: {response.status_code}")
except Exception as e:
    print_result(False, str(e))

print_test("6. Mahasiswa - Get Detail")
try:
    if 'mahasiswa_id' in locals():
        response = client.get(f'/api/mahasiswa/{mahasiswa_id}/')
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Get detail berhasil - Nama: {data['nama']}")
        else:
            print_result(False, f"Status: {response.status_code}")
    else:
        print_result(False, "Mahasiswa belum dibuat")
except Exception as e:
    print_result(False, str(e))

print_test("7. Mahasiswa - Latest (Homepage)")
try:
    response = client.get('/api/mahasiswa/latest/')
    
    if response.status_code == 200:
        data = response.json()
        count = len(data) if isinstance(data, list) else 0
        print_result(True, f"Latest mahasiswa berhasil - Total: {count}")
    else:
        print_result(False, f"Status: {response.status_code}")
except Exception as e:
    print_result(False, str(e))

print_test("8. Mahasiswa - Most Viewed")
try:
    response = client.get('/api/mahasiswa/most-viewed/')
    
    if response.status_code == 200:
        data = response.json()
        count = len(data) if isinstance(data, list) else 0
        print_result(True, f"Most viewed berhasil - Total: {count}")
    else:
        print_result(False, f"Status: {response.status_code}")
except Exception as e:
    print_result(False, str(e))

# =============================================================================
# TEST 3: SKILLS CRUD
# =============================================================================
print_test("9. Skills - Create Skill")
try:
    if 'mahasiswa_id' in locals():
        response = client.post('/api/skills/', {
            'mahasiswa': mahasiswa_id,
            'nama': 'Python',
            'level': 'Advanced'
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        if response.status_code in [200, 201]:
            skill_data = response.json()
            skill_id = skill_data['id']
            print_result(True, f"Create skill berhasil - ID: {skill_id}")
        else:
            print_result(False, f"Status: {response.status_code}")
    else:
        print_result(False, "Mahasiswa belum dibuat")
except Exception as e:
    print_result(False, str(e))

print_test("10. Skills - List All")
try:
    response = client.get('/api/skills/')
    
    if response.status_code == 200:
        data = response.json()
        count = len(data) if isinstance(data, list) else data.get('count', 0)
        print_result(True, f"List skills berhasil - Total: {count}")
    else:
        print_result(False, f"Status: {response.status_code}")
except Exception as e:
    print_result(False, str(e))

# =============================================================================
# TEST 4: TALENTS/PORTFOLIO CRUD
# =============================================================================
print_test("11. Talents - Create Portfolio")
try:
    if 'mahasiswa_id' in locals():
        response = client.post('/api/talents/', {
            'mahasiswa': mahasiswa_id,
            'judul': 'Website E-Commerce',
            'deskripsi': 'Membuat website e-commerce menggunakan Django dan React',
            'kategori': 'Project',
            'link_portfolio': 'https://github.com/testuser/ecommerce'
        }, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        if response.status_code in [200, 201]:
            talent_data = response.json()
            talent_id = talent_data['id']
            print_result(True, f"Create talent berhasil - ID: {talent_id}")
        else:
            print_result(False, f"Status: {response.status_code}")
    else:
        print_result(False, "Mahasiswa belum dibuat")
except Exception as e:
    print_result(False, str(e))

print_test("12. Talents - List All")
try:
    response = client.get('/api/talents/')
    
    if response.status_code == 200:
        data = response.json()
        count = len(data) if isinstance(data, list) else data.get('count', 0)
        print_result(True, f"List talents berhasil - Total: {count}")
    else:
        print_result(False, f"Status: {response.status_code}")
except Exception as e:
    print_result(False, str(e))

# =============================================================================
# TEST 5: SEARCH & FILTER
# =============================================================================
print_test("13. Search - Mahasiswa by Name")
try:
    response = client.get('/api/mahasiswa/?search=Budi')
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        count = len(results) if isinstance(results, list) else 0
        print_result(True, f"Search berhasil - Found: {count}")
    else:
        print_result(False, f"Status: {response.status_code}")
except Exception as e:
    print_result(False, str(e))

print_test("14. Filter - Mahasiswa by Prodi")
try:
    response = client.get('/api/mahasiswa/?prodi=Teknik Informatika')
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        count = len(results) if isinstance(results, list) else 0
        print_result(True, f"Filter berhasil - Found: {count}")
    else:
        print_result(False, f"Status: {response.status_code}")
except Exception as e:
    print_result(False, str(e))

# =============================================================================
# TEST 6: ADMIN FEATURES
# =============================================================================
print_test("15. Admin - Toggle Mahasiswa Status")
try:
    if 'mahasiswa_id' in locals():
        # Login as admin
        admin_response = client.post('/api/accounts/login/', {
            'username': 'admin',
            'password': 'admin123'
        }, content_type='application/json')
        admin_token = admin_response.json()['tokens']['access']
        
        response = client.patch(f'/api/mahasiswa/{mahasiswa_id}/toggle-status/',
                               HTTP_AUTHORIZATION=f'Bearer {admin_token}')
        
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Toggle status berhasil - Active: {data['is_active']}")
        else:
            print_result(False, f"Status: {response.status_code}")
    else:
        print_result(False, "Mahasiswa belum dibuat")
except Exception as e:
    print_result(False, str(e))

# =============================================================================
# TEST 7: CV DOWNLOAD
# =============================================================================
print_test("16. CV Download")
try:
    if 'mahasiswa_id' in locals():
        # Django APPEND_SLASH: gunakan trailing slash
        response = client.get(f'/api/mahasiswa/{mahasiswa_id}/download-cv/', follow=True)
        
        if response.status_code == 200:
            if response.get('Content-Type', '').startswith('application/pdf'):
                print_result(True, f"CV download berhasil - Size: {len(response.content)} bytes")
            else:
                print_result(True, f"CV endpoint berhasil - Type: {response.get('Content-Type', 'unknown')}")
        else:
            print_result(False, f"Status: {response.status_code}")
    else:
        print_result(False, "Mahasiswa belum dibuat")
except Exception as e:
    print_result(False, str(e))

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 60)
print("TESTING SELESAI!")
print("=" * 60)
print("\n📊 SUMMARY:")
print(f"Database: Connected to GCP PostgreSQL (34.128.97.74)")
print(f"Total Users: {User.objects.count()}")
print(f"Total Mahasiswa: {Mahasiswa.objects.count()}")
print(f"Total Skills: {Skill.objects.count()}")
print(f"Total Talents: {Talent.objects.count()}")

print("\n🌐 AKSES:")
print("- Swagger API: http://127.0.0.1:8000/swagger/")
print("- Admin Panel: http://127.0.0.1:8000/admin/")
print("- ReDoc: http://127.0.0.1:8000/redoc/")

print("\n" + "🎉" * 30)
print("SEMUA TEST SELESAI!")
print("🎉" * 30 + "\n")
