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


class FuzzyParameter(models.Model):
    """
    Model untuk menyimpan parameter-parameter membership function
    
    Model ini memungkinkan pengguna untuk mengatur parameter fuzzy
    secara dinamis tanpa perlu mengubah kode.
    
    Attributes:
        variabel (str): Nama variabel (usia, frekuensi_bantuan, dll)
        kategori (str): Kategori fuzzy (baru, sedang, lama, dll)
        tipe_fungsi (str): Tipe fungsi (bahu_kiri, segitiga, bahu_kanan)
        param_a (float): Parameter a
        param_b (float): Parameter b
        param_c (float): Parameter c (opsional, untuk fungsi segitiga)
        keterangan (str): Keterangan parameter
    """
    
    VARIABEL_CHOICES = [
        ('usia', 'Usia'),
        ('frekuensi_bantuan', 'Frekuensi Bantuan'),
        ('luas_lahan', 'Luas Lahan'),
        ('jumlah_anggota', 'Jumlah Anggota'),
        ('sdm', 'SDM'),
        ('unit_usaha', 'Unit Usaha'),
        ('kas', 'Kas'),
    ]
    
    TIPE_FUNGSI_CHOICES = [
        ('bahu_kiri', 'Bahu Kiri (Left Shoulder)'),
        ('segitiga', 'Segitiga (Triangle)'),
        ('bahu_kanan', 'Bahu Kanan (Right Shoulder)'),
    ]
    
    variabel = models.CharField(
        max_length=50,
        choices=VARIABEL_CHOICES,
        verbose_name="Variabel"
    )
    
    kategori = models.CharField(
        max_length=50,
        verbose_name="Kategori",
        help_text="Contoh: baru, sedang, lama"
    )
    
    tipe_fungsi = models.CharField(
        max_length=20,
        choices=TIPE_FUNGSI_CHOICES,
        verbose_name="Tipe Fungsi"
    )
    
    param_a = models.FloatField(
        verbose_name="Parameter A",
        help_text="Batas bawah atau titik awal"
    )
    
    param_b = models.FloatField(
        verbose_name="Parameter B",
        help_text="Titik tengah atau batas atas"
    )
    
    param_c = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Parameter C",
        help_text="Batas atas (hanya untuk fungsi segitiga)"
    )
    
    keterangan = models.TextField(
        blank=True,
        verbose_name="Keterangan",
        help_text="Penjelasan tentang parameter ini"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Parameter Fuzzy"
        verbose_name_plural = "Parameter Fuzzy"
        ordering = ['variabel', 'kategori']
        unique_together = ['variabel', 'kategori']
    
    def __str__(self):
        return f"{self.get_variabel_display()} - {self.kategori}"
    
    def get_params_dict(self):
        """
        Mengembalikan parameter dalam bentuk dictionary
        
        Returns:
            dict: Dictionary parameter sesuai format utils.py
        """
        params = {
            'a': self.param_a,
            'b': self.param_b,
        }
        if self.param_c is not None:
            params['c'] = self.param_c
        return params
