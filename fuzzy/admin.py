"""
Admin Configuration untuk SPK Fuzzy Database Model Tahani

File ini mengkonfigurasi tampilan model di Django Admin.
"""

from django.contrib import admin
from .models import Kelompok, FuzzyParameter


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


@admin.register(FuzzyParameter)
class FuzzyParameterAdmin(admin.ModelAdmin):
    """
    Konfigurasi Admin untuk Model FuzzyParameter
    
    Menampilkan dan mengelola parameter membership function.
    """
    
    # Kolom yang ditampilkan di list view
    list_display = [
        'get_parameter_name',
        'variabel',
        'kategori',
        'tipe_fungsi',
        'param_a',
        'param_b',
        'param_c',
        'updated_at',
    ]
    
    # Field yang bisa dicari
    search_fields = ['variabel', 'kategori', 'keterangan']
    
    # Filter di sidebar
    list_filter = [
        'variabel',
        'tipe_fungsi',
    ]
    
    # Urutan default
    ordering = ['variabel', 'kategori']
    
    # Field yang readonly
    readonly_fields = ['created_at', 'updated_at']
    
    # Organisasi field di form edit
    fieldsets = (
        ('Identifikasi', {
            'fields': ('variabel', 'kategori', 'tipe_fungsi')
        }),
        ('Parameter Fungsi Keanggotaan', {
            'fields': ('param_a', 'param_b', 'param_c'),
            'description': 'Parameter A dan B wajib diisi. Parameter C hanya untuk fungsi segitiga.'
        }),
        ('Informasi Tambahan', {
            'fields': ('keterangan',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_parameter_name(self, obj):
        """Menampilkan nama parameter lengkap"""
        return str(obj)
    get_parameter_name.short_description = 'Parameter'

