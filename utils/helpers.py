import os
import base64
from pathlib import Path
import streamlit as st
import datetime
from utils.campaign import get_campaign_by_id

# ═══════════════════════════════════════════════════════════════════════
# General helpers (Static Data Version)
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
    """Simpan transaksi donasi ke session state."""
    if "donations" not in st.session_state:
        st.session_state["donations"] = []
        
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_donation = {
        "id": len(st.session_state["donations"]) + 1,
        "user_id": user_id,
        "campaign_id": campaign_id,
        "nominal": nominal,
        "metode_pembayaran": metode,
        "anonim": 1 if anonim else 0,
        "bukti_transfer": bukti,
        "pesan": pesan,
        "tanggal_donasi": now_str
    }
    
    st.session_state["donations"].append(new_donation)


def get_all_donations():
    """Ambil semua riwayat donasi beserta nama kampanye dari session state."""
    if "donations" not in st.session_state:
        return []
        
    donations = st.session_state["donations"]
    result = []
    
    for d in sorted(donations, key=lambda x: x["tanggal_donasi"], reverse=True):
        d_copy = dict(d)
        campaign = get_campaign_by_id(d["campaign_id"])
        d_copy["program_judul"] = campaign["judul"] if campaign else "Program Donasi"
        result.append(d_copy)
        
    return result


def get_donation_count():
    """Hitung jumlah donasi (base stat + session)."""
    # Assuming around 150 previous donations + new ones in session
    base_count = 150
    session_count = len(st.session_state.get("donations", []))
    return base_count + session_count


def get_total_donated():
    """Total nominal seluruh donasi."""
    from utils.campaign import get_total_donasi
    return get_total_donasi()


def get_monthly_donations():
    """Ambil total donasi bulanan untuk grafik."""
    # Since we don't have DB, return empty list or dummy data
    return []