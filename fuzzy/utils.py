"""
Fuzzy Database Model Tahani - Utility Functions

File ini berisi implementasi semua fungsi keanggotaan (membership function)
dan fungsi fire strength untuk SPK Fuzzy Database Model Tahani.

Referensi: Paper "Sistem Pendukung Keputusan Pemilihan Penerima 
Bantuan Sosial Menggunakan Metode Fuzzy Database Model Tahani"

Fungsi keanggotaan yang diimplementasikan:
1. Usia: baru, sedang, lama
2. Frekuensi Bantuan: jarang, sedang, sering
3. Luas Lahan: sempit, sedang, luas
4. Jumlah Anggota: sedikit, cukup, banyak
5. SDM/Unit Usaha/Kas: buruk, kurang, cukup, baik, sangat_baik
"""


# =============================================================================
# KONSTANTA - Parameter Membership Function
# =============================================================================

# Parameter untuk fungsi keanggotaan USIA (dalam tahun)
USIA_PARAMS = {
    'baru': {'a': 0, 'b': 2},      # 0-2 tahun = baru
    'sedang': {'a': 1, 'b': 3, 'c': 5},  # 1-5 tahun = sedang (segitiga)
    'lama': {'a': 4, 'b': 6}       # >4 tahun = lama
}

# Parameter untuk fungsi keanggotaan FREKUENSI BANTUAN
FREKUENSI_PARAMS = {
    'jarang': {'a': 0, 'b': 2},    # 0-2 kali = jarang
    'sedang': {'a': 1, 'b': 3, 'c': 5},  # 1-5 kali = sedang
    'sering': {'a': 4, 'b': 6}     # >4 kali = sering
}

# Parameter untuk fungsi keanggotaan LUAS LAHAN (dalam hektar)
LUAS_LAHAN_PARAMS = {
    'sempit': {'a': 0, 'b': 1},     # 0-1 ha = sempit
    'sedang': {'a': 0.5, 'b': 1.5, 'c': 2.5},  # 0.5-2.5 ha = sedang
    'luas': {'a': 2, 'b': 3}        # >2 ha = luas
}

# Parameter untuk fungsi keanggotaan JUMLAH ANGGOTA
JUMLAH_ANGGOTA_PARAMS = {
    'sedikit': {'a': 0, 'b': 10},   # 0-10 orang = sedikit
    'cukup': {'a': 5, 'b': 15, 'c': 25},  # 5-25 orang = cukup
    'banyak': {'a': 20, 'b': 30}    # >20 orang = banyak
}

# Parameter untuk fungsi keanggotaan SDM, UNIT USAHA, KAS (skala 1-10)
SKOR_PARAMS = {
    'buruk': {'a': 0, 'b': 2},
    'kurang': {'a': 1, 'b': 3, 'c': 4},
    'cukup': {'a': 3, 'b': 5, 'c': 6},
    'baik': {'a': 5, 'b': 7, 'c': 8},
    'sangat_baik': {'a': 7, 'b': 10}
}


# =============================================================================
# FUNGSI KEANGGOTAAN DASAR
# =============================================================================

def fungsi_bahu_kiri(x, a, b):
    """
    Fungsi Keanggotaan Bahu Kiri (Left Shoulder)
    
    Representasi linear menurun dari kiri ke kanan.
    Nilai tinggi di kiri, menurun ke kanan.
    
    Formula:
        μ(x) = 1,           jika x <= a
        μ(x) = (b-x)/(b-a), jika a < x < b
        μ(x) = 0,           jika x >= b
    
    Args:
        x (float): Nilai input
        a (float): Batas bawah (nilai penuh = 1)
        b (float): Batas atas (nilai = 0)
    
    Returns:
        float: Nilai keanggotaan (0-1)
    
    Example:
        >>> fungsi_bahu_kiri(0, 0, 2)  # x <= a
        1.0
        >>> fungsi_bahu_kiri(1, 0, 2)  # a < x < b
        0.5
        >>> fungsi_bahu_kiri(3, 0, 2)  # x >= b
        0.0
    """
    if x <= a:
        return 1.0
    elif x >= b:
        return 0.0
    else:
        return (b - x) / (b - a)


