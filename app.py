import streamlit as st

# ── Page Configuration ──────────────────────────────────────────────
st.set_page_config(
    page_title="DonasiCare - Platform Donasi Terpercaya",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Define Pages ────────────────────────────────────────────────────
home = st.Page(
    "pages/home.py",
    title="Home",
    icon="🏠",
    default=True
)

program_donasi = st.Page(
    "pages/programdonasi.py",
    title="Program Donasi",
    icon="📋"
)

ai_assistant = st.Page(
    "pages/aichatbot.py",
    title="AI Assistant",
    icon="🤖"
)

donasi = st.Page(
    "pages/donasi.py",
    title="Donasi",
    icon="💰"
)

impact_tracker = st.Page(
    "pages/impacttracker.py",
    title="Impact Tracker",
    icon="📊"
)

volunteer_center = st.Page(
    "pages/volunteercenter.py",
    title="Volunteer Center",
    icon="🤝"
)

tentang_kami = st.Page(
    "pages/tentangkami.py",
    title="Tentang Kami",
    icon="ℹ️"
)

riwayat_donasi = st.Page(
    "pages/riwayatdonasi.py",
    title="Riwayat Donasi",
    icon="📜"
)

peta_bantuan = st.Page(
    "pages/petabantuan.py",
    title="Peta Bantuan",
    icon="🗺️"
)

dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    icon="📈"
)

# ── Navigation ──────────────────────────────────────────────────────
pg = st.navigation(
    {
        "🏠 Menu Utama": [
            home,
            dashboard,
            program_donasi,
            donasi,
            ai_assistant,
        ],

        "📊 Monitoring": [
            impact_tracker,
            peta_bantuan,
            riwayat_donasi,
        ],

        "🤝 Komunitas": [
            volunteer_center,
        ],

        "ℹ️ Informasi": [
            tentang_kami,
        ],
    }
)

pg.run()