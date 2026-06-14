import streamlit as st
import time
import datetime
import random
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from utils.campaign import get_all_campaigns, get_campaign_by_id
    from utils.helpers import format_rupiah, save_donation
    UTILS_OK = True
except ImportError:
    UTILS_OK = False

def format_rupiah(amount):
    return "Rp {:,}".format(int(amount)).replace(",", ".")

def get_all_campaigns():
    return [
        {"id":1,"judul":"Beasiswa Anak Pelosok Jawa Tengah","kategori":"Pendidikan","dana_terkumpul":8_200_000,"target_dana":10_000_000},
        {"id":2,"judul":"Klinik Desa Terpencil Kalimantan","kategori":"Kesehatan","dana_terkumpul":6_500_000,"target_dana":12_000_000},
        {"id":3,"judul":"Reboisasi Mangrove Pesisir Demak","kategori":"Lingkungan","dana_terkumpul":14_300_000,"target_dana":20_000_000},
        {"id":4,"judul":"UMKM Perempuan Desa NTT","kategori":"Ekonomi","dana_terkumpul":9_800_000,"target_dana":15_000_000},
        {"id":5,"judul":"Tanggap Bencana Banjir Sulawesi","kategori":"Bencana Alam","dana_terkumpul":22_000_000,"target_dana":25_000_000},
    ]

def save_donation(**kwargs):
    pass