def fungsi_bahu_kanan(x, a, b):
    """
    Fungsi Keanggotaan Bahu Kanan (Right Shoulder)
    
    Representasi linear meningkat dari kiri ke kanan.
    Nilai rendah di kiri, meningkat ke kanan.
    
    Formula:
        μ(x) = 0,           jika x <= a
        μ(x) = (x-a)/(b-a), jika a < x < b
        μ(x) = 1,           jika x >= b
    
    Args:
        x (float): Nilai input
        a (float): Batas bawah (nilai = 0)
        b (float): Batas atas (nilai penuh = 1)
    
    Returns:
        float: Nilai keanggotaan (0-1)
    
    Example:
        >>> fungsi_bahu_kanan(0, 2, 4)  # x <= a
        0.0
        >>> fungsi_bahu_kanan(3, 2, 4)  # a < x < b
        0.5
        >>> fungsi_bahu_kanan(5, 2, 4)  # x >= b
        1.0
    """
    if x <= a:
        return 0.0
    elif x >= b:
        return 1.0
    else:
        return (x - a) / (b - a)


def fungsi_segitiga(x, a, b, c):
    """
    Fungsi Keanggotaan Segitiga (Triangle)
    
    Representasi segitiga dengan puncak di tengah.
    
    Formula:
        μ(x) = 0,           jika x <= a atau x >= c
        μ(x) = (x-a)/(b-a), jika a < x <= b
        μ(x) = (c-x)/(c-b), jika b < x < c
    
    Args:
        x (float): Nilai input
        a (float): Batas kiri (nilai = 0)
        b (float): Puncak segitiga (nilai = 1)
        c (float): Batas kanan (nilai = 0)
    
    Returns:
        float: Nilai keanggotaan (0-1)
    
    Example:
        >>> fungsi_segitiga(0, 1, 3, 5)   # x <= a
        0.0
        >>> fungsi_segitiga(2, 1, 3, 5)   # a < x <= b
        0.5
        >>> fungsi_segitiga(3, 1, 3, 5)   # x = b (puncak)
        1.0
        >>> fungsi_segitiga(4, 1, 3, 5)   # b < x < c
        0.5
        >>> fungsi_segitiga(6, 1, 3, 5)   # x >= c
        0.0
    """
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:  # b < x < c
        return (c - x) / (c - b)


# =============================================================================
# FUNGSI KEANGGOTAAN USIA
# =============================================================================

def mu_usia_baru(usia):
    """
    Fungsi Keanggotaan Usia BARU
    
    Kelompok dengan usia baru (0-2 tahun).
    Menggunakan fungsi bahu kiri.
    
    Args:
        usia (int/float): Usia kelompok dalam tahun
    
    Returns:
        float: Nilai keanggotaan (0-1)
    
    Kurva:
        μ(usia) = 1,                    jika usia <= 0
        μ(usia) = (2-usia)/(2-0),       jika 0 < usia < 2
        μ(usia) = 0,                    jika usia >= 2
    """
    params = USIA_PARAMS['baru']
    return fungsi_bahu_kiri(usia, params['a'], params['b'])


def mu_usia_sedang(usia):
    """
    Fungsi Keanggotaan Usia SEDANG
    
    Kelompok dengan usia sedang (1-5 tahun).
    Menggunakan fungsi segitiga dengan puncak di 3 tahun.
    
    Args:
        usia (int/float): Usia kelompok dalam tahun
    
    Returns:
        float: Nilai keanggotaan (0-1)
    
    Kurva:
        μ(usia) = 0,                    jika usia <= 1 atau usia >= 5
        μ(usia) = (usia-1)/(3-1),       jika 1 < usia <= 3
        μ(usia) = (5-usia)/(5-3),       jika 3 < usia < 5
    """
    params = USIA_PARAMS['sedang']
    return fungsi_segitiga(usia, params['a'], params['b'], params['c'])


def mu_usia_lama(usia):
    """
    Fungsi Keanggotaan Usia LAMA
    
    Kelompok dengan usia lama (>4 tahun).
    Menggunakan fungsi bahu kanan.
    
    Args:
        usia (int/float): Usia kelompok dalam tahun
    
    Returns:
        float: Nilai keanggotaan (0-1)
    
    Kurva:
        μ(usia) = 0,                    jika usia <= 4
        μ(usia) = (usia-4)/(6-4),       jika 4 < usia < 6
        μ(usia) = 1,                    jika usia >= 6
    """
    params = USIA_PARAMS['lama']
    return fungsi_bahu_kanan(usia, params['a'], params['b'])


