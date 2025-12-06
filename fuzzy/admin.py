"""
Admin Configuration untuk SPK Fuzzy Database Model Tahani

File ini mengkonfigurasi tampilan model di Django Admin.
"""

from django.contrib import admin
from .models import Kelompok


@admin.register(Kelompok)
class KelompokAdmin(admin.ModelAdmin):
    """
    Konfigurasi Admin untuk Model Kelompok
    
    Menampilkan data kelompok dengan field yang relevan
    dan fitur pencarian serta filter.
    """
    
    # Kolom yang ditampilkan di list view
    list_display = [
        'nama',
        'tanggal_berdiri',
        'get_usia',
        'jumlah_anggota',
        'luas_lahan',
        'frekuensi_bantuan',
        'sdm',
        'unit_usaha',
        'kas',
        'created_at',
    ]
    
    # Field yang bisa dicari
    search_fields = ['nama']
    
    # Filter di sidebar
    list_filter = [
        'tanggal_berdiri',
        'frekuensi_bantuan',
        'sdm',
        'unit_usaha',
        'kas',
    ]
    
    # Urutan default
    ordering = ['nama']
    
    # Field yang readonly
    readonly_fields = ['created_at', 'updated_at']
    
    # Organisasi field di form edit
    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('nama', 'tanggal_berdiri', 'jumlah_anggota', 'luas_lahan', 'frekuensi_bantuan')
        }),
        ('Skor Penilaian', {
            'fields': ('sdm', 'unit_usaha', 'kas')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_usia(self, obj):
        """Menampilkan usia kelompok dalam tahun"""
        return f"{obj.usia} tahun"
    get_usia.short_description = 'Usia'
    get_usia.admin_order_field = 'tanggal_berdiri'
