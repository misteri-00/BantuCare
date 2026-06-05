from utils.database import get_connection

# ═══════════════════════════════════════════════════════════════════════
# Recommendation helpers
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
    conn = get_connection()
    results = []
    for minat in minat_list:
        kategori = MINAT_TO_KATEGORI.get(minat)
        if kategori:
            rows = conn.execute(
                "SELECT * FROM campaigns WHERE kategori = ? AND status = 'Aktif' ORDER BY dana_terkumpul DESC LIMIT 2",
                (kategori,)
            ).fetchall()
            results.extend([dict(r) for r in rows])
    conn.close()
    # Hilangkan duplikat berdasarkan id
    seen = set()
    unique = []
    for r in results:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)
    return unique