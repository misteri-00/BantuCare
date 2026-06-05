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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #0a0f1c 0%, #121a2e 50%, #0d1520 100%); }

    /* Hide default header */
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ── Header Titles ──────────────────────────────────────────── */
    .page-header {
        text-align: center;
        margin: 1rem 0 3rem 0;
        animation: fadeIn 0.8s ease;
    }
    .page-header h1 {
        color: #f1f5f9;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .page-header h1 span {
        background: linear-gradient(135deg, #f7c737, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .page-header p {
        color: #94a3b8;
        font-size: 1.1rem;
    }

    /* ── Filter & Search UI ──────────────────────────────────────── */
    div[data-testid="stTextInput"] input {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(247, 199, 55, 0.3) !important;
        color: #f1f5f9 !important;
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #f7c737 !important;
        box-shadow: 0 0 10px rgba(247, 199, 55, 0.2) !important;
    }

    /* ── Program Card ────────────────────────────────────────────── */
    .program-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .program-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        border-color: rgba(247, 199, 55, 0.25);
    }
    .program-img-wrapper {
        position: relative;
        width: 100%;
        height: 200px;
        overflow: hidden;
    }
    .program-img-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
    }
    .program-card:hover .program-img-wrapper img {
        transform: scale(1.05);
    }
    .program-badge {
        position: absolute;
        top: 15px; left: 15px;
        background: rgba(10, 15, 28, 0.8);
        backdrop-filter: blur(4px);
        color: #f7c737;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(247, 199, 55, 0.3);
    }
    .program-card-body {
        padding: 1.5rem;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    .program-title {
        color: #f1f5f9;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    .program-desc {
        color: #94a3b8;
        font-size: 0.85rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        flex-grow: 1;
    }
    .progress-bar-bg {
        background: rgba(255,255,255,0.08);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #f7c737, #f59e0b);
        transition: width 1.5s ease;
    }
    .progress-stats {
        display: flex;
        justify-content: space-between;
        font-size: 0.8rem;
        color: #cbd5e1;
        margin-bottom: 1.2rem;
    }
    .progress-stats span.terkumpul {
        color: #f7c737;
        font-weight: 700;
    }
    
    /* Tombol Detail Custom */
    .btn-detail {
        display: block;
        width: 100%;
        text-align: center;
        background: rgba(247, 199, 55, 0.1);
        color: #f7c737 !important;
        border: 1px solid rgba(247, 199, 55, 0.4);
        padding: 0.7rem;
        border-radius: 10px;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.3s ease;
        margin-top: auto;
    }
    .btn-detail:hover {
        background: linear-gradient(135deg, #f7c737, #f59e0b);
        color: #0a0f1c !important;
        box-shadow: 0 4px 15px rgba(247, 199, 55, 0.3);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
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
