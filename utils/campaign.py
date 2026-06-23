# ═══════════════════════════════════════════════════════════════════════
# Campaign CRUD helpers (Static Data Version)
# ═══════════════════════════════════════════════════════════════════════

CAMPAIGNS_DATA = [
    {
        'id': 1, 
        'judul': 'Beasiswa Indonesia', 
        'kategori': 'Pendidikan', 
        'deskripsi': 'Membantu siswa kurang mampu mendapatkan pendidikan yang layak.', 
        'target_dana': 50000000, 
        'dana_terkumpul': 15000000, 
        'lokasi': 'Bandung', 
        'latitude': -6.9175, 
        'longitude': 107.6191, 
        'status': 'Aktif'
    },
    {
        'id': 2, 
        'judul': 'Peduli Banjir Jawa Barat', 
        'kategori': 'Bencana Alam', 
        'deskripsi': 'Bantuan darurat untuk korban banjir.', 
        'target_dana': 100000000, 
        'dana_terkumpul': 45000000, 
        'lokasi': 'Bekasi', 
        'latitude': -6.2383, 
        'longitude': 106.9756, 
        'status': 'Aktif'
    },
    {
        'id': 3, 
        'judul': '1000 Pohon Hijau', 
        'kategori': 'Lingkungan', 
        'deskripsi': 'Program penghijauan dan pelestarian lingkungan.', 
        'target_dana': 30000000, 
        'dana_terkumpul': 10110000, 
        'lokasi': 'Bogor', 
        'latitude': -6.595, 
        'longitude': 106.8166, 
        'status': 'Aktif'
    },
    {
        'id': 4, 
        'judul': 'Bantuan Panti Asuhan', 
        'kategori': 'Panti Asuhan', 
        'deskripsi': 'Membantu kebutuhan anak-anak panti asuhan.', 
        'target_dana': 25000000, 
        'dana_terkumpul': 8250000, 
        'lokasi': 'Depok', 
        'latitude': -6.4025, 
        'longitude': 106.7942, 
        'status': 'Aktif'
    },
]


def get_all_campaigns():
    """Ambil semua kampanye yang aktif."""
    return sorted(CAMPAIGNS_DATA, key=lambda x: x['id'], reverse=True)


def get_campaign(campaign_id):
    """Ambil satu kampanye berdasarkan id (alias lama)."""
    return get_campaign_by_id(campaign_id)


def get_campaign_by_id(campaign_id):
    """Ambil satu kampanye berdasarkan id."""
    for c in CAMPAIGNS_DATA:
        if c['id'] == campaign_id:
            return c
    return None


def get_campaigns_by_category(kategori):
    """Ambil kampanye berdasarkan kategori."""
    filtered = [c for c in CAMPAIGNS_DATA if c['kategori'] == kategori]
    return sorted(filtered, key=lambda x: x['id'], reverse=True)


def search_campaigns(keyword):
    """Cari kampanye berdasarkan kata kunci di judul atau deskripsi."""
    keyword_lower = keyword.lower()
    filtered = [c for c in CAMPAIGNS_DATA if keyword_lower in c['judul'].lower() or keyword_lower in c['deskripsi'].lower()]
    return sorted(filtered, key=lambda x: x['id'], reverse=True)


def get_total_donasi():
    """Hitung total dana terkumpul dari seluruh kampanye."""
    import streamlit as st
    
    # Hitung total donasi dari kampanye dasar
    base_total = sum(c['dana_terkumpul'] for c in CAMPAIGNS_DATA)
    
    # Tambahkan donasi baru dari session jika ada
    session_donations = st.session_state.get('donations', [])
    session_total = sum(d['nominal'] for d in session_donations)
    
    return base_total + session_total


def get_campaign_count():
    """Hitung jumlah kampanye."""
    return len(CAMPAIGNS_DATA)