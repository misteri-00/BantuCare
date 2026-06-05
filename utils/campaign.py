from utils.database import get_connection

# ═══════════════════════════════════════════════════════════════════════
# Campaign CRUD helpers
# ═══════════════════════════════════════════════════════════════════════

def get_all_campaigns():
    """Ambil semua kampanye yang aktif."""
    conn = get_connection()
    campaigns = conn.execute("""
        SELECT *
        FROM campaigns
        ORDER BY id DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in campaigns]


def get_campaign(campaign_id):
    """Ambil satu kampanye berdasarkan id (alias lama)."""
    return get_campaign_by_id(campaign_id)


def get_campaign_by_id(campaign_id):
    """Ambil satu kampanye berdasarkan id."""
    conn = get_connection()
    campaign = conn.execute("""
        SELECT *
        FROM campaigns
        WHERE id = ?
    """, (campaign_id,)).fetchone()
    conn.close()
    return dict(campaign) if campaign else None


def get_campaigns_by_category(kategori):
    """Ambil kampanye berdasarkan kategori."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM campaigns WHERE kategori = ? ORDER BY id DESC",
        (kategori,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_campaigns(keyword):
    """Cari kampanye berdasarkan kata kunci di judul atau deskripsi."""
    conn = get_connection()
    q = f"%{keyword}%"
    rows = conn.execute(
        "SELECT * FROM campaigns WHERE (judul LIKE ? OR deskripsi LIKE ?) ORDER BY id DESC",
        (q, q)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_total_donasi():
    """Hitung total dana terkumpul dari seluruh kampanye."""
    conn = get_connection()
    row = conn.execute("SELECT COALESCE(SUM(dana_terkumpul), 0) FROM campaigns").fetchone()
    conn.close()
    return row[0]


def get_campaign_count():
    """Hitung jumlah kampanye."""
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) FROM campaigns").fetchone()
    conn.close()
    return row[0]