# ══════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], * { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp {
background: linear-gradient(160deg, #111c11 0%, #0a140a 55%, #101a10 100%) !important;
}
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, .stDeployButton { display:none !important; visibility:hidden !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #2d4a2d; border-radius: 4px; }

/* ── Page wrapper ── */
.dn-page {
padding-top: 1rem;
padding-bottom: 5rem;
}

/* ── Page header ── */
.dn-header {
text-align: center;
margin-bottom: 2.75rem;
}
.dn-header-eyebrow {
font-size: .68rem; font-weight: 700; letter-spacing: .18em;
text-transform: uppercase; color: #c9a84c;
display: flex; align-items: center; justify-content: center; gap: .5rem;
margin-bottom: .65rem;
}
.dn-header-eyebrow::before, .dn-header-eyebrow::after {
content: ''; display: inline-block;
width: 28px; height: 1.5px; background: #c9a84c; opacity: .5;
}
.dn-header h1 {
font-family: 'DM Serif Display', serif !important;
font-size: 2.6rem !important; font-weight: 400 !important;
color: #f0ede6 !important; line-height: 1.15 !important;
margin: 0 0 .5rem !important;
}
.dn-header h1 em { font-style: italic; color: #e2c97a; }
.dn-header p { color: #6a7a60; font-size: .9rem; margin: 0; }

/* ── Step pills ── */
.dn-steps {
display: flex; align-items: center; justify-content: center;
gap: 0; margin-bottom: 2.5rem;
}
.dn-step {
display: flex; align-items: center; gap: .55rem;
padding: .5rem 1.1rem;
border-radius: 999px;
font-size: .75rem; font-weight: 600;
color: #4a5a40;
transition: all .2s;
}
.dn-step.active {
background: rgba(201,168,76,.12);
border: .5px solid rgba(201,168,76,.3);
color: #e2c97a;
}
.dn-step-num {
width: 22px; height: 22px; border-radius: 50%;
background: rgba(255,255,255,.06);
display: flex; align-items: center; justify-content: center;
font-size: .68rem; font-weight: 700; color: #4a5a40;
flex-shrink: 0;
}
.dn-step.active .dn-step-num {
background: #c9a84c; color: #0f1a0f;
}
.dn-step-line {
width: 40px; height: 1px;
background: rgba(255,255,255,.08);
}

/* ── Section block ── */
.dn-block {
background: rgba(12,20,12,.65);
border: .5px solid rgba(201,168,76,.12);
border-radius: 18px;
padding: 1.75rem 2rem;
margin-bottom: 1.1rem;
transition: border-color .2s;
}
.dn-block:hover { border-color: rgba(201,168,76,.22); }

.dn-block-header {
display: flex; align-items: center; gap: .75rem;
margin-bottom: 1.35rem;
}
.dn-block-icon {
width: 36px; height: 36px; border-radius: 10px;
background: rgba(201,168,76,.1);
border: .5px solid rgba(201,168,76,.25);
display: flex; align-items: center; justify-content: center;
font-size: 1rem; flex-shrink: 0;
}
.dn-block-title {
font-family: 'DM Serif Display', serif !important;
font-size: 1.1rem !important; font-weight: 400 !important;
color: #f0ede6 !important; margin: 0 !important;
}
.dn-block-sub { color: #4a5a40; font-size: .72rem; margin: 2px 0 0; }

/* ── Campaign card grid (program selector) ── */
.dn-prog-grid {
display: grid;
grid-template-columns: 1fr 1fr;
gap: .75rem;
}
.dn-prog-card {
background: rgba(8,14,8,.7);
border: .5px solid rgba(255,255,255,.06);
border-radius: 12px;
padding: .85rem 1rem;
cursor: pointer;
transition: all .2s;
position: relative;
}
.dn-prog-card.selected {
border-color: rgba(201,168,76,.5);
background: rgba(201,168,76,.07);
}
.dn-prog-card:hover { border-color: rgba(201,168,76,.3); }
.dn-prog-badge {
display: inline-block; font-size: .62rem; font-weight: 700;
letter-spacing: .05em; text-transform: uppercase;
padding: .15rem .55rem; border-radius: 20px; margin-bottom: .4rem;
}
.badge-p { background: rgba(96,165,250,.15); color: #60a5fa; border: .5px solid rgba(96,165,250,.2); }
.badge-k { background: rgba(52,211,153,.15); color: #34d399; border: .5px solid rgba(52,211,153,.2); }
.badge-l { background: rgba(74,222,128,.15); color: #4ade80; border: .5px solid rgba(74,222,128,.2); }
.badge-b { background: rgba(251,146,60,.15);  color: #fb923c; border: .5px solid rgba(251,146,60,.2); }
.badge-e { background: rgba(167,139,250,.15); color: #a78bfa; border: .5px solid rgba(167,139,250,.2); }
.dn-prog-name {
font-size: .8rem; font-weight: 600; color: #d4c9b0;
line-height: 1.4; margin-bottom: .45rem;
}
.dn-prog-bar-bg {
background: rgba(255,255,255,.07); border-radius: 4px;
height: 3px; overflow: hidden; margin-bottom: .3rem;
}
.dn-prog-bar-fill {
height: 100%; border-radius: 4px;
background: linear-gradient(90deg, #c9a84c, #86efac);
}
.dn-prog-meta { font-size: .67rem; color: #4a5a40; }
.dn-prog-meta strong { color: #c9a84c; }
.dn-prog-check {
position: absolute; top: .65rem; right: .75rem;
width: 18px; height: 18px; border-radius: 50%;
background: #c9a84c;
display: flex; align-items: center; justify-content: center;
font-size: .6rem; color: #0f1a0f; font-weight: 900;
}

/* ── Nominal pills ── */
.dn-nom-grid {
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: .65rem;
margin-bottom: 1.1rem;
}
.dn-nom-pill {
background: rgba(8,14,8,.7);
border: .5px solid rgba(255,255,255,.08);
border-radius: 10px;
padding: .65rem;
text-align: center;
cursor: pointer;
transition: all .2s;
}
.dn-nom-pill.sel {
border-color: rgba(201,168,76,.5);
background: rgba(201,168,76,.08);
}
.dn-nom-pill:hover { border-color: rgba(201,168,76,.3); }
.dn-nom-pill .nv {
font-family: 'DM Serif Display',serif !important;
font-size: .95rem !important; color: #e2c97a !important; font-weight: 400 !important;
}
.dn-nom-pill .nl { font-size: .65rem; color: #4a5a40; margin-top: 2px; }

/* ── Divider ── */
.dn-div {
border: none; border-top: .5px solid rgba(255,255,255,.06);
margin: .1rem 0;
}

/* ── Form elements override ── */
label, .stSelectbox label, .stMultiSelect label,
.stTextInput label, .stNumberInput label,
.stTextArea label, .stCheckbox label {
color: #8a9e80 !important; font-size: .72rem !important;
font-weight: 600 !important; letter-spacing: .06em !important;
text-transform: uppercase !important;
}
.stTextInput input, .stNumberInput input {
background: rgba(5,10,5,.85) !important;
border: .5px solid rgba(201,168,76,.18) !important;
border-radius: 10px !important; color: #d4c9b0 !important;
font-size: .85rem !important;
padding: .6rem .9rem !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
border-color: rgba(201,168,76,.45) !important;
box-shadow: 0 0 0 3px rgba(201,168,76,.06) !important;
}
.stTextInput input::placeholder { color: #2e3e2e !important; }

[data-baseweb="select"] > div:first-child {
background: rgba(5,10,5,.85) !important;
border: .5px solid rgba(201,168,76,.18) !important;
border-radius: 10px !important;
}
[data-baseweb="select"] span { color: #d4c9b0 !important; font-size: .85rem !important; }
[data-baseweb="select"] svg { fill: #c9a84c !important; }
[data-baseweb="popover"] ul {
background: #0d1a0d !important;
border: .5px solid rgba(201,168,76,.18) !important;
border-radius: 10px !important;
}
[data-baseweb="popover"] li { color: #c8ddc0 !important; font-size: .82rem !important; }
[data-baseweb="popover"] li:hover { background: rgba(201,168,76,.1) !important; }

/* checkbox */
[data-testid="stCheckbox"] label {
color: #8a9e80 !important; font-size: .8rem !important;
text-transform: none !important; letter-spacing: 0 !important;
}
[data-testid="stCheckbox"] [data-baseweb="checkbox"] span {
background: rgba(5,10,5,.85) !important;
border-color: rgba(201,168,76,.3) !important;
}

/* file uploader */
[data-testid="stFileUploader"] {
background: rgba(5,10,5,.6) !important;
border: .5px dashed rgba(201,168,76,.25) !important;
border-radius: 12px !important;
}
[data-testid="stFileUploader"] p { color: #6a7a60 !important; font-size: .78rem !important; }

/* alert */
[data-testid="stAlert"] {
border-radius: 10px !important;
border: .5px solid rgba(201,168,76,.2) !important;
border-left: 2px solid rgba(201,168,76,.5) !important;
background: rgba(47,74,47,.25) !important;
}
[data-testid="stAlert"] p { color: #c8ddc0 !important; font-size: .8rem !important; }

/* spinner */
[data-testid="stSpinner"] p { color: #9aaa8a !important; }

/* number input arrows */
.stNumberInput [data-baseweb="input"] {
background: rgba(5,10,5,.85) !important;
border: .5px solid rgba(201,168,76,.18) !important;
border-radius: 10px !important;
}
.stNumberInput input { border: none !important; }

/* ── CTA button ── */
[data-testid="baseButton-primary"] {
background: linear-gradient(135deg,#c9a84c,#a8852c) !important;
color: #0f1a0f !important; font-weight: 700 !important;
border: none !important; border-radius: 12px !important;
padding: .75rem 2rem !important; font-size: .9rem !important;
box-shadow: 0 6px 22px rgba(201,168,76,.28) !important;
transition: all .2s !important;
}
[data-testid="baseButton-primary"]:hover {
opacity: .9 !important; transform: translateY(-2px) !important;
box-shadow: 0 10px 32px rgba(201,168,76,.42) !important;
}
.stButton > button {
border-radius: 10px !important;
border: .5px solid rgba(201,168,76,.3) !important;
color: #e2c97a !important; background: transparent !important;
font-weight: 600 !important; font-size: .78rem !important;
padding: .5rem 1rem !important; transition: all .18s !important;
}
.stButton > button:hover {
background: rgba(201,168,76,.1) !important;
border-color: rgba(201,168,76,.55) !important;
transform: translateY(-1px) !important;
}

/* ── Receipt ── */
.dn-receipt {
max-width: 480px; margin: 2rem auto;
background: rgba(12,20,12,.9);
border: .5px solid rgba(201,168,76,.3);
border-top: 3px solid #c9a84c;
border-radius: 18px;
overflow: hidden;
box-shadow: 0 24px 64px rgba(0,0,0,.5);
}
.dn-receipt-head {
text-align: center;
padding: 1.75rem 2rem 1.25rem;
border-bottom: .5px dashed rgba(201,168,76,.2);
}
.dn-receipt-head .ricon {
font-size: 2.2rem; margin-bottom: .6rem; display: block;
}
.dn-receipt-head h2 {
font-family: 'DM Serif Display', serif !important;
font-size: 1.35rem !important; font-weight: 400 !important;
color: #f0ede6 !important; margin: 0 0 .25rem !important;
}
.dn-receipt-head p {
color: #4a5a40; font-size: .75rem; margin: 0;
}
.dn-receipt-body { padding: 1.25rem 2rem; }
.dn-receipt-row {
display: flex; justify-content: space-between; align-items: flex-start;
padding: .6rem 0;
border-bottom: .5px solid rgba(255,255,255,.04);
}
.dn-receipt-row:last-child { border-bottom: none; }
.dn-receipt-label { color: #4a5a40; font-size: .75rem; font-weight: 500; }
.dn-receipt-value { color: #c8ddc0; font-size: .8rem; font-weight: 600; text-align: right; max-width: 58%; }
.dn-receipt-total {
display: flex; justify-content: space-between; align-items: center;
padding: 1.25rem 2rem;
background: rgba(201,168,76,.06);
border-top: .5px dashed rgba(201,168,76,.25);
}
.dn-receipt-total .tl {
font-size: .72rem; font-weight: 700; letter-spacing: .1em;
text-transform: uppercase; color: #6a7a60;
}
.dn-receipt-total .tv {
font-family: 'DM Serif Display', serif !important;
font-size: 1.5rem !important; font-weight: 400 !important;
color: #e2c97a !important;
}
.dn-receipt-status {
text-align: center; padding: .85rem 2rem;
background: rgba(74,222,128,.06);
border-top: .5px solid rgba(74,222,128,.15);
}
.dn-receipt-status span {
font-size: .78rem; font-weight: 600; color: #4ade80;
}

/* ── Summary bar (before submit) ── */
.dn-summary {
background: rgba(201,168,76,.06);
border: .5px solid rgba(201,168,76,.2);
border-radius: 14px;
padding: 1.1rem 1.5rem;
display: flex; align-items: center; justify-content: space-between;
margin-bottom: 1.1rem;
gap: 1rem;
}
.dn-summary-item { text-align: center; }
.dn-summary-item .si-label { font-size: .65rem; color: #4a5a40; font-weight: 600;
letter-spacing: .06em; text-transform: uppercase; margin-bottom: 3px; }
.dn-summary-item .si-val {
font-family: 'DM Serif Display', serif !important;
font-size: .92rem !important; color: #e2c97a !important; font-weight: 400 !important;
}
.dn-summary-div { width: 1px; height: 36px; background: rgba(255,255,255,.07); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# SESSION INIT
# ══════════════════════════════════════════════════════════════════════
def init_session():
    defaults = {
        "donation_success": False,
        "last_receipt": None,
        "nominal": 50000,
        "selected_prog_idx": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════
# RECEIPT
# ══════════════════════════════════════════════════════════════════════
def render_receipt():
    r = st.session_state.last_receipt
    if not r:
        return

    st.markdown(f"""
<div class="dn-receipt">
<div class="dn-receipt-head">
<span class="ricon">🎉</span>
<h2>Donasi Berhasil!</h2>
<p>DonasiCare · Terpercaya & Transparan · {r['date']}</p>
</div>
<div class="dn-receipt-body">
<div class="dn-receipt-row">
<span class="dn-receipt-label">ID Transaksi</span>
<span class="dn-receipt-value" style="color:#c9a84c;font-family:'DM Serif Display',serif;font-size:.88rem;">{r['tx_id']}</span>
</div>
<div class="dn-receipt-row">
<span class="dn-receipt-label">Nama Donatur</span>
<span class="dn-receipt-value">{r['name']}</span>
</div>
<div class="dn-receipt-row">
<span class="dn-receipt-label">Program</span>
<span class="dn-receipt-value">{r['program']}</span>
</div>
<div class="dn-receipt-row">
<span class="dn-receipt-label">Metode Pembayaran</span>
<span class="dn-receipt-value">{r['method']}</span>
</div>
</div>
<div class="dn-receipt-total">
<span class="tl">Total Donasi</span>
<span class="tv">{format_rupiah(r['amount'])}</span>
</div>
<div class="dn-receipt-status">
<span>✅ &nbsp;Berhasil · Terverifikasi</span>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("📋 Lihat Riwayat Donasi", use_container_width=True, type="primary"):
            st.session_state.donation_success = False
            try: st.switch_page("pages/riwayatdonasi.py")
            except: st.rerun()
        st.markdown("<br style='margin:.3rem'>", unsafe_allow_html=True)
        if st.button("💚 Donasi Lagi", use_container_width=True):
            st.session_state.donation_success = False
            st.rerun()


# ══════════════════════════════════════════════════════════════════════
# FORM
# ══════════════════════════════════════════════════════════════════════
CAT_BADGE = {
    "Pendidikan": "badge-p", "Kesehatan": "badge-k",
    "Lingkungan": "badge-l", "Bencana Alam": "badge-b", "Ekonomi": "badge-e",
}
CAT_EMOJI = {
    "Pendidikan":"🎓","Kesehatan":"🏥","Lingkungan":"🌿","Bencana Alam":"🆘","Ekonomi":"💼"
}

def render_form():
    campaigns = get_all_campaigns()
    if not campaigns:
        st.warning("Belum ada program kampanye yang tersedia.")
        return

    program_names  = [c["judul"] for c in campaigns]
    campaign_map   = {c["judul"]: c for c in campaigns}

    # Pre-select dari halaman lain
    default_idx = 0
    if "selected_campaign_id" in st.session_state:
        cid = st.session_state.selected_campaign_id
        for i, c in enumerate(campaigns):
            if c["id"] == cid:
                default_idx = i
                break

    if "selected_prog_idx" not in st.session_state:
        st.session_state.selected_prog_idx = default_idx

    # ── BLOK 1: Pilih Program ──────────────────────────────────────
    st.markdown("""
<div class="dn-block">
<div class="dn-block-header">
<div class="dn-block-icon">🏷️</div>
<div>
<div class="dn-block-title">Pilih Program Bantuan</div>
<div class="dn-block-sub">Pilih salah satu program yang ingin Anda dukung</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Inject CSS for transparent button overlay
    st.markdown('''
<style>
div[data-testid="column"]:has(.dn-prog-card) { position: relative; }
div[data-testid="column"]:has(.dn-prog-card) > div:has(.stButton) {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0; z-index: 99;
}
div[data-testid="column"]:has(.dn-prog-card) .stButton,
div[data-testid="column"]:has(.dn-prog-card) .stButton button {
    width: 100%; height: 100%; cursor: pointer; display: block;
}
</style>
''', unsafe_allow_html=True)

    sel_idx = st.session_state.selected_prog_idx
    
    # We use st.columns instead of CSS grid to pair HTML and buttons
    cols = st.columns(2)
    for i, c in enumerate(campaigns):
        cat   = c.get("kategori", "")
        badge = CAT_BADGE.get(cat, "badge-e")
        emoji = CAT_EMOJI.get(cat, "📦")
        pct   = min(round(c["dana_terkumpul"]/c["target_dana"]*100) if c["target_dana"] else 0, 100)
        sel_cls = "selected" if i == sel_idx else ""
        check   = '<div class="dn-prog-check">✓</div>' if i == sel_idx else ""
        terkumpul = format_rupiah(c["dana_terkumpul"])
        target    = format_rupiah(c["target_dana"])
        
        with cols[i % 2]:
            st.markdown(f'''
<div class="dn-prog-card {sel_cls}">
{check}
<span class="dn-prog-badge {badge}">{emoji} {cat}</span>
<div class="dn-prog-name">{c['judul']}</div>
<div class="dn-prog-bar-bg">
<div class="dn-prog-bar-fill" style="width:{pct}%"></div>
</div>
<div class="dn-prog-meta">
Terkumpul <strong>{terkumpul}</strong> / {target} · {pct}%
</div>
</div>
            ''', unsafe_allow_html=True)
            if st.button("Pilih", key=f"prog_{i}", use_container_width=True):
                st.session_state.selected_prog_idx = i
                st.rerun()

    # ── BLOK 2: Nominal ───────────────────────────────────────────
    st.markdown("""
<div class="dn-block" style="margin-top:1rem;">
<div class="dn-block-header">
<div class="dn-block-icon">💰</div>
<div>
<div class="dn-block-title">Nominal Donasi</div>
<div class="dn-block-sub">Pilih nominal atau masukkan jumlah lain</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    PRESETS = [
        (50_000,  "50 Ribu"),
        (100_000, "100 Ribu"),
        (250_000, "250 Ribu"),
        (500_000, "500 Ribu"),
    ]
    cur_nom = st.session_state.nominal

    st.markdown('''
<style>
div[data-testid="column"]:has(.dn-nom-pill) { position: relative; }
div[data-testid="column"]:has(.dn-nom-pill) > div:has(.stButton) {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0; z-index: 99;
}
div[data-testid="column"]:has(.dn-nom-pill) .stButton,
div[data-testid="column"]:has(.dn-nom-pill) .stButton button {
    width: 100%; height: 100%; cursor: pointer; display: block;
}
</style>
''', unsafe_allow_html=True)

    nom_cols = st.columns(4)
    for i, (val, lbl) in enumerate(PRESETS):
        sel = "sel" if cur_nom == val else ""
        with nom_cols[i]:
            st.markdown(f'''
<div class="dn-nom-pill {sel}">
<div class="nv">Rp {lbl}</div>
<div class="nl">{"✓ terpilih" if sel else "pilih"}</div>
</div>''', unsafe_allow_html=True)
            if st.button("Pilih", key=f"nom_{i}", use_container_width=True):
                st.session_state.nominal = val
                st.rerun()

    st.markdown("<br style='margin:.2rem'>", unsafe_allow_html=True)
    custom_nominal = st.number_input(
        "Atau masukkan nominal lain (Rp)",
        min_value=10_000, step=10_000,
        value=st.session_state.nominal,
        key="nom_input"
    )

    # ── BLOK 3: Detail Pembayaran ──────────────────────────────────
    st.markdown("""
<div class="dn-block" style="margin-top:1rem;">
<div class="dn-block-header">
<div class="dn-block-icon">🪪</div>
<div>
<div class="dn-block-title">Detail Pembayaran</div>
<div class="dn-block-sub">Isi data diri dan pilih metode pembayaran</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    donor_name = st.text_input("Nama Lengkap", placeholder="Masukkan nama lengkap Anda")
    is_anon    = st.checkbox("Sembunyikan nama saya (Donasi sebagai Hamba Allah / Anonim)")

    METODE = ["BCA Virtual Account","Mandiri Virtual Account","GoPay","OVO","DANA","QRIS","Transfer Bank Manual"]
    payment_method = st.selectbox("Metode Pembayaran", METODE)

    uploaded_file  = None
    bukti_filename = ""
    if payment_method == "Transfer Bank Manual":
        st.markdown("<br style='margin:.2rem'>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Bukti Transfer (JPG, PNG, PDF)",
            type=["jpg","png","pdf"]
        )
        if uploaded_file:
            bukti_filename = uploaded_file.name
            st.success(f"✅ Bukti transfer **{bukti_filename}** berhasil diunggah.")

    # ── Summary bar ───────────────────────────────────────────────
    selected_program = program_names[st.session_state.selected_prog_idx]
    prog_short = selected_program[:38] + "…" if len(selected_program) > 38 else selected_program
    metode_short = payment_method.replace(" Virtual Account","") \
                                 .replace(" Bank Manual","")
    st.markdown(f"""
<div class="dn-summary">
<div class="dn-summary-item">
<div class="si-label">Program</div>
<div class="si-val" style="font-size:.78rem !important;">{prog_short}</div>
</div>
<div class="dn-summary-div"></div>
<div class="dn-summary-item">
<div class="si-label">Nominal</div>
<div class="si-val">{format_rupiah(custom_nominal)}</div>
</div>
<div class="dn-summary-div"></div>
<div class="dn-summary-item">
<div class="si-label">Via</div>
<div class="si-val" style="font-size:.82rem !important;">{metode_short}</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ── Submit ────────────────────────────────────────────────────
    if st.button("💛 Mulai Donasi Sekarang", type="primary", use_container_width=True):
        if not is_anon and not donor_name.strip():
            st.error("Silakan masukkan nama Anda atau centang opsi Anonim.")
        elif payment_method == "Transfer Bank Manual" and not uploaded_file:
            st.error("Silakan upload bukti transfer terlebih dahulu.")
        else:
            with st.spinner("Memproses donasi Anda…"):
                time.sleep(1.8)

                final_name = "Hamba Allah (Anonim)" if is_anon else donor_name.strip()
                tx_id  = f"TRX-{random.randint(100000,999999)}"
                dt_now = datetime.datetime.now().strftime("%d %b %Y, %H:%M WIB")

                selected_campaign = campaign_map[selected_program]
                try:
                    save_donation(
                        user_id=None,
                        campaign_id=selected_campaign["id"],
                        nominal=custom_nominal,
                        metode=payment_method,
                        anonim=is_anon,
                        bukti=bukti_filename,
                        pesan=f"Donasi oleh {final_name}"
                    )
                except Exception:
                    pass

                receipt = {
                    "tx_id": tx_id, "name": final_name,
                    "program": selected_program,
                    "amount": custom_nominal,
                    "method": payment_method, "date": dt_now
                }

                if "riwayat_donasi" not in st.session_state:
                    st.session_state.riwayat_donasi = []
                st.session_state.riwayat_donasi.append(receipt)
                st.session_state.last_receipt     = receipt
                st.session_state.donation_success = True

                if "selected_campaign_id" in st.session_state:
                    del st.session_state["selected_campaign_id"]

                st.rerun()


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
def main():
    inject_css()
    init_session()

    st.markdown('<div class="dn-page">', unsafe_allow_html=True)

    # Step indicator
    step = 2 if st.session_state.donation_success else 1
    steps_html = f"""
<div class="dn-steps">
<div class="dn-step {"active" if step == 1 else ""}">
<span class="dn-step-num">1</span> Isi Form
</div>
<div class="dn-step-line"></div>
<div class="dn-step {"active" if step == 2 else ""}">
<span class="dn-step-num">2</span> Konfirmasi
</div>
</div>"""

    # Header
    st.markdown(f"""
<div class="dn-header">
<div class="dn-header-eyebrow">DonasiCare · Berikan Harapan</div>
<h1>{"Terima Kasih atas <em>Kebaikan</em> Anda" if step == 2 else "Mulai <em>Berdonasi</em>"}</h1>
<p>{"Donasi Anda telah berhasil diproses dan tersimpan." if step == 2 else "Setiap kebaikan Anda adalah harapan nyata bagi mereka yang membutuhkan."}</p>
</div>
{steps_html}
""", unsafe_allow_html=True)

    if st.session_state.donation_success:
        st.balloons()
        render_receipt()
    else:
        render_form()

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()