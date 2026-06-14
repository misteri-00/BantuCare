import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.campaign import get_all_campaigns, get_total_donasi, get_campaign_count
from utils.helpers import format_rupiah, get_donation_count, get_total_donated, get_monthly_donations
from utils.impact import get_total_impact

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – IMPACT TRACKER · Forest Luxury Theme
# ═══════════════════════════════════════════════════════════════════════

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp {
    background: linear-gradient(160deg, #111c11 0%, #0a140a 55%, #101a10 100%) !important;
    min-height: 100vh;
}
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, .stDeployButton { display: none !important; visibility: hidden !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #2d4a2d; border-radius: 4px; }

/* ── Page Header ── */
.it-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
}
.it-header .eyebrow {
    font-size: .68rem; font-weight: 700; letter-spacing: .14em;
    text-transform: uppercase; color: #c9a84c; display: block; margin-bottom: .4rem;
}
.it-header h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.2rem !important; font-weight: 400 !important;
    color: #f0ede6 !important; line-height: 1.15 !important;
    margin: 0 0 .4rem !important;
}
.it-header h1 em { font-style: italic; color: #e2c97a; }
.it-header p { color: #6a7a60; font-size: .88rem; margin: 0; max-width: 520px; margin: 0 auto; }

/* ── Section Titles ── */
.it-sec {
    margin: 2.5rem 0 1.25rem;
    display: flex; align-items: flex-end; justify-content: space-between; gap: 1rem;
}
.it-sec-eyebrow {
    font-size: .68rem; font-weight: 700; letter-spacing: .14em;
    text-transform: uppercase; color: #c9a84c; margin-bottom: .2rem;
}
.it-sec-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.5rem !important; font-weight: 400 !important;
    color: #f0ede6 !important; margin: 0 !important; line-height: 1.2 !important;
}
.it-sec-title em { font-style: italic; color: #e2c97a; }
.it-sec-sub { color: #6a7a60; font-size: .78rem; margin: .2rem 0 0; }

/* ── Stat Cards ── */
.it-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
.it-stat {
    background: rgba(15,25,15,.7);
    border: .5px solid rgba(201,168,76,.15);
    border-radius: 16px;
    padding: 1.5rem 1.6rem;
    transition: all .3s;
    position: relative; overflow: hidden;
    text-align: center;
}
.it-stat::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #c9a84c, transparent);
    opacity: 0; transition: opacity .3s;
}
.it-stat:hover { transform: translateY(-4px); border-color: rgba(201,168,76,.32);
                 box-shadow: 0 12px 36px rgba(0,0,0,.3); }
.it-stat:hover::before { opacity: 1; }
.it-stat-icon { font-size: 1.8rem; margin-bottom: .5rem; display: block; }
.it-stat-num {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.75rem !important; font-weight: 400 !important;
    color: #e2c97a !important; line-height: 1.1; margin-bottom: .25rem;
}
.it-stat-label { color: #6a7a60; font-size: .75rem; font-weight: 500; }

/* ── Impact Cards ── */
.it-impacts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.it-impact {
    background: rgba(12,20,12,.65);
    border: .5px solid rgba(255,255,255,.06);
    border-radius: 16px;
    padding: 1.4rem;
    text-align: center;
    transition: all .3s;
}
.it-impact:hover { border-color: rgba(201,168,76,.2); transform: translateY(-3px);
                   box-shadow: 0 12px 28px rgba(0,0,0,.3); }
.it-impact-icon { font-size: 2.2rem; margin-bottom: .5rem; display: block; }
.it-impact-num {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.5rem !important; font-weight: 400 !important;
    color: #e2c97a !important; margin-bottom: .15rem;
}
.it-impact-label { color: #8a9e80; font-size: .75rem; font-weight: 500; }

/* ── Chart Container ── */
.it-chart-box {
    background: rgba(12,20,12,.65);
    border: .5px solid rgba(201,168,76,.12);
    border-radius: 18px;
    padding: 1.5rem 1.75rem;
    margin-bottom: .5rem;
}
.it-chart-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1rem !important; color: #d4c9b0 !important;
    font-weight: 400 !important; text-align: center; margin: 0 0 1rem !important;
}

/* ── Map Container ── */
.it-map-box {
    background: rgba(12,20,12,.65);
    border: .5px solid rgba(201,168,76,.12);
    border-radius: 18px;
    padding: 1.25rem;
    overflow: hidden;
}

/* ── Page Wrapper ── */
.it-page { padding: 0 2rem 3rem; max-width: 1280px; margin: 0 auto; }

/* ── Streamlit overrides ── */
.stButton > button {
    border-radius: 10px !important;
    border: .5px solid rgba(201,168,76,.35) !important;
    color: #e2c97a !important;
    background: transparent !important;
    font-weight: 600 !important; font-size: .78rem !important;
    padding: .45rem 1rem !important; transition: all .18s !important;
}
.stButton > button:hover {
    background: rgba(201,168,76,.1) !important;
    border-color: rgba(201,168,76,.6) !important;
    transform: translateY(-1px) !important;
}
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg,#c9a84c,#a8852c) !important;
    color: #0f1a0f !important; font-weight: 700 !important;
    border: none !important; border-radius: 12px !important;
    padding: .7rem 2rem !important; font-size: .88rem !important;
}
</style>
""", unsafe_allow_html=True)


def main():
    inject_css()

    # ── Header ──
    st.markdown("""
<div class="it-header">
<span class="eyebrow">DonasiCare · Transparansi</span>
<h1>Impact <em>Tracker</em></h1>
<p>Lihat secara real-time bagaimana donasi Anda mengubah kehidupan nyata</p>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="it-page">', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # 1. DASHBOARD STATS
    # ═══════════════════════════════════════════
    st.markdown("""
<div class="it-sec">
<div>
<div class="it-sec-eyebrow">Dashboard</div>
<div class="it-sec-title">Ringkasan <em>Donasi</em></div>
<div class="it-sec-sub">Data real-time dari seluruh program</div>
</div>
</div>
""", unsafe_allow_html=True)

    total_donasi_kampanye = get_total_donasi()
    total_donated = get_total_donated()
    total_display = max(total_donasi_kampanye, total_donated) if total_donated > 0 else total_donasi_kampanye
    donor_count = get_donation_count()
    campaign_count = get_campaign_count()

    st.markdown(f"""
<div class="it-stats">
<div class="it-stat">
<span class="it-stat-icon">💰</span>
<div class="it-stat-num">{format_rupiah(total_display)}</div>
<div class="it-stat-label">Total Dana Terkumpul</div>
</div>
<div class="it-stat">
<span class="it-stat-icon">👥</span>
<div class="it-stat-num">{donor_count:,}</div>
<div class="it-stat-label">Jumlah Donatur</div>
</div>
<div class="it-stat">
<span class="it-stat-icon">📋</span>
<div class="it-stat-num">{campaign_count}</div>
<div class="it-stat-label">Program Aktif</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # 2. CHART
    # ═══════════════════════════════════════════
    st.markdown("""
<div class="it-sec">
<div>
<div class="it-sec-eyebrow">Grafik</div>
<div class="it-sec-title">Donasi per <em>Kampanye</em></div>
</div>
</div>
""", unsafe_allow_html=True)

    campaigns = get_all_campaigns()

    st.markdown('<div class="it-chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="it-chart-title">Dana Terkumpul (Jutaan Rupiah)</div>', unsafe_allow_html=True)
    if campaigns:
        chart_data = pd.DataFrame({
            c["judul"][:20]: [c["dana_terkumpul"] / 1_000_000] for c in campaigns
        })
        st.bar_chart(chart_data, height=350, use_container_width=True)
    else:
        st.info("Belum ada data kampanye.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # 3. IMPACT TRACKER
    # ═══════════════════════════════════════════
    st.markdown("""
<div class="it-sec">
<div>
<div class="it-sec-eyebrow">Dampak Nyata</div>
<div class="it-sec-title">Impact <em>Tracker</em></div>
<div class="it-sec-sub">Setiap angka merepresentasikan harapan baru yang Anda wujudkan</div>
</div>
</div>
""", unsafe_allow_html=True)

    impact = get_total_impact()
    penerima = f"{impact.get('penerima', 0):,}".replace(",", ".")
    laptop = f"{impact.get('laptop', 0):,}".replace(",", ".")
    pohon = f"{impact.get('pohon', 0):,}".replace(",", ".")
    sekolah = f"{impact.get('sekolah', 0):,}".replace(",", ".")

    st.markdown(f"""
<div class="it-impacts">
<div class="it-impact">
<span class="it-impact-icon">❤️</span>
<div class="it-impact-num">{penerima}</div>
<div class="it-impact-label">Penerima Manfaat</div>
</div>
<div class="it-impact">
<span class="it-impact-icon">💻</span>
<div class="it-impact-num">{laptop}</div>
<div class="it-impact-label">Laptop Dibagikan</div>
</div>
<div class="it-impact">
<span class="it-impact-icon">🌳</span>
<div class="it-impact-num">{pohon}</div>
<div class="it-impact-label">Pohon Ditanam</div>
</div>
<div class="it-impact">
<span class="it-impact-icon">🏫</span>
<div class="it-impact-num">{sekolah}</div>
<div class="it-impact-label">Sekolah Direnovasi</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════
    # 4. PETA SEBARAN
    # ═══════════════════════════════════════════
    st.markdown("""
<div class="it-sec">
<div>
<div class="it-sec-eyebrow">Jangkauan</div>
<div class="it-sec-title">Peta Sebaran <em>Bantuan</em></div>
<div class="it-sec-sub">Titik-titik penyaluran program di seluruh Indonesia</div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="it-map-box">', unsafe_allow_html=True)
    map_points = []
    for c in campaigns:
        if c.get("latitude") and c.get("longitude"):
            map_points.append({"lat": c["latitude"], "lon": c["longitude"]})

    if map_points:
        map_data = pd.DataFrame(map_points)
        st.map(map_data, zoom=4, color="#c9a84c", size=20)
    else:
        st.info("Belum ada data koordinat lokasi bantuan.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close it-page


if __name__ == "__main__":
    main()