# =============================================================================
# FUNGSI KEANGGOTAAN FREKUENSI BANTUAN
# =============================================================================

def mu_frekuensi_jarang(frekuensi):
    """
    Fungsi Keanggotaan Frekuensi JARANG
    
    Kelompok jarang menerima bantuan (0-2 kali).
    Menggunakan fungsi bahu kiri.
    
    Args:
        frekuensi (int): Jumlah bantuan yang diterima
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = FREKUENSI_PARAMS['jarang']
    return fungsi_bahu_kiri(frekuensi, params['a'], params['b'])


def mu_frekuensi_sedang(frekuensi):
    """
    Fungsi Keanggotaan Frekuensi SEDANG
    
    Kelompok cukup sering menerima bantuan (1-5 kali).
    Menggunakan fungsi segitiga.
    
    Args:
        frekuensi (int): Jumlah bantuan yang diterima
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = FREKUENSI_PARAMS['sedang']
    return fungsi_segitiga(frekuensi, params['a'], params['b'], params['c'])


def mu_frekuensi_sering(frekuensi):
    """
    Fungsi Keanggotaan Frekuensi SERING
    
    Kelompok sering menerima bantuan (>4 kali).
    Menggunakan fungsi bahu kanan.
    
    Args:
        frekuensi (int): Jumlah bantuan yang diterima
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = FREKUENSI_PARAMS['sering']
    return fungsi_bahu_kanan(frekuensi, params['a'], params['b'])


# =============================================================================
# FUNGSI KEANGGOTAAN LUAS LAHAN
# =============================================================================

def mu_lahan_sempit(luas):
    """
    Fungsi Keanggotaan Lahan SEMPIT
    
    Kelompok dengan lahan sempit (0-1 ha).
    Menggunakan fungsi bahu kiri.
    
    Args:
        luas (float): Luas lahan dalam hektar
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = LUAS_LAHAN_PARAMS['sempit']
    return fungsi_bahu_kiri(luas, params['a'], params['b'])


def mu_lahan_sedang(luas):
    """
    Fungsi Keanggotaan Lahan SEDANG
    
    Kelompok dengan lahan sedang (0.5-2.5 ha).
    Menggunakan fungsi segitiga.
    
    Args:
        luas (float): Luas lahan dalam hektar
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = LUAS_LAHAN_PARAMS['sedang']
    return fungsi_segitiga(luas, params['a'], params['b'], params['c'])


def mu_lahan_luas(luas):
    """
    Fungsi Keanggotaan Lahan LUAS
    
    Kelompok dengan lahan luas (>2 ha).
    Menggunakan fungsi bahu kanan.
    
    Args:
        luas (float): Luas lahan dalam hektar
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = LUAS_LAHAN_PARAMS['luas']
    return fungsi_bahu_kanan(luas, params['a'], params['b'])


# =============================================================================
# FUNGSI KEANGGOTAAN JUMLAH ANGGOTA
# =============================================================================

def mu_anggota_sedikit(jumlah):
    """
    Fungsi Keanggotaan Anggota SEDIKIT
    
    Kelompok dengan anggota sedikit (0-10 orang).
    Menggunakan fungsi bahu kiri.
    
    Args:
        jumlah (int): Jumlah anggota
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = JUMLAH_ANGGOTA_PARAMS['sedikit']
    return fungsi_bahu_kiri(jumlah, params['a'], params['b'])


def mu_anggota_cukup(jumlah):
    """
    Fungsi Keanggotaan Anggota CUKUP
    
    Kelompok dengan anggota cukup (5-25 orang).
    Menggunakan fungsi segitiga.
    
    Args:
        jumlah (int): Jumlah anggota
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = JUMLAH_ANGGOTA_PARAMS['cukup']
    return fungsi_segitiga(jumlah, params['a'], params['b'], params['c'])


