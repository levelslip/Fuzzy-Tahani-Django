"""
Model Kelompok untuk SPK Fuzzy Database Model Tahani

Model ini menyimpan data kelompok yang akan dinilai menggunakan
metode Fuzzy Database Model Tahani untuk menentukan penerima
bantuan sosial.

Referensi: Paper "Sistem Pendukung Keputusan Pemilihan Penerima 
Bantuan Sosial Menggunakan Metode Fuzzy Database Model Tahani"
"""

from django.db import models
from django.utils import timezone
from datetime import date


class Kelompok(models.Model):
    """
    Model Kelompok
    
    Menyimpan data kelompok/organisasi yang akan dievaluasi
    untuk mendapatkan bantuan sosial.
    
    Attributes:
        nama (str): Nama kelompok
        tanggal_berdiri (date): Tanggal berdirinya kelompok
        jumlah_anggota (int): Jumlah anggota dalam kelompok
        luas_lahan (float): Luas lahan yang dimiliki (dalam hektar)
        frekuensi_bantuan (int): Jumlah bantuan yang pernah diterima
        sdm (int): Skor kualitas SDM (1-10)
        unit_usaha (int): Skor unit usaha (1-10)
        kas (int): Skor kas kelompok (1-10)
    """
    
    nama = models.CharField(
        max_length=200, 
        verbose_name="Nama Kelompok",
        help_text="Masukkan nama kelompok"
    )
    
    tanggal_berdiri = models.DateField(
        verbose_name="Tanggal Berdiri",
        help_text="Tanggal kelompok didirikan"
    )
    
    jumlah_anggota = models.IntegerField(
        verbose_name="Jumlah Anggota",
        help_text="Jumlah anggota dalam kelompok"
    )
    
    luas_lahan = models.FloatField(
        verbose_name="Luas Lahan (Ha)",
        help_text="Luas lahan yang dimiliki dalam hektar"
    )
    
    frekuensi_bantuan = models.IntegerField(
        verbose_name="Frekuensi Bantuan",
        help_text="Jumlah bantuan yang pernah diterima"
    )
    
    sdm = models.IntegerField(
        verbose_name="Kualitas SDM",
        help_text="Skor kualitas SDM (1-10)"
    )
    
    unit_usaha = models.IntegerField(
        verbose_name="Unit Usaha",
        help_text="Skor unit usaha (1-10)"
    )
    
    kas = models.IntegerField(
        verbose_name="Kas",
        help_text="Skor kas kelompok (1-10)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Kelompok"
        verbose_name_plural = "Kelompok"
        ordering = ['nama']
    
    def __str__(self):
        return self.nama
    
    @property
    def usia(self):
        """
        Menghitung usia kelompok dalam tahun
        
        Usia dihitung dari tanggal berdiri hingga hari ini.
        
        Returns:
            int: Usia kelompok dalam tahun
        """
        today = date.today()
        delta = today - self.tanggal_berdiri
        # Konversi ke tahun (365.25 untuk memperhitungkan tahun kabisat)
        return int(delta.days / 365.25)
    
    @property
    def usia_bulan(self):
        """
        Menghitung usia kelompok dalam bulan
        
        Returns:
            int: Usia kelompok dalam bulan
        """
        today = date.today()
        delta = today - self.tanggal_berdiri
        return int(delta.days / 30.44)  # Rata-rata hari per bulan
    
    def get_data_dict(self):
        """
        Mengembalikan data kelompok dalam bentuk dictionary
        
        Berguna untuk proses fuzzifikasi.
        
        Returns:
            dict: Data kelompok
        """
        return {
            'id': self.id,
            'nama': self.nama,
            'usia': self.usia,
            'jumlah_anggota': self.jumlah_anggota,
            'luas_lahan': self.luas_lahan,
            'frekuensi_bantuan': self.frekuensi_bantuan,
            'sdm': self.sdm,
            'unit_usaha': self.unit_usaha,
            'kas': self.kas,
        }
