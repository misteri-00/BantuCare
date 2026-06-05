from utils.database import get_connection

# ═══════════════════════════════════════════════════════════════════════
# Impact Tracker helpers
# ═══════════════════════════════════════════════════════════════════════

def get_total_impact():
    """Ambil total dampak dari seluruh kampanye."""
    conn = get_connection()
    row = conn.execute("""
        SELECT
            COALESCE(SUM(penerima_manfaat), 0) as penerima,
            COALESCE(SUM(laptop_diberikan), 0) as laptop,
            COALESCE(SUM(pohon_ditanam), 0) as pohon,
            COALESCE(SUM(sekolah_dibantu), 0) as sekolah,
            COALESCE(SUM(siswa_terbantu), 0) as siswa
        FROM impacts
    """).fetchone()
    conn.close()
    return dict(row) if row else {}


def get_impact_by_campaign(campaign_id):
    """Ambil dampak untuk satu kampanye."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM impacts WHERE campaign_id = ?", (campaign_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
