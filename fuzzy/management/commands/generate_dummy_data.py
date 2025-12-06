"""
Management Command untuk Generate Dummy Data

Menambahkan data kelompok dummy untuk testing aplikasi SPK Fuzzy Tahani.
Data ini berdasarkan contoh yang ada pada paper.

Penggunaan:
    python manage.py generate_dummy_data
"""

from django.core.management.base import BaseCommand
from datetime import date, timedelta
from fuzzy.models import Kelompok
import random


class Command(BaseCommand):
    help = 'Generate dummy data kelompok untuk testing SPK Fuzzy Tahani'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=15,
            help='Jumlah data dummy yang akan dibuat (default: 15)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua data kelompok sebelum generate'
        )
    
    def handle(self, *args, **options):
        count = options['count']
        clear = options['clear']
        
        if clear:
            Kelompok.objects.all().delete()
            self.stdout.write(self.style.WARNING('Semua data kelompok telah dihapus.'))
        
        # Data kelompok berdasarkan paper/contoh umum
        # Format: (nama, usia_tahun, jumlah_anggota, luas_lahan, frek_bantuan, sdm, unit_usaha, kas)
        sample_data = [
            ('Kelompok Tani Makmur', 5, 25, 2.5, 3, 7, 6, 8),
            ('Kelompok Tani Sejahtera', 3, 18, 1.8, 2, 6, 7, 6),
            ('Kelompok Tani Harapan', 7, 30, 3.0, 5, 8, 8, 7),
            ('Kelompok Tani Maju Jaya', 2, 12, 1.0, 1, 5, 5, 5),
            ('Kelompok Tani Subur', 4, 22, 2.0, 3, 7, 6, 6),
            ('Kelompok Tani Berkah', 1, 8, 0.5, 0, 4, 4, 4),
            ('Kelompok Tani Mandiri', 6, 28, 2.8, 4, 8, 7, 8),
            ('Kelompok Tani Sukses', 3, 15, 1.5, 2, 6, 6, 5),
            ('Kelompok Tani Bersatu', 8, 35, 3.5, 6, 9, 9, 9),
            ('Kelompok Tani Bangkit', 2, 10, 0.8, 1, 5, 4, 4),
            ('Kelompok Tani Sentosa', 4, 20, 2.2, 3, 7, 7, 7),
            ('Kelompok Tani Barokah', 5, 24, 2.3, 4, 7, 6, 6),
            ('Kelompok Tani Lestari', 6, 27, 2.7, 4, 8, 8, 7),
            ('Kelompok Tani Abadi', 1, 6, 0.4, 0, 3, 3, 3),
            ('Kelompok Tani Mulia', 3, 16, 1.6, 2, 6, 5, 6),
        ]
        
        # Tambahkan data random jika count lebih besar dari sample
        nama_depan = ['Kelompok Tani', 'Gapoktan', 'KWT', 'Kelompok Usaha']
        nama_belakang = ['Jaya', 'Makmur', 'Sejahtera', 'Maju', 'Berkah', 
                         'Mandiri', 'Sukses', 'Bersama', 'Tenteram', 'Damai',
                         'Harmoni', 'Gemilang', 'Ceria', 'Indah', 'Prima',
                         'Unggul', 'Andalan', 'Harum', 'Cemerlang', 'Bintang']
        
        created_count = 0
        today = date.today()
        
        for i in range(count):
            if i < len(sample_data):
                nama, usia, anggota, lahan, frek, sdm, unit, kas = sample_data[i]
            else:
                # Generate random data
                nama = f"{random.choice(nama_depan)} {random.choice(nama_belakang)} {i+1}"
                usia = random.randint(0, 10)
                anggota = random.randint(5, 40)
                lahan = round(random.uniform(0.3, 4.0), 2)
                frek = random.randint(0, 7)
                sdm = random.randint(1, 10)
                unit = random.randint(1, 10)
                kas = random.randint(1, 10)
            
            # Hitung tanggal berdiri berdasarkan usia
            tanggal_berdiri = today - timedelta(days=int(usia * 365.25))
            
            # Cek apakah nama sudah ada
            if not Kelompok.objects.filter(nama=nama).exists():
                Kelompok.objects.create(
                    nama=nama,
                    tanggal_berdiri=tanggal_berdiri,
                    jumlah_anggota=anggota,
                    luas_lahan=lahan,
                    frekuensi_bantuan=frek,
                    sdm=sdm,
                    unit_usaha=unit,
                    kas=kas,
                )
                created_count += 1
                self.stdout.write(f'  Created: {nama}')
            else:
                self.stdout.write(self.style.WARNING(f'  Skipped (exists): {nama}'))
        
        self.stdout.write(
            self.style.SUCCESS(f'\nBerhasil membuat {created_count} data kelompok dummy!')
        )
        self.stdout.write(
            f'Total data kelompok: {Kelompok.objects.count()}'
        )
