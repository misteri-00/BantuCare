import streamlit as st
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.campaign import get_all_campaigns, get_total_donasi, get_campaign_count
from utils.helpers import format_rupiah, get_donation_count, get_total_donated, get_monthly_donations
from utils.impact import get_total_impact

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – TRANSPARANSI PAGE
# Connected to SQLite: Dashboard, Impact Tracker, Peta Bantuan
# ═══════════════════════════════════════════════════════════════════════

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #0a0f1c 0%, #121a2e 50%, #0d1520 100%); }
    header[data-testid="stHeader"] { background: transparent !important; }

    .page-header {
        text-align: center;
        margin: 1rem 0 3rem 0;
        animation: fadeIn 0.8s ease;
    }
    .page-header h1 { color: #f1f5f9; font-size: 2.8rem; font-weight: 800; margin-bottom: 0.5rem; }
    .page-header h1 span { background: linear-gradient(135deg, #f7c737, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .page-header p { color: #94a3b8; font-size: 1.1rem; }

    .section-title {
        color: #f7c737;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(247, 199, 55, 0.2);
        padding-bottom: 0.5rem;
    }

    .metric-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: rgba(247, 199, 55, 0.3);
    }
    .metric-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #f1f5f9;
        margin-bottom: 0.2rem;
    }
    .metric-label { color: #94a3b8; font-size: 0.9rem; font-weight: 500; }

    .viz-container {
        background: rgba(30, 41, 59, 0.3);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    inject_custom_css()

    st.markdown("""
    <div class="page-header">
        <h1>Transparansi & <span>Dampak</span></h1>
        <p>Lihat secara real-time bagaimana kebaikan Anda tersalurkan dan mengubah dunia</p>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # 1. DASHBOARD DONASI (from DB)
    # ==========================================
    st.markdown('<div class="section-title">Dashboard Donasi</div>', unsafe_allow_html=True)
    
    # Ambil data dari database
    total_donasi_kampanye = get_total_donasi()  # Total dari campaigns.dana_terkumpul
    total_donated = get_total_donated()          # Total dari donations table
    total_display = max(total_donasi_kampanye, total_donated) if total_donated > 0 else total_donasi_kampanye
    donor_count = get_donation_count()
    campaign_count = get_campaign_count()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">💰</div>
            <div class="metric-value">{format_rupiah(total_display)}</div>
            <div class="metric-label">Total Donasi Terkumpul</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-value">{donor_count}</div>
            <div class="metric-label">Jumlah Donatur</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">📦</div>
            <div class="metric-value">{campaign_count}</div>
            <div class="metric-label">Program Aktif</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grafik Bulanan dari DB
    st.markdown('<div class="viz-container">', unsafe_allow_html=True)
    st.markdown("<h4 style='color:#f1f5f9; text-align:center; margin-bottom:1rem;'>Grafik Donasi per Kampanye (Jutaan Rupiah)</h4>", unsafe_allow_html=True)
    
    campaigns = get_all_campaigns()
    if campaigns:
        chart_data = pd.DataFrame({
            c["judul"][:20]: [c["dana_terkumpul"] / 1_000_000] for c in campaigns
        })
        st.bar_chart(chart_data, height=350, use_container_width=True)
    else:
        st.info("Belum ada data kampanye untuk ditampilkan.")

    st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # 2. IMPACT TRACKER (from DB)
    # ==========================================
    st.markdown('<div class="section-title">Impact Tracker</div>', unsafe_allow_html=True)
    st.write("Setiap angka di bawah ini merepresentasikan nyawa dan harapan baru yang telah Anda wujudkan.")
    
    impact = get_total_impact()
    penerima = f"{impact.get('penerima', 0):,}".replace(",", ".")
    laptop = f"{impact.get('laptop', 0):,}".replace(",", ".")
    pohon = f"{impact.get('pohon', 0):,}".replace(",", ".")
    sekolah = f"{impact.get('sekolah', 0):,}".replace(",", ".")

    ic1, ic2, ic3, ic4 = st.columns(4)
    impact_data = [
        ("❤️", penerima, "Penerima Manfaat", ic1),
        ("💻", laptop, "Laptop Dibagikan", ic2),
        ("🌳", pohon, "Pohon Ditanam", ic3),
        ("🏫", sekolah, "Sekolah Direnovasi", ic4)
    ]
    
    for icon, value, label, col in impact_data:
        with col:
            st.markdown(f"""
            <div class="metric-card" style="padding: 1rem;">
                <div class="metric-icon" style="font-size:2rem;">{icon}</div>
                <div class="metric-value" style="font-size:1.4rem; color:#f59e0b;">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


    # ==========================================
    # 3. PETA BANTUAN (from DB campaigns lat/lon)
    # ==========================================
    st.markdown('<div class="section-title">Peta Sebaran Bantuan</div>', unsafe_allow_html=True)
    st.write("Lokasi titik-titik penyaluran program bantuan kami di seluruh Indonesia.")
    
    st.markdown('<div class="viz-container">', unsafe_allow_html=True)
    
    # Ambil koordinat dari kampanye yang punya latitude/longitude
    map_points = []
    for c in campaigns:
        if c.get("latitude") and c.get("longitude"):
            map_points.append({"lat": c["latitude"], "lon": c["longitude"]})
    
    if map_points:
        map_data = pd.DataFrame(map_points)
        st.map(map_data, zoom=4, color="#f7c737", size=20)
    else:
        st.info("Belum ada data koordinat lokasi bantuan.")

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
