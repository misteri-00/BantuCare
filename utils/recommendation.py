from utils.campaign import get_all_campaigns

# ═══════════════════════════════════════════════════════════════════════
# Recommendation helpers (Static Data Version)
# ═══════════════════════════════════════════════════════════════════════

# Mapping minat user ke kategori kampanye
MINAT_TO_KATEGORI = {
    "Pendidikan Anak": "Pendidikan",
    "Kesehatan & Medis": "Kesehatan",
    "Pelestarian Lingkungan": "Lingkungan",
    "Pemberdayaan Ekonomi": "Panti Asuhan",
    "Bantuan Bencana Alam": "Bencana Alam",
}


def get_recommendations(minat_list):
    """Berikan rekomendasi kampanye berdasarkan daftar minat user."""
    all_campaigns = get_all_campaigns()
    results = []
    
    for minat in minat_list:
        kategori = MINAT_TO_KATEGORI.get(minat)
        if kategori:
            # Filter by category and take top 2 by dana_terkumpul
            filtered = [c for c in all_campaigns if c['kategori'] == kategori and c['status'] == 'Aktif']
            sorted_filtered = sorted(filtered, key=lambda x: x['dana_terkumpul'], reverse=True)[:2]
            results.extend(sorted_filtered)
            
    # Hilangkan duplikat berdasarkan id
    seen = set()
    unique = []
    for r in results:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)
            
    return unique