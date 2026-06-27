import streamlit as st
from utils.navbar_dark import render_navbar
import time
import sys
import os
import re
import random
import datetime
import json

st.set_page_config(
    page_title="DonasiCare AI Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# ══════════════════════════════════════════════════════════════════════
# IMPORTS dari utils (database-connected)
# ══════════════════════════════════════════════════════════════════════
from utils.chatbot import generate_smart_response, save_chat, stream_text, classify_intent
from utils.campaign import get_all_campaigns, get_campaigns_by_category, get_total_donasi, get_campaign_count
from utils.helpers import format_rupiah, save_donation, get_donation_count
import time


# ══════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════
def calc_progress(terkumpul, target):
    return round((terkumpul / target) * 100) if target else 0

def render_inline_donation_form(key_index):
    st.markdown("<div style='background:rgba(201,168,76,0.1); border:1px solid rgba(201,168,76,0.3); padding:1rem; border-radius:12px; margin-top:0.5rem; margin-bottom:1rem;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#e2c97a; margin-top:0;'>💳 Donasi Langsung</h4>", unsafe_allow_html=True)
    
    step_key = f"donasi_step_{key_index}"
    if step_key not in st.session_state:
        st.session_state[step_key] = 1

    if st.session_state[step_key] == 1:
        campaigns = get_all_campaigns()
        prog_names = [c["judul"] for c in campaigns]
        
        with st.form(key=f"inline_donasi_form_{key_index}"):
            prog = st.selectbox("Pilih Program", prog_names)
            nom = st.number_input("Nominal (Rp)", min_value=10000, step=10000)
            
            c1, c2 = st.columns(2)
            nama = c1.text_input("Nama Anda (Kosong = Anonim)")
            metode = c2.selectbox("Metode Pembayaran", ["BCA", "Mandiri", "BNI", "BRI", "GoPay", "OVO", "Dana", "QRIS"])
            
            if st.form_submit_button("Lanjut Pembayaran", type="primary"):
                st.session_state[f"donasi_data_{key_index}"] = {
                    "prog": prog, "nom": nom, "nama": nama, "metode": metode,
                    "c_id": next(c["id"] for c in campaigns if c["judul"] == prog)
                }
                st.session_state[step_key] = 2
                st.rerun()

    elif st.session_state[step_key] == 2:
        data = st.session_state[f"donasi_data_{key_index}"]
        nom = data["nom"]
        metode = data["metode"]
        prog = data["prog"]

        st.markdown(f"""
<div style='background:rgba(15,25,15,.7); border:.5px solid rgba(201,168,76,.2); border-radius:10px; padding:.8rem 1rem; margin-bottom:.8rem;'>
<p style='margin:0; font-size:.78rem; color:#9aaa8a;'>Program: <strong style='color:#e2c97a;'>{prog}</strong></p>
<p style='margin:0; font-size:.78rem; color:#9aaa8a;'>Nominal: <strong style='color:#e2c97a;'>{format_rupiah(nom)}</strong> &nbsp;·&nbsp; Via: <strong style='color:#e2c97a;'>{metode}</strong></p>
</div>
""", unsafe_allow_html=True)

        st.info(f"Mohon selesaikan pembayaran sebesar **{format_rupiah(nom)}**.")

        # Simulasi tampilan pembayaran
        if metode == "QRIS":
            st.markdown("<div style='text-align:center; padding:1rem; background:white; border-radius:8px; margin-bottom:1rem;'>", unsafe_allow_html=True)
            st.image("https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg", width=150)
            st.markdown("<p style='color:black; font-weight:bold;'>Scan QRIS ini dengan aplikasi M-Banking atau E-Wallet Anda</p></div>", unsafe_allow_html=True)
        elif metode in ["GoPay", "OVO", "Dana"]:
            st.markdown(f"""
<div style='background:rgba(0,0,0,0.3); padding:1rem; border-radius:8px; text-align:center; margin-bottom:1rem;'>
<p>Buka aplikasi <b>{metode}</b> Anda dan transfer ke nomor:</p>
<h3 style='color:#4ade80; letter-spacing:2px;'>0812-3456-7890</h3>
<p style='font-size:0.8rem; color:#aaa;'>a.n. Yayasan DonasiCare</p>
</div>
""", unsafe_allow_html=True)
        else:
            # Virtual Account Bank
            va_num = f"{10203040 if metode=='BCA' else 998877}{int(time.time()) % 100000}"
            st.markdown(f"""
<div style='background:rgba(0,0,0,0.3); padding:1rem; border-radius:8px; text-align:center; margin-bottom:1rem;'>
<p>Transfer Virtual Account <b>Bank {metode}</b>:</p>
<h3 style='color:#4ade80; letter-spacing:2px;'>{va_num}</h3>
<p style='font-size:0.8rem; color:#aaa;'>a.n. Yayasan DonasiCare</p>
</div>
""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        if col1.button("Batal", key=f"btn_batal_{key_index}"):
            st.session_state[step_key] = 1
            st.rerun()
            
        if col2.button("✅ Konfirmasi Pembayaran", type="primary", key=f"btn_konfirm_{key_index}"):
            prog = data["prog"]
            c_id = data["c_id"]
            nama = data["nama"]
            final_name = nama if nama else "Anonim"
            is_anon = 1 if not nama else 0
            
            save_donation(None, c_id, nom, metode, is_anon, "", f"Donasi via Chat oleh {final_name}")
            
            if "riwayat_donasi" not in st.session_state:
                st.session_state.riwayat_donasi = []
            
            import datetime
            dt_now = datetime.datetime.now().strftime("%d %b %Y, %H:%M WIB")
            
            st.session_state.riwayat_donasi.append({
                "tx_id": f"TX-CHAT-{int(time.time())}",
                "program": prog,
                "amount": nom,
                "method": metode,
                "name": final_name,
                "date": dt_now
            })
            
            st.session_state[step_key] = 3
            st.rerun()

    elif st.session_state[step_key] == 3:
        st.success("✅ Pembayaran berhasil dikonfirmasi! Terima kasih atas kebaikan Anda.")
        if st.button("📜 Lihat Riwayat Donasi", key=f"btn_riwayat_{key_index}"):
            st.switch_page("pages/riwayatdonasi.py")
                
    st.markdown("</div>", unsafe_allow_html=True)


REKOMENDASI_MAP = {
    "Pendidikan Anak":        "Pendidikan",
    "Kesehatan & Medis":      "Kesehatan",
    "Pelestarian Lingkungan": "Lingkungan",
    "Pemberdayaan Ekonomi":   "Ekonomi",
    "Bantuan Bencana Alam":   "Bencana Alam",
}

def get_recommendations(minat_list):
    cats = {REKOMENDASI_MAP.get(m) for m in minat_list if m in REKOMENDASI_MAP}
    all_campaigns = get_all_campaigns()
    hasil = [c for c in all_campaigns if c["kategori"] in cats]
    return hasil or all_campaigns[:2]


# ══════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    .stApp { background: linear-gradient(160deg, #1a2e1a 0%, #0f1f0f 55%, #1c2a1a 100%) !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .block-container { padding-top: 1rem !important; padding-left:1.5rem !important; padding-right:1.5rem !important; max-width:100% !important; }
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-thumb { background: #3a5a3a; border-radius: 4px; }

    .pg-header { text-align:center; padding:1.2rem 0 1.5rem; }
    .pg-header .eyebrow { font-size:11px; font-weight:600; letter-spacing:.14em; text-transform:uppercase; color:#c9a84c; display:block; margin-bottom:.4rem; }
    .pg-header h1 { font-family:'DM Serif Display',serif !important; font-size:2rem !important; font-weight:400 !important; color:#f0ede6 !important; line-height:1.15 !important; margin:0 0 .3rem !important; }
    .pg-header h1 em { font-style:italic; color:#e2c97a; }
    .pg-header p { color:#9aaa8a; font-size:.88rem; margin:0; }

    div[data-baseweb="tab-list"] { gap:4px !important; background:rgba(15,31,15,.8) !important; padding:5px !important; border-radius:14px !important; border:.5px solid rgba(201,168,76,.2) !important; }
    div[data-baseweb="tab"] { color:#9aaa8a !important; font-weight:600 !important; font-size:.76rem !important; border-radius:10px !important; padding:.4rem .8rem !important; }
    div[data-baseweb="tab"][aria-selected="true"] { background:rgba(201,168,76,.14) !important; color:#e2c97a !important; border:.5px solid rgba(201,168,76,.3) !important; }
    div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display:none !important; }

    .g-card { background:rgba(15,25,15,.6); backdrop-filter:blur(12px); border:.5px solid rgba(201,168,76,.18); border-radius:18px; padding:1.5rem 1.75rem; margin-bottom:1.25rem; }
    .g-card h3 { font-family:'DM Serif Display',serif !important; font-size:1.2rem; font-weight:400; color:#f0ede6; margin:0 0 .3rem; }
    .g-card .sub { color:#9aaa8a; font-size:.8rem; line-height:1.6; margin:0 0 1rem; }

    .stButton > button { border-radius:20px !important; border:.5px solid rgba(201,168,76,.35) !important; color:#e2c97a !important; background:transparent !important; font-weight:600 !important; font-size:.75rem !important; padding:.32rem .85rem !important; transition:all .18s !important; height:auto !important; line-height:1.4 !important; }
    .stButton > button:hover { background:rgba(201,168,76,.13) !important; border-color:rgba(201,168,76,.6) !important; transform:translateY(-1px) !important; }
    [data-testid="baseButton-primary"] { background:linear-gradient(135deg,#c9a84c,#a8852c) !important; color:#1a2e1a !important; font-weight:700 !important; border:none !important; border-radius:10px !important; padding:.5rem 1.2rem !important; font-size:.82rem !important; }
    [data-testid="baseButton-primary"]:hover { opacity:.88 !important; transform:translateY(-1px) !important; }

    label, .stSelectbox label, .stMultiSelect label, .stTextInput label, .stNumberInput label, .stTextArea label { color:#c9a84c !important; font-size:.72rem !important; font-weight:600 !important; letter-spacing:.05em !important; text-transform:uppercase !important; }
    .stTextInput input, .stNumberInput input { background:rgba(47,74,47,.35) !important; border:.5px solid rgba(201,168,76,.22) !important; border-radius:10px !important; color:#f0ede6 !important; font-size:.82rem !important; }
    .stTextArea textarea { background:rgba(8,16,8,.7) !important; border:.5px solid rgba(201,168,76,.25) !important; border-radius:12px !important; color:#c8ddc0 !important; font-size:.81rem !important; line-height:1.7 !important; }

    [data-baseweb="select"] > div:first-child { background:rgba(47,74,47,.35) !important; border:.5px solid rgba(201,168,76,.22) !important; border-radius:10px !important; }
    [data-baseweb="select"] span { color:#f0ede6 !important; font-size:.82rem !important; }
    [data-baseweb="select"] svg { fill:#c9a84c !important; }
    [data-baseweb="tag"] { background:rgba(201,168,76,.15) !important; border:.5px solid rgba(201,168,76,.35) !important; border-radius:20px !important; }
    [data-baseweb="tag"] span { color:#e2c97a !important; font-size:.74rem !important; }
    [data-baseweb="popover"] ul { background:#152015 !important; border:.5px solid rgba(201,168,76,.2) !important; border-radius:10px !important; }
    [data-baseweb="popover"] li { color:#c8ddc0 !important; font-size:.8rem !important; }
    [data-baseweb="popover"] li:hover { background:rgba(201,168,76,.1) !important; }

    [data-testid="stExpander"] { background:rgba(15,25,15,.55) !important; border:.5px solid rgba(201,168,76,.15) !important; border-radius:13px !important; margin-bottom:.65rem !important; }
    [data-testid="stExpander"] summary { color:#f0ede6 !important; font-weight:600 !important; font-size:.85rem !important; padding:.9rem 1.1rem !important; }
    [data-testid="stExpander"] summary svg { fill:#c9a84c !important; }
    [data-testid="stExpander"] > div > div { padding:0 1.1rem 1rem !important; }
    [data-testid="stExpander"] p { color:#a3b89e !important; font-size:.8rem !important; line-height:1.65 !important; }
    [data-testid="stExpander"] strong { color:#e2c97a !important; }

    [data-testid="stAlert"] { border-radius:12px !important; border:.5px solid rgba(201,168,76,.2) !important; border-left:2px solid rgba(201,168,76,.5) !important; background:rgba(47,74,47,.3) !important; }
    [data-testid="stAlert"] p { color:#c8ddc0 !important; font-size:.81rem !important; }
    [data-testid="stSpinner"] p { color:#9aaa8a !important; font-size:.8rem !important; }

    .rc { background:rgba(47,74,47,.3); border:.5px solid rgba(77,160,77,.22); border-left:2.5px solid #4ade80; border-radius:12px; padding:1rem 1.2rem; margin-top:.8rem; }
    .rc h4 { font-size:.87rem !important; font-weight:600; color:#86efac; margin:0 0 4px; }
    .rc p { font-size:.78rem; color:#a3b89e; line-height:1.5; margin:0; }
    .rc .rmeta { font-size:.7rem; color:#5a6a50; margin-top:5px; }
    .rc .rdana { font-size:.78rem; color:#e2c97a; font-weight:600; margin-top:5px; }
    .pb { height:4px; background:rgba(201,168,76,.12); border-radius:4px; margin-top:8px; }
    .pf { height:4px; border-radius:4px; background:linear-gradient(90deg,#c9a84c,#86efac); }

    .estat { display:inline-flex; align-items:center; gap:7px; background:rgba(201,168,76,.1); border:.5px solid rgba(201,168,76,.22); border-radius:8px; padding:.35rem .8rem; margin:.25rem .25rem 0 0; }
    .estat .en { font-size:1rem; font-weight:700; color:#e2c97a; font-family:'DM Serif Display',serif; }
    .estat .el { font-size:.7rem; color:#9aaa8a; }

    hr { border-color:rgba(201,168,76,.1) !important; margin:1rem 0 !important; }

    /* hide bridge input */
    div[data-testid="stTextInput"]:has(input[aria-label="__cb_bridge__"]) {
        position:fixed !important; left:-9999px !important;
        opacity:0 !important; pointer-events:none !important;
        height:0 !important; overflow:hidden !important;
    }

    /* ══ CHATBOT HEADER CARD ══ */
    .chat-header-card {
        background: linear-gradient(135deg, rgba(20,34,20,.8), rgba(12,22,12,.9));
        border: .5px solid rgba(201,168,76,.25);
        border-radius: 18px;
        padding: 1.2rem 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 24px rgba(0,0,0,.25);
    }
    .chat-avatar-ring {
        width: 52px; height: 52px;
        border-radius: 14px;
        background: linear-gradient(135deg, #c9a84c, #86efac);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6rem;
        box-shadow: 0 4px 16px rgba(201,168,76,.3);
        flex-shrink: 0;
    }
    .chat-header-info h3 {
        font-family: 'DM Serif Display', serif !important;
        color: #f0ede6;
        font-size: 1.3rem;
        font-weight: 400;
        margin: 0 0 .15rem;
        line-height: 1.2;
    }
    .chat-header-info .status-line {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .status-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 6px rgba(74,222,128,.5);
        animation: statusPulse 2s ease-in-out infinite;
    }
    .status-text {
        color: #8a9e80;
        font-size: .75rem;
        font-weight: 500;
    }
    .chat-header-info .desc {
        color: #6a7a60;
        font-size: .72rem;
        margin: .3rem 0 0;
    }

    @keyframes statusPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: .5; transform: scale(.85); }
    }

    /* ══ CHAT MESSAGES (NO BUBBLES) ══ */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: .6rem 0 !important;
    }
    [data-testid="stChatMessage"][data-testid-role="assistant"] > div:last-child {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: .4rem 0 !important;
    }
    [data-testid="stChatMessage"][data-testid-role="user"] > div:last-child {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: .4rem 0 !important;
    }
    [data-testid="stChatMessage"] p {
        color: #d0dcc8 !important;
        font-size: .88rem !important;
        line-height: 1.65 !important;
    }
    [data-testid="stChatMessage"] strong {
        color: #e2c97a !important;
    }

    /* Chat container */
    [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stChatMessage"]) {
        background: rgba(8,14,8,.3) !important;
        border: .5px solid rgba(201,168,76,.08) !important;
        border-radius: 16px !important;
    }

    /* Chat input */
    [data-testid="stChatInput"] {
        background: rgba(15,25,15,.7) !important;
        border: .5px solid rgba(201,168,76,.2) !important;
        border-radius: 14px !important;
        padding: .2rem !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #d0dcc8 !important;
        font-size: .88rem !important;
    }
    [data-testid="stChatInput"] button {
        color: #c9a84c !important;
    }
    [data-testid="stChatInput"] button:hover {
        background: rgba(201,168,76,.15) !important;
    }

    /* ══ QUICK REPLY CHIPS ══ */
    .qr-label {
        font-size: .72rem;
        font-weight: 600;
        color: #c9a84c;
        letter-spacing: .06em;
        text-transform: uppercase;
        margin: .8rem 0 .4rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .qr-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: rgba(201,168,76,.15);
    }
    </style>
    """, unsafe_allow_html=True)






# ══════════════════════════════════════════════════════════════════════
# TAB 1 — CHATBOT + KERANJANG (layout 2 kolom)
# ══════════════════════════════════════════════════════════════════════
def tab_chatbot():
    # Init session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content":
            "Halo, Kak! 👋 Saya **CareBot**, asisten AI DonasiCare.\n\n"
            "Setiap kebaikan kecil sangat berarti bagi mereka yang membutuhkan. "
            "Kira-kira, program donasi seperti apa yang sedang Kakak cari hari ini? "
            "Apakah Kakak tertarik pada program pendidikan, kesehatan, lingkungan, atau mungkin bantuan bencana alam?"}]
    if "keranjang" not in st.session_state:
        st.session_state.keranjang = []
    if "quick_prompt" not in st.session_state:
        st.session_state.quick_prompt = None

    # ── Layout: Chat + Program Sidebar ──
    chat_col, prog_col = st.columns([2.2, 1])

    with prog_col:
        st.markdown("""
<div style='background:rgba(15,25,15,.7); border:.5px solid rgba(201,168,76,.2); border-radius:14px; padding:1.1rem 1.2rem; margin-bottom:.5rem;'>
<h4 style='font-family:"DM Serif Display",serif; color:#e2c97a; font-size:1rem; font-weight:400; margin:0 0 .1rem;'>Program Donasi</h4>
<p style='color:#6a7a60; font-size:.72rem; margin:0;'>Klik untuk berdonasi langsung</p>
</div>
""", unsafe_allow_html=True)
        campaigns = get_all_campaigns()
        for c in campaigns:
            pct = min(round(c["dana_terkumpul"] / c["target_dana"] * 100) if c["target_dana"] else 0, 100)
            st.markdown(f"""
<div style='background:rgba(12,20,12,.65); border:.5px solid rgba(255,255,255,.06); border-radius:12px; padding:.8rem 1rem; margin-bottom:.5rem; transition:all .3s;'>
<div style='font-size:.82rem; font-weight:600; color:#f0ede6; margin-bottom:.2rem;'>{c['judul'][:30]}</div>
<div style='font-size:.68rem; color:#6a7a60; margin-bottom:.4rem;'>📂 {c.get('kategori','')}</div>
<div style='background:rgba(255,255,255,.07); border-radius:4px; height:4px; overflow:hidden; margin-bottom:.3rem;'>
<div style='height:100%; border-radius:4px; background:linear-gradient(90deg,#c9a84c,#86efac); width:{pct}%;'></div>
</div>
<div style='display:flex; justify-content:space-between; font-size:.68rem;'>
<span style='color:#8a9e80;'>Terkumpul <strong style="color:#e2c97a">{format_rupiah(c["dana_terkumpul"])}</strong></span>
<span style='color:#c9a84c; font-weight:600;'>{pct}%</span>
</div>
</div>
""", unsafe_allow_html=True)

        if st.button("💛 Donasi Sekarang", type="primary", use_container_width=True, key="chat_donasi_btn"):
            st.switch_page("pages/donasi.py")

    with chat_col:
        st.markdown("""
<div class="chat-header-card">
    <div class="chat-avatar-ring">🤖</div>
    <div class="chat-header-info">
        <h3>CareBot</h3>
        <div class="status-line">
            <div class="status-dot"></div>
            <span class="status-text">Online — Siap membantu</span>
        </div>
        <p class="desc">Asisten cerdas yang bisa merekomendasikan program, menjawab pertanyaan, dan membantu Anda berdonasi</p>
    </div>
</div>
""", unsafe_allow_html=True)

        # ── Area Chat Scrollable (ChatGPT Style) ──
        chat_container = st.container(height=480, border=False)

        # Menampilkan riwayat pesan di dalam container
        with chat_container:
            for i, msg in enumerate(st.session_state.messages):
                avatar = "🤖" if msg["role"] == "assistant" else "👤"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])
                    if msg.get("show_donation_form"):
                        render_inline_donation_form(i)

        # Tangkap input (fixed di bagian bawah layar/kolom)
        user_input = st.chat_input("Tulis pesan Anda...")

        # Tangkap jika ada penekanan tombol quick reply
        if st.session_state.quick_prompt:
            user_input = st.session_state.quick_prompt
            st.session_state.quick_prompt = None

        if user_input:
            # 1. Tambahkan pesan user ke histori
            st.session_state.messages.append({"role": "user", "content": user_input})

            # 2. Render langsung di dalam container
            with chat_container:
                with st.chat_message("user", avatar="👤"):
                    st.markdown(user_input)

                # 3. Stream balasan AI
                with st.chat_message("assistant", avatar="🤖"):
                    try:
                        intent = classify_intent(user_input)
                        show_form = (intent == "ask_direct_donate")

                        # Kirim seluruh history untuk memory context
                        resp = generate_smart_response(user_input, st.session_state.messages)
                        st.write_stream(stream_text(resp, delay_min=0.005, delay_max=0.02))

                        if show_form:
                            render_inline_donation_form(len(st.session_state.messages))
                    except Exception as e:
                        resp = f"Maaf, terjadi kesalahan: {e}"
                        show_form = False
                        st.markdown(resp)

            # 4. Simpan balasan ke histori
            st.session_state.messages.append({
                "role": "assistant",
                "content": resp,
                "show_donation_form": show_form
            })
            try:
                save_chat(None, user_input, resp)
            except Exception:
                pass



        # ── Quick Replies ──
        st.markdown('<div class="qr-label">💡 Saran Topik</div>', unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns([1.4, 1.3, 1.3, 1.3, .7])

        if c1.button("📊 Dana terkumpul", use_container_width=True, key="qr1"):
            st.session_state.quick_prompt = "Berapa total dana yang sudah terkumpul?"
            st.rerun()
        if c2.button("💖 Donasi", use_container_width=True, key="qr2"):
            st.session_state.quick_prompt = "Saya mau donasi"
            st.rerun()
        if c3.button("🤝 Jadi relawan", use_container_width=True, key="qr3"):
            st.session_state.quick_prompt = "Bagaimana cara menjadi volunteer?"
            st.rerun()
        if c4.button("🌟 Dampak donasi", use_container_width=True, key="qr4"):
            st.session_state.quick_prompt = "Apa dampak donasi saya sebesar Rp 50.000?"
            st.rerun()
        with c5:
            if st.button("🗑️", use_container_width=True, key="qr_clear", help="Hapus semua percakapan"):
                st.session_state.messages = [{"role": "assistant", "content":
                        "Halo, Kak! 👋 Saya **CareBot**, asisten AI DonasiCare.\n\n"
                        "Setiap kebaikan kecil sangat berarti bagi mereka yang membutuhkan. "
                        "Kira-kira, program donasi seperti apa yang sedang Kakak cari hari ini? "
                        "Apakah Kakak tertarik pada program pendidikan, kesehatan, lingkungan, atau mungkin bantuan bencana alam?"}]
                st.rerun()




# ══════════════════════════════════════════════════════════════════════
# TAB 2 — REKOMENDASI
# ══════════════════════════════════════════════════════════════════════
def tab_recommendation():
    st.markdown("""
<div class="g-card">
<h3>Rekomendasi Berdasarkan Minat</h3>
<p class="sub">AI mencocokkan program donasi terbaik sesuai preferensi Anda.</p>
</div>""", unsafe_allow_html=True)

    minat = st.multiselect(
        "Area yang paling Anda pedulikan",
        options=["Pendidikan Anak","Kesehatan & Medis","Pelestarian Lingkungan","Pemberdayaan Ekonomi","Bantuan Bencana Alam"],
        default=["Pendidikan Anak"]
    )
    st.selectbox("Rentang donasi per bulan",
        options=["Kurang dari Rp 50.000","Rp 50.000 – Rp 200.000","Lebih dari Rp 200.000"], index=1)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("✨ Tampilkan Rekomendasi", type="primary", key="rec_btn"):
        if not minat:
            st.warning("Pilih minimal satu area minat.")
        else:
            with st.spinner("Menganalisis program terbaik…"):
                time.sleep(0.6)
                results = get_recommendations(minat)
                if results:
                    st.success(f"Ditemukan **{len(results)} program** yang cocok!")
                    for r in results:
                        pct = calc_progress(r["dana_terkumpul"], r["target_dana"])
                        st.markdown(f"""
<div class="rc">
<h4>{r['judul']}</h4>
<p>{r.get('deskripsi', '')}</p>
<p class="rmeta">📂 {r['kategori']} &nbsp;·&nbsp; 📍 {r.get('lokasi','—')}</p>
<p class="rdana">Terkumpul {format_rupiah(r['dana_terkumpul'])} dari {format_rupiah(r['target_dana'])} ({pct}%)</p>
<div class="pb"><div class="pf" style="width:{pct}%"></div></div>
</div>""", unsafe_allow_html=True)
                else:
                    st.info("Belum ada program yang cocok.")


# ══════════════════════════════════════════════════════════════════════
# TAB 3 — EDUKASI
# ══════════════════════════════════════════════════════════════════════
def tab_education():
    st.markdown("""
<div class="g-card">
<h3>Edukasi &amp; Dampak Sosial</h3>
<p class="sub">Wawasan berbasis data — bagaimana donasi kecil menciptakan dampak besar.</p>
</div>""", unsafe_allow_html=True)

    with st.expander("📚 Pendidikan Anak Pelosok"):
        st.markdown("Anak di daerah terpencil memiliki tingkat putus sekolah **3× lebih tinggi** dari rata-rata nasional. Donasi **Rp 150.000/bulan** dapat menutup kebutuhan nutrisi dan buku mereka. Pendidikan memutus rantai kemiskinan dengan efektivitas **68%** dalam satu generasi.")
        st.markdown('<div><div class="estat"><span class="en">3×</span><span class="el">Risiko putus sekolah</span></div><div class="estat"><span class="en">68%</span><span class="el">Efektivitas</span></div><div class="estat"><span class="en">150rb</span><span class="el">Biaya/anak/bulan</span></div></div>', unsafe_allow_html=True)

    with st.expander("🌿 Reboisasi Hutan Mangrove"):
        st.markdown("**1 hektar** mangrove menyerap karbon **4× lebih banyak** dari hutan tropis biasa. Program DonasiCare fokus di pesisir yang terancam abrasi. Sudah **14.200 bibit** tertanam tahun ini.")
        st.markdown('<div><div class="estat"><span class="en">4×</span><span class="el">Penyerapan karbon</span></div><div class="estat"><span class="en">14.200</span><span class="el">Bibit ditanam</span></div></div>', unsafe_allow_html=True)

    with st.expander("🛡️ Transparansi Dana"):
        st.markdown("Setiap aliran dana dianalisis sistem kami — **tanpa overhead tersembunyi**. Laporan otomatis dikirim tiap akhir bulan, rinci hingga ke tangan penerima manfaat.")
        st.markdown('<div><div class="estat"><span class="en">100%</span><span class="el">Dana tercatat</span></div><div class="estat"><span class="en">0%</span><span class="el">Overhead tersembunyi</span></div></div>', unsafe_allow_html=True)

    with st.expander("💼 Pemberdayaan Ekonomi Perempuan"):
        st.markdown("Program UMKM DonasiCare menjangkau **1.340 perempuan kepala keluarga** di 6 provinsi. Peserta rata-rata mengalami kenaikan pendapatan **2,3×** dalam 6 bulan pasca pelatihan.")
        st.markdown('<div><div class="estat"><span class="en">1.340</span><span class="el">Perempuan terdampak</span></div><div class="estat"><span class="en">2,3×</span><span class="el">Kenaikan pendapatan</span></div></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 4 — GENERATOR
# ══════════════════════════════════════════════════════════════════════
def tab_generator():
    st.markdown("""
<div class="g-card">
<h3>Generator Kampanye AI</h3>
<p class="sub">Buat deskripsi kampanye yang menggugah empati — dalam hitungan detik.</p>
</div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        judul  = st.text_input("Judul Kampanye", placeholder="Bantuan Air Bersih Gunung Kidul")
        target = st.text_input("Target Penerima", placeholder="50 KK di Desa X")
    with c2:
        kategori = st.selectbox("Kategori", ["Kesehatan","Lingkungan","Pendidikan","Kemanusiaan","Ekonomi"])
        dana = st.number_input("Target Dana (Rp)", min_value=1_000_000, max_value=1_000_000_000, value=5_000_000, step=500_000)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🪄 Generate Deskripsi", type="primary", key="gen_btn"):
        if not judul or not target:
            st.error("Lengkapi **judul** dan **target penerima** terlebih dahulu.")
        else:
            with st.spinner("Merangkai kata-kata yang menyentuh hati…"):
                time.sleep(1.0)
                hasil = (
                    f"{judul.upper()}\n\n"
                    f"Bayangkan jika setiap langkah kecil kita bisa mengubah hidup seseorang. "
                    f"Di sudut negeri ini, {target} tengah berjuang menghadapi tantangan "
                    f"{kategori.lower()} yang tak seharusnya mereka hadapi sendirian.\n\n"
                    f"Mereka tidak meminta kemewahan — hanya uluran tangan sederhana dari kita "
                    f"yang lebih beruntung. Setiap kontribusi, sekecil apapun, adalah nyala harapan.\n\n"
                    f"Dengan target {format_rupiah(dana)}, setiap rupiah Anda langsung menjadi solusi "
                    f"nyata yang terukur dan transparan — terpantau hingga ke tangan penerima manfaat.\n\n"
                    f"Mari bersama menjadi alasan mereka tersenyum hari ini. 🌿"
                )
            st.success("✅ Deskripsi berhasil dibuat!")
            st.text_area("Hasil Generate — salin dan gunakan:", value=hasil, height=255)
            st.markdown('<p style="font-size:.72rem;color:#5a6a50;margin-top:.4rem;">💡 Edit agar lebih personal sebelum dipublikasi.</p>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
def main():
    render_navbar("aichatbot")
    inject_css()

    st.markdown("""
<br><div class="pg-header">
<span class="eyebrow">DonasiCare · Powered by AI</span>
<h1>Asisten <em>Cerdas</em> Donasi</h1>
<p>Pendamping pintar untuk perjalanan donasi yang lebih bermakna</p>
</div>""", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs([
        "🤖 Chatbot Donasi",
        "✨ Rekomendasi Minat",
        "📖 Edukasi & Dampak",
        "🪄 Generator Kampanye",
    ])

    with t1: tab_chatbot()
    with t2: tab_recommendation()
    with t3: tab_education()
    with t4: tab_generator()


if __name__ == "__main__":
    main()
