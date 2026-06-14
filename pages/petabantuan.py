import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.campaign import get_all_campaigns

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – PETA BANTUAN · Forest Luxury Theme
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
.pb-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
}
.pb-header .eyebrow {
    font-size: .68rem; font-weight: 700; letter-spacing: .14em;
    text-transform: uppercase; color: #c9a84c; display: block; margin-bottom: .4rem;
}
.pb-header h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.2rem !important; font-weight: 400 !important;
    color: #f0ede6 !important; line-height: 1.15 !important;
    margin: 0 0 .4rem !important;
}
.pb-header h1 em { font-style: italic; color: #e2c97a; }
.pb-header p { color: #6a7a60; font-size: .88rem; margin: 0; max-width: 520px; margin: 0 auto; }

/* ── Page Wrapper ── */
.pb-page { padding: 0 2rem 3rem; max-width: 1280px; margin: 0 auto; }

/* ── Description Card ── */
.pb-desc {
    background: rgba(12,20,12,.65);
    border: .5px solid rgba(201,168,76,.15);
    border-radius: 18px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    display: flex; align-items: center; gap: 1.2rem;
}
.pb-desc-icon {
    font-size: 2.2rem; flex-shrink: 0;
}
.pb-desc-text h3 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.15rem !important; font-weight: 400 !important;
    color: #f0ede6 !important; margin: 0 0 .3rem !important;
}
.pb-desc-text p {
    color: #6a7a60; font-size: .82rem; line-height: 1.7; margin: 0;
}

/* ── Map Container ── */
.pb-map-box {
    background: rgba(12,20,12,.65);
    border: .5px solid rgba(201,168,76,.12);
    border-radius: 18px;
    padding: 1.25rem;
    overflow: hidden;
    margin-bottom: 1.5rem;
}

/* ── Stats Row ── */
.pb-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.pb-stat {
    background: rgba(15,25,15,.7);
    border: .5px solid rgba(201,168,76,.15);
    border-radius: 14px;
    padding: 1.1rem;
    text-align: center;
    transition: all .3s;
}
.pb-stat:hover { transform: translateY(-3px); border-color: rgba(201,168,76,.3); }
.pb-stat-icon { font-size: 1.4rem; margin-bottom: .3rem; display: block; }
.pb-stat-num {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.35rem !important; font-weight: 400 !important;
    color: #e2c97a !important; margin-bottom: .1rem;
}
.pb-stat-label { color: #6a7a60; font-size: .7rem; font-weight: 500; }

/* ── Location Cards ── */
.pb-locations { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.pb-loc {
    background: rgba(12,20,12,.65);
    border: .5px solid rgba(255,255,255,.06);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    display: flex; align-items: center; gap: 1rem;
    transition: all .3s;
}
.pb-loc:hover { border-color: rgba(201,168,76,.2); transform: translateY(-2px); }
.pb-loc-icon {
    width: 42px; height: 42px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.pb-loc-name { color: #f0ede6; font-size: .85rem; font-weight: 600; }
.pb-loc-cat { color: #6a7a60; font-size: .72rem; margin-top: 1px; }

/* ── Selectbox ── */
[data-baseweb="select"] > div:first-child {
    background: rgba(15,25,15,.7) !important;
    border: .5px solid rgba(201,168,76,.22) !important;
    border-radius: 12px !important;
}
[data-baseweb="select"] span { color: #f0ede6 !important; font-size: .82rem !important; }
[data-baseweb="select"] svg { fill: #c9a84c !important; }
label { color: #c9a84c !important; font-size: .72rem !important; font-weight: 600 !important;
        letter-spacing: .05em !important; text-transform: uppercase !important; }
</style>
""", unsafe_allow_html=True)


CAT_BG = {
    "Pendidikan":    "rgba(96,165,250,.15)",
    "Kesehatan":     "rgba(52,211,153,.15)",
    "Lingkungan":    "rgba(74,222,128,.15)",
    "Bencana Alam":  "rgba(251,146,60,.15)",
    "Pemberdayaan":  "rgba(167,139,250,.15)",
}
CAT_EMOJI = {
    "Pendidikan": "🎓", "Kesehatan": "🏥", "Lingkungan": "🌿",
    "Bencana Alam": "🆘", "Pemberdayaan": "💼",
}


def main():
    inject_css()

    # ── Header ──
    st.markdown("""
<div class="pb-header">
<span class="eyebrow">DonasiCare · Jangkauan</span>
<h1>Peta <em>Bantuan</em></h1>
<p>Sebaran lokasi program donasi dan penerima bantuan di seluruh Indonesia</p>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="pb-page">', unsafe_allow_html=True)

    # ── Description ──
    st.markdown("""
<div class="pb-desc">
<div class="pb-desc-icon">📍</div>
<div class="pb-desc-text">
<h3>Titik Penyaluran Bantuan</h3>
<p>Peta di bawah menunjukkan lokasi-lokasi di mana DonasiCare telah menyalurkan bantuan. Setiap titik merepresentasikan satu area program aktif.</p>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Data ──
    data_lokasi = pd.DataFrame({
        'latitude':  [-6.2088, -7.2504, -6.9175,  3.5952, -5.1477, -7.7956, -0.9471, -3.3167,  1.4748, -8.6500],
        'longitude': [106.8456, 112.7688, 107.6191, 98.6722, 119.4327, 110.3695, 100.3658, 114.5901, 124.8421, 115.2167],
        'kota':     ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Makassar', 'Yogyakarta', 'Padang', 'Banjarmasin', 'Manado', 'Denpasar'],
        'bantuan':  ['Pendidikan', 'Kesehatan', 'Lingkungan', 'Bencana Alam', 'Pemberdayaan', 'Pendidikan', 'Bencana Alam', 'Kesehatan', 'Lingkungan', 'Pemberdayaan']
    })

    # ── Stats ──
    cats_count = data_lokasi['bantuan'].value_counts()
    st.markdown(f"""
<div class="pb-stats">
<div class="pb-stat">
<span class="pb-stat-icon">📍</span>
<div class="pb-stat-num">{len(data_lokasi)}</div>
<div class="pb-stat-label">Total Titik Bantuan</div>
</div>
<div class="pb-stat">
<span class="pb-stat-icon">🏝️</span>
<div class="pb-stat-num">{len(data_lokasi['kota'].unique())}</div>
<div class="pb-stat-label">Kota Terjangkau</div>
</div>
<div class="pb-stat">
<span class="pb-stat-icon">📂</span>
<div class="pb-stat-num">{len(cats_count)}</div>
<div class="pb-stat-label">Kategori Bantuan</div>
</div>
<div class="pb-stat">
<span class="pb-stat-icon">🌍</span>
<div class="pb-stat-num">34</div>
<div class="pb-stat-label">Provinsi Target</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Filter ──
    kategori_pilihan = st.selectbox(
        "Filter Kategori Bantuan",
        ["Semua Kategori", "Pendidikan", "Kesehatan", "Lingkungan", "Bencana Alam", "Pemberdayaan"]
    )

    if kategori_pilihan != "Semua Kategori":
        data_tampil = data_lokasi[data_lokasi['bantuan'] == kategori_pilihan]
    else:
        data_tampil = data_lokasi

    # ── Map ──
    st.markdown('<div class="pb-map-box">', unsafe_allow_html=True)
    if not data_tampil.empty:
        st.map(data_tampil, zoom=4, color="#c9a84c", size=25)
    else:
        st.info("Belum ada data untuk kategori ini.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Location Cards ──
    if not data_tampil.empty:
        st.markdown(f"""
<div style="color:#8a9e80; font-size:.8rem; margin-bottom:.8rem; font-weight:500;">
Menampilkan <strong style="color:#e2c97a">{len(data_tampil)}</strong> titik penyaluran bantuan
</div>
""", unsafe_allow_html=True)

        locs_html = '<div class="pb-locations">'
        for _, row in data_tampil.iterrows():
            cat = row['bantuan']
            bg = CAT_BG.get(cat, "rgba(201,168,76,.1)")
            emoji = CAT_EMOJI.get(cat, "📦")
            locs_html += f"""
<div class="pb-loc">
<div class="pb-loc-icon" style="background:{bg}">{emoji}</div>
<div>
<div class="pb-loc-name">{row['kota']}</div>
<div class="pb-loc-cat">{cat}</div>
</div>
</div>"""
        locs_html += '</div>'
        st.markdown(locs_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close pb-page


if __name__ == "__main__":
    main()
