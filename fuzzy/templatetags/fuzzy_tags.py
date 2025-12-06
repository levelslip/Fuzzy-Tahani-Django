"""
Custom Template Tags untuk SPK Fuzzy Tahani

Template tags ini digunakan untuk mengakses dictionary
di dalam template Django.
"""

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Template filter untuk mengakses item dictionary
    
    Penggunaan di template:
        {{ my_dict|get_item:key_variable }}
    
    Args:
        dictionary: Dictionary yang akan diakses
        key: Key yang dicari
    
    Returns:
        Value dari dictionary[key] atau None jika tidak ada
    """
    if dictionary is None:
        return None
    
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    
    # Jika dictionary adalah list of tuples, convert ke dict dulu
    if isinstance(dictionary, (list, tuple)):
        return dict(dictionary).get(key)
    
    return None


@register.filter
def multiply(value, arg):
    """
    Template filter untuk perkalian
    
    Penggunaan di template:
        {{ value|multiply:100 }}
    
    Args:
        value: Nilai yang akan dikalikan
        arg: Pengali
    
    Returns:
        Hasil perkalian
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def cut(value, arg):
    """
    Template filter untuk menghapus substring
    
    Penggunaan di template:
        {{ value|cut:"_" }}
    
    Args:
        value: String yang akan diproses
        arg: Substring yang akan dihapus
    
    Returns:
        String tanpa substring yang dihapus
    """
    if value is None:
        return ''
    return str(value).replace(arg, ' ')


@register.filter
def percentage(value):
    """
    Konversi nilai 0-1 ke persentase
    
    Penggunaan di template:
        {{ value|percentage }}
    
    Args:
        value: Nilai antara 0-1
    
    Returns:
        Nilai dalam persentase (0-100)
    """
    try:
        return float(value) * 100
    except (ValueError, TypeError):
        return 0
