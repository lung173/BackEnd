"""
Script untuk test koneksi database
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pusat.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from mahasiswa.models import Mahasiswa

print("=" * 50)
print("TEST KONEKSI DATABASE")
print("=" * 50)

try:
    # Test koneksi
    connection.ensure_connection()
    print("✅ DATABASE CONNECTED!")
    print()
    
    # Info database
    print(f"Database: {connection.settings_dict['NAME']}")
    print(f"Host: {connection.settings_dict['HOST']}")
    print(f"Port: {connection.settings_dict['PORT']}")
    print(f"User: {connection.settings_dict['USER']}")
    print()
    
    # Test query
    print("=" * 50)
    print("DATA DI DATABASE:")
    print("=" * 50)
    
    user_count = User.objects.count()
    print(f"Total Users: {user_count}")
    
    mahasiswa_count = Mahasiswa.objects.count()
    print(f"Total Mahasiswa: {mahasiswa_count}")
    
    if mahasiswa_count > 0:
        print("\nMahasiswa Terbaru:")
        for mhs in Mahasiswa.objects.all()[:5]:
            print(f"  - {mhs.nama} ({mhs.nim})")
    
    print()
    print("=" * 50)
    print("✅ SEMUA TEST BERHASIL!")
    print("=" * 50)
    
except Exception as e:
    print("❌ ERROR:", str(e))
    sys.exit(1)