def mu_anggota_banyak(jumlah):
    """
    Fungsi Keanggotaan Anggota BANYAK
    
    Kelompok dengan anggota banyak (>20 orang).
    Menggunakan fungsi bahu kanan.
    
    Args:
        jumlah (int): Jumlah anggota
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = JUMLAH_ANGGOTA_PARAMS['banyak']
    return fungsi_bahu_kanan(jumlah, params['a'], params['b'])


# =============================================================================
# FUNGSI KEANGGOTAAN SDM, UNIT USAHA, KAS (menggunakan skala yang sama)
# =============================================================================

def mu_skor_buruk(skor):
    """
    Fungsi Keanggotaan Skor BURUK
    
    Untuk SDM/Unit Usaha/Kas dengan nilai buruk (0-2).
    Menggunakan fungsi bahu kiri.
    
    Args:
        skor (int): Nilai skor (1-10)
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = SKOR_PARAMS['buruk']
    return fungsi_bahu_kiri(skor, params['a'], params['b'])


def mu_skor_kurang(skor):
    """
    Fungsi Keanggotaan Skor KURANG
    
    Untuk SDM/Unit Usaha/Kas dengan nilai kurang (1-4).
    Menggunakan fungsi segitiga.
    
    Args:
        skor (int): Nilai skor (1-10)
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = SKOR_PARAMS['kurang']
    return fungsi_segitiga(skor, params['a'], params['b'], params['c'])


def mu_skor_cukup(skor):
    """
    Fungsi Keanggotaan Skor CUKUP
    
    Untuk SDM/Unit Usaha/Kas dengan nilai cukup (3-6).
    Menggunakan fungsi segitiga.
    
    Args:
        skor (int): Nilai skor (1-10)
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = SKOR_PARAMS['cukup']
    return fungsi_segitiga(skor, params['a'], params['b'], params['c'])


