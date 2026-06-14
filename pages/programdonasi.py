import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.campaign import get_all_campaigns, search_campaigns, get_campaigns_by_category
from utils.helpers import img_to_base64, get_image_for_category, format_rupiah, calc_progress

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – PROGRAM DONASI PAGE
# Menampilkan kampanye dari DATABASE dengan search, filter, dan progress.
# ═══════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════
# CUSTOM CSS  –  Premium golden-accent + modern glassmorphism look
# ═══════════════════════════════════════════════════════════════════════
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background: linear-gradient(160deg, #111c11 0%, #0a140a 55%, #101a10 100%) !important; }
    header[data-testid="stHeader"] { background: transparent !important; }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-thumb { background: #2d4a2d; border-radius: 4px; }

    .page-header {
        text-align: center;
        padding: 3rem 0 2rem;
        animation: fadeInDown 0.8s ease-out;
    }
    .page-header h1 {
        font-family: 'DM Serif Display', serif !important;
        color: #f0ede6;
        font-size: 3.5rem;
        font-weight: 400;
        margin-bottom: 1rem;
        line-height: 1.1;
    }
    .page-header h1 span {
        background: linear-gradient(135deg, #e2c97a, #c9a84c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-style: italic;
    }
    .page-header p {
        color: #8a9e80;
        font-size: 1.15rem;
        max-width: 600px;
        margin: 0 auto;
    }

    /* Filter & Search UI */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stSelectbox"] > div {
        background-color: rgba(20, 30, 20, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f0ede6 !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stSelectbox"] > div:focus {
        border-color: #e2c97a !important;
        box-shadow: 0 0 0 2px rgba(247, 199, 55, 0.2) !important;
        background-color: rgba(20, 30, 20, 0.8) !important;
    }

    /* Program Card */
    .program-card {
        background: rgba(12, 20, 12, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 20px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .program-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px rgba(247, 199, 55, 0.1);
        border-color: rgba(247, 199, 55, 0.3);
    }
    .program-img-wrapper {
        position: relative;
        width: 100%;
        height: 220px;
        overflow: hidden;
    }
    .program-img-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.6s ease;
    }
    .program-card:hover .program-img-wrapper img {
        transform: scale(1.08);
    }
    .program-badge {
        position: absolute;
        top: 15px; left: 15px;
        background: rgba(10, 15, 28, 0.85);
        backdrop-filter: blur(4px);
        color: #e2c97a;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid rgba(247, 199, 55, 0.3);
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .program-card-body {
        padding: 1.8rem;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    .program-title {
        color: #f0ede6;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        line-height: 1.3;
    }
    .program-desc {
        color: #8a9e80;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        flex-grow: 1;
    }
    
    /* Progress Bar */
    .progress-bar-bg {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin-bottom: 0.6rem;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #e2c97a, #c9a84c);
        transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 10px rgba(247, 199, 55, 0.4);
    }
    .progress-stats {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: #a0b098;
        margin-bottom: 1.5rem;
    }
    .progress-stats span.terkumpul {
        color: #e2c97a;
        font-weight: 700;
    }
    
    /* Tombol Detail Custom */
    button[kind="secondary"] {
        display: block;
        width: 100%;
        background: rgba(247, 199, 55, 0.1) !important;
        color: #e2c97a !important;
        border: 1px solid rgba(247, 199, 55, 0.3) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        padding: 0.6rem !important;
    }
    button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #e2c97a, #c9a84c) !important;
        color: #0a140a !important;
        box-shadow: 0 4px 15px rgba(247, 199, 55, 0.3) !important;
        transform: translateY(-2px) !important;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    inject_custom_css()
    
    # ── Header ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="page-header">
        <h1>Jelajahi <span>Program Donasi</span></h1>
        <p>Temukan kampanye kebaikan yang sesuai dengan panggilan hati Anda</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Filter & Search Section ────────────────────────────────────────
    col_search, col_filter = st.columns([1, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Cari program donasi...", placeholder="Ketik kata kunci (misal: Sembako, Sekolah)")
    
    with col_filter:
        categories = ["Semua Kategori", "Pendidikan", "Kesehatan", "Bencana Alam", "Lingkungan", "Panti Asuhan"]
        selected_category = st.selectbox("📂 Filter Kategori", categories)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Fetch from Database ────────────────────────────────────────────
    if search_query:
        kampanye_list = search_campaigns(search_query)
    elif selected_category != "Semua Kategori":
        kampanye_list = get_campaigns_by_category(selected_category)
    else:
        kampanye_list = get_all_campaigns()

    # Apply both filters if both are set
    if search_query and selected_category != "Semua Kategori":
        kampanye_list = [c for c in kampanye_list if c["kategori"] == selected_category]

    # ── Render Cards ───────────────────────────────────────────────────
    if not kampanye_list:
        st.warning("Belum ada program donasi yang sesuai dengan pencarian atau filter Anda.")
        return

    cols = st.columns(3)
    
    for idx, prog in enumerate(kampanye_list):
        col = cols[idx % 3]
        img_path = get_image_for_category(prog["kategori"])
        img_b64 = img_to_base64(img_path)
        progress = calc_progress(prog["dana_terkumpul"], prog["target_dana"])
        
        with col:
            html_card = f"""
<div class="program-card">
<div class="program-img-wrapper">
<img src="{img_b64}" alt="{prog['judul']}" />
<span class="program-badge">{prog['kategori']}</span>
</div>
<div class="program-card-body">
<div class="program-title">{prog['judul']}</div>
<div class="program-desc">{prog['deskripsi']}</div>
<div class="progress-bar-bg">
<div class="progress-bar-fill" style="width: {progress}%;"></div>
</div>
<div class="progress-stats">
<span class="terkumpul">{format_rupiah(prog['dana_terkumpul'])}</span>
<span>{format_rupiah(prog['target_dana'])}</span>
</div>
</div>
</div>
<br>
"""
            st.markdown(html_card, unsafe_allow_html=True)
            
            if st.button("Lihat Detail & Donasi", key=f"btn_detail_{prog['id']}", use_container_width=True):
                st.session_state['selected_campaign_id'] = prog['id']
                st.switch_page("pages/donasi.py")

main()
