#!/usr/bin/env python
"""
Script untuk test parameter fuzzy
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from fuzzy.models import FuzzyParameter
from fuzzy.utils import get_parameter_value, USIA_PARAMS

print("=" * 60)
print("TEST PARAMETER FUZZY")
print("=" * 60)

# Test 1: Check parameter default
print("\n1. Parameter Default (dari konstanta):")
print(f"   Usia Baru: {USIA_PARAMS['baru']}")

# Test 2: Check parameter dari fungsi get_parameter_value
print("\n2. Parameter dari get_parameter_value:")
param = get_parameter_value('usia', 'baru', USIA_PARAMS)
print(f"   Usia Baru: {param}")

# Test 3: Check jumlah parameter di database
count = FuzzyParameter.objects.count()
print(f"\n3. Jumlah parameter di database: {count}")

if count > 0:
    print("\n4. Sample parameter dari database:")
    for p in FuzzyParameter.objects.all()[:5]:
        print(f"   - {p}")
else:
    print("\n4. Database masih kosong. Jalankan inisialisasi parameter.")

# Test 4: Test membership function dengan parameter
from fuzzy.utils import mu_usia_baru

print("\n5. Test membership function:")
test_usia = 1.5
nilai = mu_usia_baru(test_usia)
print(f"   μ_usia_baru({test_usia}) = {nilai}")

print("\n" + "=" * 60)
print("TEST SELESAI")
print("=" * 60)
