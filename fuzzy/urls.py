"""
URL Configuration untuk aplikasi SPK Fuzzy Database Model Tahani

URL Patterns:
- /                     : Dashboard
- /kelompok/            : List data kelompok
- /kelompok/add/        : Tambah kelompok
- /kelompok/<id>/       : Detail kelompok
- /kelompok/<id>/edit/  : Edit kelompok
- /kelompok/<id>/delete/: Hapus kelompok
- /seleksi/and/         : Seleksi fuzzy AND
- /seleksi/or/          : Seleksi fuzzy OR
- /seleksi/multi/       : Seleksi fuzzy multi-kriteria
- /api/kategori/<var>/  : API kategori per variabel
- /api/fuzzifikasi/<id>/: API fuzzifikasi kelompok
- /api/seleksi/         : API seleksi fuzzy
"""

from django.urls import path
from . import views

app_name = 'fuzzy'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # CRUD Kelompok
    path('kelompok/', views.kelompok_list, name='kelompok_list'),
    path('kelompok/add/', views.kelompok_add, name='kelompok_add'),
    path('kelompok/<int:pk>/', views.kelompok_detail, name='kelompok_detail'),
    path('kelompok/<int:pk>/edit/', views.kelompok_edit, name='kelompok_edit'),
    path('kelompok/<int:pk>/delete/', views.kelompok_delete, name='kelompok_delete'),
    
    # Seleksi Fuzzy
    path('seleksi/and/', views.seleksi_and, name='seleksi_and'),
    path('seleksi/or/', views.seleksi_or, name='seleksi_or'),
    path('seleksi/multi/', views.seleksi_multi, name='seleksi_multi'),
    
    # API Endpoints
    path('api/kategori/<str:variabel>/', views.api_kategori, name='api_kategori'),
    path('api/fuzzifikasi/<int:pk>/', views.api_fuzzifikasi, name='api_fuzzifikasi'),
    path('api/seleksi/', views.api_seleksi, name='api_seleksi'),
    
    # Pengaturan Parameter Fuzzy
    path('parameter/', views.parameter_list, name='parameter_list'),
    path('parameter/<int:pk>/edit/', views.parameter_edit, name='parameter_edit'),
    path('parameter/reset/', views.parameter_reset, name='parameter_reset'),
    path('parameter/initialize/', views.parameter_initialize, name='parameter_initialize'),
]
