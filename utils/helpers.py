import os
import base64
from pathlib import Path
from utils.database import get_connection

# ═══════════════════════════════════════════════════════════════════════
# General helpers
# ═══════════════════════════════════════════════════════════════════════

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

# Mapping kategori ke gambar banner
KATEGORI_IMAGE = {
    "Pendidikan": os.path.join(ASSETS, "banner_education.png"),
    "Kesehatan": os.path.join(ASSETS, "banner_health.png"),
    "Bencana Alam": os.path.join(ASSETS, "banner_food.png"),
    "Lingkungan": os.path.join(ASSETS, "banner_education.png"),
    "Panti Asuhan": os.path.join(ASSETS, "banner_food.png"),
}


def format_rupiah(amount):
    """Format angka ke format Rupiah Indonesia."""
    return f"Rp {amount:,.0f}".replace(",", ".")


def calculate_progress(terkumpul, target):
    """Hitung persentase progress donasi (alias lama)."""
    if target == 0:
        return 0
    return round((terkumpul / target) * 100, 2)


def calc_progress(terkumpul, target):
    """Hitung persentase progress donasi."""
    if target <= 0:
        return 0
    return min(int((terkumpul / target) * 100), 100)


def img_to_base64(path: str) -> str:
    """Return a base64 data-URI string for the given image file."""
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = Path(path).suffix.lstrip(".")
        if ext == "jpg":
            ext = "jpeg"
        return f"data:image/{ext};base64,{data}"
    except Exception:
        return ""


def get_image_for_category(kategori):
    """Dapatkan path gambar banner berdasarkan kategori kampanye."""
    return KATEGORI_IMAGE.get(kategori, os.path.join(ASSETS, "banner_food.png"))


# ── Donation CRUD ──────────────────────────────────────────────────────

def save_donation(user_id, campaign_id, nominal, metode, anonim, bukti, pesan=""):
    """Simpan transaksi donasi ke database dan update dana kampanye."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO donations (user_id, campaign_id, nominal, metode_pembayaran, anonim, bukti_transfer, pesan)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, campaign_id, nominal, metode, 1 if anonim else 0, bukti, pesan)
    )
    conn.execute(
        "UPDATE campaigns SET dana_terkumpul = dana_terkumpul + ? WHERE id = ?",
        (nominal, campaign_id)
    )
    conn.commit()
    conn.close()


def get_all_donations():
    """Ambil semua riwayat donasi beserta nama kampanye."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT d.*, c.judul as program_judul
        FROM donations d
        LEFT JOIN campaigns c ON d.campaign_id = c.id
        ORDER BY d.tanggal_donasi DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_donation_count():
    """Hitung jumlah donasi."""
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) FROM donations").fetchone()
    conn.close()
    return row[0]


def get_total_donated():
    """Total nominal seluruh donasi."""
    conn = get_connection()
    row = conn.execute("SELECT COALESCE(SUM(nominal), 0) FROM donations").fetchone()
    conn.close()
    return row[0]


def get_monthly_donations():
    """Ambil total donasi bulanan untuk grafik."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT strftime('%Y-%m', tanggal_donasi) as bulan, SUM(nominal) as total
        FROM donations
        GROUP BY bulan
        ORDER BY bulan ASC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]