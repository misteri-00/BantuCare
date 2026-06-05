from utils.database import get_connection

# ═══════════════════════════════════════════════════════════════════════
# Volunteer CRUD helpers
# ═══════════════════════════════════════════════════════════════════════

def register_volunteer(nama, email, no_hp, event):
    """Daftarkan volunteer baru ke database."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO volunteers (nama, email, no_hp, event) VALUES (?, ?, ?, ?)",
        (nama, email, no_hp, event)
    )
    conn.commit()
    conn.close()


def get_all_volunteers():
    """Ambil semua data volunteer."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM volunteers ORDER BY tanggal_daftar DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_volunteer_count():
    """Hitung jumlah volunteer terdaftar."""
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) FROM volunteers").fetchone()
    conn.close()
    return row[0]