def mu_skor_baik(skor):
    """
    Fungsi Keanggotaan Skor BAIK
    
    Untuk SDM/Unit Usaha/Kas dengan nilai baik (5-8).
    Menggunakan fungsi segitiga.
    
    Args:
        skor (int): Nilai skor (1-10)
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = SKOR_PARAMS['baik']
    return fungsi_segitiga(skor, params['a'], params['b'], params['c'])


def mu_skor_sangat_baik(skor):
    """
    Fungsi Keanggotaan Skor SANGAT BAIK
    
    Untuk SDM/Unit Usaha/Kas dengan nilai sangat baik (7-10).
    Menggunakan fungsi bahu kanan.
    
    Args:
        skor (int): Nilai skor (1-10)
    
    Returns:
        float: Nilai keanggotaan (0-1)
    """
    params = SKOR_PARAMS['sangat_baik']
    return fungsi_bahu_kanan(skor, params['a'], params['b'])


# =============================================================================
# MAPPING FUNGSI KEANGGOTAAN
# =============================================================================

# Dictionary untuk mapping variabel ke fungsi keanggotaan
MEMBERSHIP_FUNCTIONS = {
    'usia': {
        'baru': mu_usia_baru,
        'sedang': mu_usia_sedang,
        'lama': mu_usia_lama,
    },
    'frekuensi_bantuan': {
        'jarang': mu_frekuensi_jarang,
        'sedang': mu_frekuensi_sedang,
        'sering': mu_frekuensi_sering,
    },
    'luas_lahan': {
        'sempit': mu_lahan_sempit,
        'sedang': mu_lahan_sedang,
        'luas': mu_lahan_luas,
    },
    'jumlah_anggota': {
        'sedikit': mu_anggota_sedikit,
        'cukup': mu_anggota_cukup,
        'banyak': mu_anggota_banyak,
    },
    'sdm': {
        'buruk': mu_skor_buruk,
        'kurang': mu_skor_kurang,
        'cukup': mu_skor_cukup,
        'baik': mu_skor_baik,
        'sangat_baik': mu_skor_sangat_baik,
    },
    'unit_usaha': {
        'buruk': mu_skor_buruk,
        'kurang': mu_skor_kurang,
        'cukup': mu_skor_cukup,
        'baik': mu_skor_baik,
        'sangat_baik': mu_skor_sangat_baik,
    },
    'kas': {
        'buruk': mu_skor_buruk,
        'kurang': mu_skor_kurang,
        'cukup': mu_skor_cukup,
        'baik': mu_skor_baik,
        'sangat_baik': mu_skor_sangat_baik,
    },
}

# Daftar variabel yang tersedia
VARIABEL_LIST = [
    ('usia', 'Usia Kelompok'),
    ('frekuensi_bantuan', 'Frekuensi Bantuan'),
    ('luas_lahan', 'Luas Lahan'),
    ('jumlah_anggota', 'Jumlah Anggota'),
    ('sdm', 'Kualitas SDM'),
    ('unit_usaha', 'Unit Usaha'),
    ('kas', 'Kas'),
]

# Kategori untuk setiap variabel
KATEGORI_VARIABEL = {
    'usia': [
        ('baru', 'Baru'),
        ('sedang', 'Sedang'),
        ('lama', 'Lama'),
    ],
    'frekuensi_bantuan': [
        ('jarang', 'Jarang'),
        ('sedang', 'Sedang'),
        ('sering', 'Sering'),
    ],
    'luas_lahan': [
        ('sempit', 'Sempit'),
        ('sedang', 'Sedang'),
        ('luas', 'Luas'),
    ],
    'jumlah_anggota': [
        ('sedikit', 'Sedikit'),
        ('cukup', 'Cukup'),
        ('banyak', 'Banyak'),
    ],
    'sdm': [
        ('buruk', 'Buruk'),
        ('kurang', 'Kurang'),
        ('cukup', 'Cukup'),
        ('baik', 'Baik'),
        ('sangat_baik', 'Sangat Baik'),
    ],
    'unit_usaha': [
        ('buruk', 'Buruk'),
        ('kurang', 'Kurang'),
        ('cukup', 'Cukup'),
        ('baik', 'Baik'),
        ('sangat_baik', 'Sangat Baik'),
    ],
    'kas': [
        ('buruk', 'Buruk'),
        ('kurang', 'Kurang'),
        ('cukup', 'Cukup'),
        ('baik', 'Baik'),
        ('sangat_baik', 'Sangat Baik'),
    ],
}


# =============================================================================
# FUNGSI HELPER
# =============================================================================

def get_membership_value(variabel, kategori, nilai):
    """
    Mendapatkan nilai keanggotaan berdasarkan variabel dan kategori
    
    Args:
        variabel (str): Nama variabel (usia, luas_lahan, dll)
        kategori (str): Kategori fuzzy (baru, sedang, lama, dll)
        nilai (float): Nilai crisp yang akan difuzzifikasi
    
    Returns:
        float: Nilai keanggotaan (0-1)
    
    Example:
        >>> get_membership_value('usia', 'baru', 1)
        0.5
    """
    if variabel not in MEMBERSHIP_FUNCTIONS:
        raise ValueError(f"Variabel '{variabel}' tidak valid")
    
    if kategori not in MEMBERSHIP_FUNCTIONS[variabel]:
        raise ValueError(f"Kategori '{kategori}' tidak valid untuk variabel '{variabel}'")
    
    func = MEMBERSHIP_FUNCTIONS[variabel][kategori]
    return func(nilai)


def get_all_membership_values(kelompok_data):
    """
    Menghitung semua nilai keanggotaan untuk semua variabel dan kategori
    
    Args:
        kelompok_data (dict): Data kelompok dalam bentuk dictionary
    
    Returns:
        dict: Dictionary berisi semua nilai keanggotaan
    
    Example:
        >>> data = {'usia': 3, 'luas_lahan': 1.5, ...}
        >>> get_all_membership_values(data)
        {
            'usia': {'baru': 0.0, 'sedang': 1.0, 'lama': 0.0},
            'luas_lahan': {'sempit': 0.0, 'sedang': 1.0, 'luas': 0.0},
            ...
        }
    """
    hasil = {}
    
    for variabel, _ in VARIABEL_LIST:
        nilai_crisp = kelompok_data.get(variabel, 0)
        hasil[variabel] = {}
        
        for kategori, _ in KATEGORI_VARIABEL[variabel]:
            hasil[variabel][kategori] = get_membership_value(
                variabel, kategori, nilai_crisp
            )
    
    return hasil


# =============================================================================
# FUNGSI FIRE STRENGTH (OPERATOR FUZZY)
# =============================================================================

def fire_strength_and(*membership_values):
    """
    Menghitung Fire Strength dengan operator AND (minimum)
    
    Operator AND dalam logika fuzzy menggunakan fungsi MIN.
    Hasilnya adalah nilai keanggotaan minimum dari semua input.
    
    Formula:
        μA ∧ μB = min(μA, μB)
    
    Args:
        *membership_values: Nilai-nilai keanggotaan yang akan di-AND-kan
    
    Returns:
        float: Nilai fire strength (0-1)
    
    Example:
        >>> fire_strength_and(0.8, 0.6, 0.9)
        0.6
        >>> fire_strength_and(0.5, 0.7)
        0.5
    """
    if not membership_values:
        return 0.0
    return min(membership_values)


def fire_strength_or(*membership_values):
    """
    Menghitung Fire Strength dengan operator OR (maximum)
    
    Operator OR dalam logika fuzzy menggunakan fungsi MAX.
    Hasilnya adalah nilai keanggotaan maximum dari semua input.
    
    Formula:
        μA ∨ μB = max(μA, μB)
    
    Args:
        *membership_values: Nilai-nilai keanggotaan yang akan di-OR-kan
    
    Returns:
        float: Nilai fire strength (0-1)
    
    Example:
        >>> fire_strength_or(0.3, 0.6, 0.4)
        0.6
        >>> fire_strength_or(0.2, 0.8)
        0.8
    """
    if not membership_values:
        return 0.0
    return max(membership_values)


# =============================================================================
# FUNGSI SELEKSI FUZZY
# =============================================================================

def seleksi_fuzzy(kelompok_list, kriteria, operator='AND'):
    """
    Melakukan seleksi fuzzy terhadap daftar kelompok
    
    Fungsi ini menghitung fire strength untuk setiap kelompok
    berdasarkan kriteria yang diberikan dan operator yang dipilih.
    
    Args:
        kelompok_list (list): List of Kelompok objects atau dict
        kriteria (list): List of tuples [(variabel, kategori), ...]
        operator (str): 'AND' atau 'OR'
    
    Returns:
        list: List of dict berisi hasil seleksi dengan fire strength > 0,
              diurutkan dari terbesar ke terkecil
    
    Example:
        >>> kriteria = [('usia', 'baru'), ('luas_lahan', 'luas')]
        >>> hasil = seleksi_fuzzy(kelompok_list, kriteria, 'AND')
    """
    hasil = []
    
    for kelompok in kelompok_list:
        # Ambil data kelompok
        if hasattr(kelompok, 'get_data_dict'):
            data = kelompok.get_data_dict()
            kelompok_obj = kelompok  # Simpan object asli
        else:
            data = kelompok
            kelompok_obj = kelompok  # Jika sudah dict, gunakan apa adanya
        
        # Hitung membership value untuk setiap kriteria
        membership_values = []
        detail_membership = {}
        
        for variabel, kategori in kriteria:
            nilai_crisp = data.get(variabel, 0)
            mu = get_membership_value(variabel, kategori, nilai_crisp)
            membership_values.append(mu)
            detail_membership[f"{variabel}_{kategori}"] = {
                'nilai_crisp': nilai_crisp,
                'membership': round(mu, 4)
            }
        
        # Hitung fire strength berdasarkan operator
        if operator.upper() == 'AND':
            fire_strength = fire_strength_and(*membership_values)
        else:
            fire_strength = fire_strength_or(*membership_values)
        
        # Hanya tambahkan jika fire strength > 0
        if fire_strength > 0:
            hasil.append({
                'kelompok': kelompok_obj,  # Gunakan object asli
                'membership_values': detail_membership,
                'fire_strength': round(fire_strength, 4)
            })
    
    # Urutkan dari fire strength terbesar ke terkecil
    hasil.sort(key=lambda x: x['fire_strength'], reverse=True)
    
    return hasil


def hitung_fuzzifikasi_lengkap(kelompok):
    """
    Menghitung fuzzifikasi lengkap untuk satu kelompok
    
    Mengembalikan semua nilai membership untuk semua variabel
    dan semua kategori.
    
    Args:
        kelompok: Object Kelompok atau dict
    
    Returns:
        dict: Data lengkap dengan semua nilai membership
    """
    if hasattr(kelompok, 'get_data_dict'):
        data = kelompok.get_data_dict()
    else:
        data = kelompok
    
    # Hitung semua membership values
    all_memberships = get_all_membership_values(data)
    
    return {
        'data': data,
        'memberships': all_memberships
    }
