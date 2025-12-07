"""
Forms untuk aplikasi SPK Fuzzy Database Model Tahani

File ini berisi form-form Django untuk:
1. CRUD data kelompok
2. Seleksi fuzzy (AND/OR)
"""

from django import forms
from .models import Kelompok
from .utils import VARIABEL_LIST, KATEGORI_VARIABEL


class KelompokForm(forms.ModelForm):
    """
    Form untuk menambah/mengedit data Kelompok
    
    Form ini menggunakan ModelForm untuk otomatis generate
    field berdasarkan model Kelompok.
    """
    
    class Meta:
        model = Kelompok
        fields = [
            'nama',
            'tanggal_berdiri',
            'jumlah_anggota',
            'luas_lahan',
            'frekuensi_bantuan',
            'sdm',
            'unit_usaha',
            'kas'
        ]
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama kelompok'
            }),
            'tanggal_berdiri': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'jumlah_anggota': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Jumlah anggota',
                'min': '0'
            }),
            'luas_lahan': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Luas lahan (Ha)',
                'step': '0.01',
                'min': '0'
            }),
            'frekuensi_bantuan': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Frekuensi bantuan',
                'min': '0'
            }),
            'sdm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Skor SDM (1-10)',
                'min': '1',
                'max': '10'
            }),
            'unit_usaha': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Skor Unit Usaha (1-10)',
                'min': '1',
                'max': '10'
            }),
            'kas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Skor Kas (1-10)',
                'min': '1',
                'max': '10'
            }),
        }
        labels = {
            'nama': 'Nama Kelompok',
            'tanggal_berdiri': 'Tanggal Berdiri',
            'jumlah_anggota': 'Jumlah Anggota',
            'luas_lahan': 'Luas Lahan (Ha)',
            'frekuensi_bantuan': 'Frekuensi Bantuan',
            'sdm': 'Kualitas SDM',
            'unit_usaha': 'Unit Usaha',
            'kas': 'Kas',
        }
    
    def clean_sdm(self):
        """Validasi skor SDM harus antara 1-10"""
        sdm = self.cleaned_data.get('sdm')
        if sdm is not None and (sdm < 1 or sdm > 10):
            raise forms.ValidationError('Skor SDM harus antara 1-10')
        return sdm
    
    def clean_unit_usaha(self):
        """Validasi skor unit usaha harus antara 1-10"""
        unit_usaha = self.cleaned_data.get('unit_usaha')
        if unit_usaha is not None and (unit_usaha < 1 or unit_usaha > 10):
            raise forms.ValidationError('Skor Unit Usaha harus antara 1-10')
        return unit_usaha
    
    def clean_kas(self):
        """Validasi skor kas harus antara 1-10"""
        kas = self.cleaned_data.get('kas')
        if kas is not None and (kas < 1 or kas > 10):
            raise forms.ValidationError('Skor Kas harus antara 1-10')
        return kas


class SeleksiFuzzyForm(forms.Form):
    """
    Form untuk seleksi fuzzy dengan 2 kriteria
    
    User dapat memilih:
    - Variabel 1 dan kategori 1
    - Variabel 2 dan kategori 2
    
    Operator (AND/OR) ditentukan dari URL, bukan dari form.
    """
    
    # Gabungkan semua kategori untuk validasi
    ALL_KATEGORI_CHOICES = []
    for var, kats in KATEGORI_VARIABEL.items():
        ALL_KATEGORI_CHOICES.extend(kats)
    
    variabel_1 = forms.ChoiceField(
        choices=VARIABEL_LIST,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'variabel_1'
        }),
        label='Variabel 1'
    )
    
    kategori_1 = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'kategori_1'
        }),
        label='Kategori 1'
    )
    
    variabel_2 = forms.ChoiceField(
        choices=VARIABEL_LIST,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'variabel_2'
        }),
        label='Variabel 2'
    )
    
    kategori_2 = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'kategori_2'
        }),
        label='Kategori 2'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Default to first variable's categories
        default_var = VARIABEL_LIST[0][0]
        default_choices = KATEGORI_VARIABEL.get(default_var, [])
        
        # If form is bound (POST), update choices based on selected variable
        if self.data:
            var1 = self.data.get('variabel_1', default_var)
            var2 = self.data.get('variabel_2', default_var)
            
            self.fields['kategori_1'].choices = KATEGORI_VARIABEL.get(var1, default_choices)
            self.fields['kategori_2'].choices = KATEGORI_VARIABEL.get(var2, default_choices)
        else:
            self.fields['kategori_1'].choices = default_choices
            self.fields['kategori_2'].choices = default_choices



class SeleksiFuzzyMultiForm(forms.Form):
    """
    Form untuk seleksi fuzzy dengan banyak kriteria
    
    User dapat memilih lebih dari 2 kriteria sekaligus.
    """
    
    OPERATOR_CHOICES = [
        ('AND', 'AND (Minimum)'),
        ('OR', 'OR (Maximum)'),
    ]
    
    operator = forms.ChoiceField(
        choices=OPERATOR_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Operator'
    )
    
    # Checkbox fields for each variable/category combination
    # These will be generated dynamically in the template
