import streamlit as st

# ── Page Configuration ──────────────────────────────────────────────
st.set_page_config(
    page_title="DonasiCare - Platform Donasi Terpercaya",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Define Pages ────────────────────────────────────────────────────
home = st.Page("pages/home.py", title="Home", icon="🏠", default=True, url_path="home")
program_donasi = st.Page("pages/programdonasi.py", title="Program Donasi", icon="📋", url_path="programdonasi")
ai_assistant = st.Page("pages/aichatbot.py", title="AI Assistant", icon="🤖", url_path="aichatbot")
donasi_sekarang = st.Page("pages/donasi.py", title="Donasi Sekarang", icon="💰", url_path="donasi")
transparansi = st.Page("pages/impacttracker.py", title="Transparansi", icon="📊", url_path="transparansi")
volunteer = st.Page("pages/volunteercenter.py", title="Volunteer", icon="🤝", url_path="volunteer")
tentang_kami = st.Page("pages/tentangkami.py", title="Tentang Kami", icon="ℹ️", url_path="tentangkami")
riwayat = st.Page("pages/riwayatdonasi.py", title="Riwayat Donasi", icon="📜", url_path="riwayat")
peta_bantuan = st.Page("pages/petabantuan.py", title="Peta Bantuan", icon="🗺️", url_path="petabantuan")

# ── Navigation ──────────────────────────────────────────────────────
pg = st.navigation(
    {
        "Menu Utama": [home, program_donasi, ai_assistant, donasi_sekarang],
        "Informasi": [transparansi, volunteer, peta_bantuan, tentang_kami],
        "Lainnya": [riwayat],
    }
)

pg.run()
