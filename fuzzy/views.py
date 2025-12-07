"""
Views untuk aplikasi SPK Fuzzy Database Model Tahani

File ini berisi semua view untuk:
1. Dashboard
2. CRUD data kelompok
3. Seleksi fuzzy AND
4. Seleksi fuzzy OR
5. Fuzzifikasi detail
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Avg

from .models import Kelompok
from .forms import KelompokForm, SeleksiFuzzyForm
from .utils import (
    seleksi_fuzzy,
    hitung_fuzzifikasi_lengkap,
    VARIABEL_LIST,
    KATEGORI_VARIABEL,
    get_all_membership_values
)


# =============================================================================
# DASHBOARD
# =============================================================================

def dashboard(request):
    """
    Halaman Dashboard
    
    Menampilkan:
    - Jumlah total kelompok
    - Statistik rata-rata
    - Data kelompok terbaru
    """
    kelompok_list = Kelompok.objects.all()
    total_kelompok = kelompok_list.count()
    
    # Hitung statistik
    statistik = {
        'total': total_kelompok,
        'avg_anggota': kelompok_list.aggregate(Avg('jumlah_anggota'))['jumlah_anggota__avg'] or 0,
        'avg_lahan': kelompok_list.aggregate(Avg('luas_lahan'))['luas_lahan__avg'] or 0,
        'avg_sdm': kelompok_list.aggregate(Avg('sdm'))['sdm__avg'] or 0,
        'avg_unit_usaha': kelompok_list.aggregate(Avg('unit_usaha'))['unit_usaha__avg'] or 0,
        'avg_kas': kelompok_list.aggregate(Avg('kas'))['kas__avg'] or 0,
    }
    
    # Kelompok terbaru (5 terakhir)
    kelompok_terbaru = kelompok_list.order_by('-created_at')[:5]
    
    context = {
        'title': 'Dashboard',
        'statistik': statistik,
        'kelompok_terbaru': kelompok_terbaru,
    }
    
    return render(request, 'fuzzy/dashboard.html', context)


# =============================================================================
# CRUD KELOMPOK
# =============================================================================

def kelompok_list(request):
    """
    Halaman Daftar Kelompok
    
    Menampilkan semua data kelompok dalam bentuk tabel.
    """
    kelompok_list = Kelompok.objects.all().order_by('nama')
    
    context = {
        'title': 'Data Kelompok',
        'kelompok_list': kelompok_list,
    }
    
    return render(request, 'fuzzy/kelompok_list.html', context)


def kelompok_add(request):
    """
    Halaman Tambah Kelompok
    
    Form untuk menambahkan data kelompok baru.
    """
    if request.method == 'POST':
        form = KelompokForm(request.POST)
        if form.is_valid():
            kelompok = form.save()
            messages.success(request, f'Kelompok "{kelompok.nama}" berhasil ditambahkan!')
            return redirect('kelompok_list')
        else:
            messages.error(request, 'Terjadi kesalahan. Periksa kembali data yang dimasukkan.')
    else:
        form = KelompokForm()
    
    context = {
        'title': 'Tambah Kelompok',
        'form': form,
        'action': 'Tambah',
    }
    
    return render(request, 'fuzzy/kelompok_form.html', context)


def kelompok_edit(request, pk):
    """
    Halaman Edit Kelompok
    
    Form untuk mengedit data kelompok yang sudah ada.
    
    Args:
        pk (int): Primary key kelompok yang akan diedit
    """
    kelompok = get_object_or_404(Kelompok, pk=pk)
    
    if request.method == 'POST':
        form = KelompokForm(request.POST, instance=kelompok)
        if form.is_valid():
            form.save()
            messages.success(request, f'Kelompok "{kelompok.nama}" berhasil diperbarui!')
            return redirect('kelompok_list')
        else:
            messages.error(request, 'Terjadi kesalahan. Periksa kembali data yang dimasukkan.')
    else:
        form = KelompokForm(instance=kelompok)
    
    context = {
        'title': f'Edit Kelompok: {kelompok.nama}',
        'form': form,
        'kelompok': kelompok,
        'action': 'Simpan',
    }
    
    return render(request, 'fuzzy/kelompok_form.html', context)


def kelompok_delete(request, pk):
    """
    Hapus Kelompok
    
    Menghapus data kelompok berdasarkan primary key.
    
    Args:
        pk (int): Primary key kelompok yang akan dihapus
    """
    kelompok = get_object_or_404(Kelompok, pk=pk)
    nama = kelompok.nama
    
    if request.method == 'POST':
        kelompok.delete()
        messages.success(request, f'Kelompok "{nama}" berhasil dihapus!')
        return redirect('kelompok_list')
    
    context = {
        'title': f'Hapus Kelompok: {nama}',
        'kelompok': kelompok,
    }
    
    return render(request, 'fuzzy/kelompok_delete.html', context)


def kelompok_detail(request, pk):
    """
    Halaman Detail Kelompok
    
    Menampilkan detail lengkap kelompok beserta nilai fuzzifikasi.
    
    Args:
        pk (int): Primary key kelompok
    """
    kelompok = get_object_or_404(Kelompok, pk=pk)
    
    # Hitung fuzzifikasi lengkap
    fuzzifikasi = hitung_fuzzifikasi_lengkap(kelompok)
    
    context = {
        'title': f'Detail Kelompok: {kelompok.nama}',
        'kelompok': kelompok,
        'fuzzifikasi': fuzzifikasi,
        'variabel_list': VARIABEL_LIST,
        'kategori_variabel': KATEGORI_VARIABEL,
    }
    
    return render(request, 'fuzzy/kelompok_detail.html', context)


# =============================================================================
# SELEKSI FUZZY
# =============================================================================

def seleksi_and(request):
    """
    Halaman Seleksi Fuzzy AND
    
    Melakukan seleksi kelompok menggunakan operator AND (minimum).
    User memilih 2 kriteria (variabel + kategori).
    """
    hasil = None
    kriteria_teks = []
    form = SeleksiFuzzyForm()
    
    if request.method == 'POST':
        form = SeleksiFuzzyForm(request.POST)
        if form.is_valid():
            variabel_1 = form.cleaned_data['variabel_1']
            kategori_1 = form.cleaned_data['kategori_1']
            variabel_2 = form.cleaned_data['variabel_2']
            kategori_2 = form.cleaned_data['kategori_2']
            
            # Buat kriteria
            kriteria = [
                (variabel_1, kategori_1),
                (variabel_2, kategori_2),
            ]
            
            # Ambil semua kelompok
            kelompok_list = Kelompok.objects.all()
            
            # Lakukan seleksi fuzzy dengan operator AND
            hasil = seleksi_fuzzy(kelompok_list, kriteria, operator='AND')
            
            # Buat teks kriteria untuk ditampilkan
            for var, kat in kriteria:
                var_label = dict(VARIABEL_LIST).get(var, var)
                kat_label = dict(KATEGORI_VARIABEL.get(var, [])).get(kat, kat)
                kriteria_teks.append(f"{var_label} = {kat_label}")
        else:
            # Debug: Print form errors
            print(f"Form errors: {form.errors}")
    
    context = {
        'title': 'Seleksi Fuzzy AND',
        'form': form,
        'hasil': hasil,
        'kriteria_teks': kriteria_teks,
        'operator': 'AND',
        'kategori_variabel': KATEGORI_VARIABEL,
    }
    
    return render(request, 'fuzzy/seleksi_fuzzy.html', context)


def seleksi_or(request):
    """
    Halaman Seleksi Fuzzy OR
    
    Melakukan seleksi kelompok menggunakan operator OR (maximum).
    User memilih 2 kriteria (variabel + kategori).
    """
    hasil = None
    kriteria_teks = []
    form = SeleksiFuzzyForm()
    
    if request.method == 'POST':
        form = SeleksiFuzzyForm(request.POST)
        if form.is_valid():
            variabel_1 = form.cleaned_data['variabel_1']
            kategori_1 = form.cleaned_data['kategori_1']
            variabel_2 = form.cleaned_data['variabel_2']
            kategori_2 = form.cleaned_data['kategori_2']
            
            # Buat kriteria
            kriteria = [
                (variabel_1, kategori_1),
                (variabel_2, kategori_2),
            ]
            
            # Ambil semua kelompok
            kelompok_list = Kelompok.objects.all()
            
            # Lakukan seleksi fuzzy dengan operator OR
            hasil = seleksi_fuzzy(kelompok_list, kriteria, operator='OR')
            
            # Buat teks kriteria untuk ditampilkan
            for var, kat in kriteria:
                var_label = dict(VARIABEL_LIST).get(var, var)
                kat_label = dict(KATEGORI_VARIABEL.get(var, [])).get(kat, kat)
                kriteria_teks.append(f"{var_label} = {kat_label}")
        else:
            # Debug: Print form errors
            print(f"Form errors: {form.errors}")
    
    context = {
        'title': 'Seleksi Fuzzy OR',
        'form': form,
        'hasil': hasil,
        'kriteria_teks': kriteria_teks,
        'operator': 'OR',
        'kategori_variabel': KATEGORI_VARIABEL,
    }
    
    return render(request, 'fuzzy/seleksi_fuzzy.html', context)


def seleksi_multi(request):
    """
    Halaman Seleksi Fuzzy Multi-Kriteria
    
    Melakukan seleksi dengan lebih dari 2 kriteria.
    User dapat memilih banyak kriteria sekaligus.
    """
    hasil = None
    kriteria_teks = []
    selected_kriteria = []
    operator_used = 'AND'
    
    if request.method == 'POST':
        # Ambil kriteria dari POST
        kriteria_list = request.POST.getlist('kriteria')
        operator_used = request.POST.get('operator', 'AND')
        
        if kriteria_list:
            # Parse kriteria (format: variabel|kategori)
            kriteria = []
            for k in kriteria_list:
                if '|' in k:
                    var, kat = k.split('|')
                    kriteria.append((var, kat))
                    selected_kriteria.append(k)
            
            if kriteria:
                # Ambil semua kelompok
                kelompok_list = Kelompok.objects.all()
                
                # Lakukan seleksi fuzzy
                hasil = seleksi_fuzzy(kelompok_list, kriteria, operator=operator_used)
                
                # Buat teks kriteria
                for var, kat in kriteria:
                    var_label = dict(VARIABEL_LIST).get(var, var)
                    kat_label = dict(KATEGORI_VARIABEL.get(var, [])).get(kat, kat)
                    kriteria_teks.append(f"{var_label} = {kat_label}")
    
    context = {
        'title': 'Seleksi Fuzzy Multi-Kriteria',
        'variabel_list': VARIABEL_LIST,
        'kategori_variabel': KATEGORI_VARIABEL,
        'hasil': hasil,
        'kriteria_teks': kriteria_teks,
        'selected_kriteria': selected_kriteria,
        'operator': operator_used,
    }
    
    return render(request, 'fuzzy/seleksi_multi.html', context)


# =============================================================================
# API ENDPOINTS
# =============================================================================

def api_kategori(request, variabel):
    """
    API endpoint untuk mendapatkan kategori berdasarkan variabel
    
    Digunakan untuk update dropdown kategori secara dinamis via AJAX.
    
    Args:
        variabel (str): Nama variabel
    
    Returns:
        JsonResponse: List kategori untuk variabel tersebut
    """
    kategori = KATEGORI_VARIABEL.get(variabel, [])
    return JsonResponse({
        'variabel': variabel,
        'kategori': [{'value': k[0], 'label': k[1]} for k in kategori]
    })


def api_fuzzifikasi(request, pk):
    """
    API endpoint untuk mendapatkan nilai fuzzifikasi kelompok
    
    Args:
        pk (int): Primary key kelompok
    
    Returns:
        JsonResponse: Data fuzzifikasi lengkap
    """
    kelompok = get_object_or_404(Kelompok, pk=pk)
    fuzzifikasi = hitung_fuzzifikasi_lengkap(kelompok)
    
    return JsonResponse(fuzzifikasi)


def api_seleksi(request):
    """
    API endpoint untuk seleksi fuzzy
    
    Request (POST):
        kriteria: list of [variabel, kategori] pairs
        operator: 'AND' atau 'OR'
    
    Returns:
        JsonResponse: Hasil seleksi
    """
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        
        kriteria = [tuple(k) for k in data.get('kriteria', [])]
        operator = data.get('operator', 'AND')
        
        kelompok_list = Kelompok.objects.all()
        hasil = seleksi_fuzzy(kelompok_list, kriteria, operator=operator)
        
        return JsonResponse({
            'operator': operator,
            'kriteria': kriteria,
            'hasil': hasil,
            'total': len(hasil)
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
