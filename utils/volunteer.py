import streamlit as st
import datetime

# ═══════════════════════════════════════════════════════════════════════
# Volunteer CRUD helpers (Static Data Version)
# ═══════════════════════════════════════════════════════════════════════

def register_volunteer(nama, email, no_hp, event):
    """Daftarkan volunteer baru ke session state."""
    if "volunteers" not in st.session_state:
        st.session_state["volunteers"] = []
        
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_vol = {
        "id": len(st.session_state["volunteers"]) + 1,
        "nama": nama,
        "email": email,
        "no_hp": no_hp,
        "event": event,
        "tanggal_daftar": now_str
    }
    
    st.session_state["volunteers"].append(new_vol)


def get_all_volunteers():
    """Ambil semua data volunteer dari session state."""
    return sorted(st.session_state.get("volunteers", []), key=lambda x: x["tanggal_daftar"], reverse=True)


def get_volunteer_count():
    """Hitung jumlah volunteer terdaftar (base stat + session)."""
    base_count = 1250  # Dummy base count
    session_count = len(st.session_state.get("volunteers", []))
    return base_count + session_count
