# SPK Fuzzy Database Model Tahani

Sistem Pendukung Keputusan (SPK) berbasis **Fuzzy Database Model Tahani** untuk pemilihan penerima bantuan sosial.

## 📋 Deskripsi

Aplikasi web ini mampu melakukan:
- ✅ CRUD data kelompok (nama, tanggal berdiri, jumlah anggota, luas lahan, frekuensi bantuan, kualitas SDM, unit usaha, kas)
- ✅ Hitung fuzzifikasi untuk setiap variabel sesuai fungsi keanggotaan
- ✅ Proses seleksi fuzzy dengan operator AND (min) dan OR (max)
- ✅ Tampilkan daftar kelompok yang memenuhi kriteria dengan nilai fire strength

## 🛠️ Tech Stack

- **Backend:** Python 3.11+, Django 5.x
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Database:** SQLite (dev), PostgreSQL (production)

## 📦 Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd fuzzy-tahani
```

### 2. Buat Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Migrasi Database
```bash
python manage.py migrate
```

### 5. Generate Dummy Data (Opsional)
```bash
python manage.py generate_dummy_data
```

### 6. Jalankan Server
```bash
python manage.py runserver
```

Akses aplikasi di: http://127.0.0.1:8000

## 📂 Struktur Proyek

```
fuzzy-tahani/
├── fuzzy/                      # Django app utama
│   ├── management/
│   │   └── commands/
│   │       └── generate_dummy_data.py
│   ├── templates/fuzzy/        # HTML templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── kelompok_list.html
│   │   ├── kelompok_form.html
│   │   ├── kelompok_detail.html
│   │   ├── kelompok_delete.html
│   │   ├── seleksi_fuzzy.html
│   │   └── seleksi_multi.html
│   ├── templatetags/
│   │   └── fuzzy_tags.py
│   ├── admin.py
│   ├── forms.py
│   ├── models.py              # Model Kelompok
│   ├── urls.py
│   ├── utils.py               # Fungsi membership & fire strength
│   └── views.py
├── config/                    # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── Procfile                   # For Railway/Render
├── runtime.txt
└── README.md
```

## 🔢 Fungsi Keanggotaan (Membership Functions)

### Usia Kelompok
- **Baru:** 0-2 tahun (bahu kiri)
- **Sedang:** 1-5 tahun (segitiga, puncak 3)
- **Lama:** >4 tahun (bahu kanan)

### Frekuensi Bantuan
- **Jarang:** 0-2 kali (bahu kiri)
- **Sedang:** 1-5 kali (segitiga, puncak 3)
- **Sering:** >4 kali (bahu kanan)

### Luas Lahan
- **Sempit:** 0-1 Ha (bahu kiri)
- **Sedang:** 0.5-2.5 Ha (segitiga)
- **Luas:** >2 Ha (bahu kanan)

### Jumlah Anggota
- **Sedikit:** 0-10 orang (bahu kiri)
- **Cukup:** 5-25 orang (segitiga)
- **Banyak:** >20 orang (bahu kanan)

### SDM / Unit Usaha / Kas (Skala 1-10)
- **Buruk:** 0-2
- **Kurang:** 1-4
- **Cukup:** 3-6
- **Baik:** 5-8
- **Sangat Baik:** 7-10

## 🧮 Operator Fuzzy

### AND (Minimum)
```
Fire Strength = MIN(μ₁, μ₂, ..., μₙ)
```
Cocok ketika **semua kriteria harus dipenuhi**.

### OR (Maximum)
```
Fire Strength = MAX(μ₁, μ₂, ..., μₙ)
```
Cocok ketika **salah satu kriteria sudah cukup**.

## 🌐 Deployment

### Railway
1. Push code ke GitHub
2. Connect repository di Railway
3. Set environment variables:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.railway.app
   DATABASE_URL=postgres://...
   ```

### Render
1. Push code ke GitHub
2. Create new Web Service di Render
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn config.wsgi:application`

## 📸 Screenshots

### Dashboard
Menampilkan statistik dan kelompok terbaru.

### Data Kelompok
CRUD lengkap untuk mengelola data kelompok.

### Seleksi Fuzzy
Pilih kriteria dan operator untuk melakukan seleksi.

## 📚 Referensi

Paper: "Sistem Pendukung Keputusan Pemilihan Penerima Bantuan Sosial Menggunakan Metode Fuzzy Database Model Tahani"

## 📝 License

MIT License

## 👨‍💻 Author

Developed for Fuzzy Logic Course - Semester 5
