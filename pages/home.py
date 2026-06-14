import streamlit as st
import base64
import os
import sys
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from utils.campaign import get_all_campaigns, get_total_donasi, get_campaign_count
    from utils.helpers import format_rupiah, calc_progress, get_image_for_category, get_donation_count
    UTILS_OK = True
except ImportError:
    UTILS_OK = False

# ── Fallbacks ──────────────────────────────────────────────────────────
def format_rupiah(amount):
    return "Rp {:,}".format(int(amount)).replace(",", ".")
def calc_progress(a, b):
    return round((a / b) * 100) if b else 0
def get_total_donasi():    return 4_870_000_000
def get_donation_count():  return 14_872
def get_campaign_count():  return 8
def get_all_campaigns():
    return [
        {"judul":"Beasiswa Anak Pelosok Jawa Tengah","deskripsi":"Mendukung 120 anak putus sekolah dengan kebutuhan nutrisi dan alat tulis.","kategori":"Pendidikan","dana_terkumpul":8_200_000,"target_dana":10_000_000},
        {"judul":"Klinik Desa Terpencil Kalimantan","deskripsi":"Layanan kesehatan dasar untuk 5 desa terpencil di Kalimantan Tengah.","kategori":"Kesehatan","dana_terkumpul":6_500_000,"target_dana":12_000_000},
        {"judul":"Reboisasi Mangrove Pesisir Demak","deskripsi":"Penanaman 20.000 bibit mangrove untuk mencegah abrasi pesisir.","kategori":"Lingkungan","dana_terkumpul":14_300_000,"target_dana":20_000_000},
    ]
def get_image_for_category(cat): return None

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets") if not UTILS_OK else os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = Path(path).suffix.lstrip(".")
        if ext == "jpg": ext = "jpeg"
        return f"data:image/{ext};base64,{data}"
    except:
        return None


# ══════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DonasiCare — Berikan Harapan",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ══════════════════════════════════════════════════════════════════════
# CSS — Forest Luxury · DM Serif + Plus Jakarta Sans
# ══════════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], * {
font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── App background ── */
.stApp {
background: linear-gradient(160deg, #111c11 0%, #0a140a 55%, #101a10 100%) !important;
min-height: 100vh;
}
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, .stDeployButton { display: none !important; visibility: hidden !important; }

/* ── Container ── */

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #2d4a2d; border-radius: 4px; }

/* ════════════════════════════════════════
NAVBAR
════════════════════════════════════════ */
.dc-nav {
background: rgba(8, 14, 8, 0.92);
backdrop-filter: blur(24px);
-webkit-backdrop-filter: blur(24px);
border-bottom: 1px solid rgba(201,168,76,.14);
padding: 0 1rem;
height: 64px;
display: flex;
align-items: center;
justify-content: space-between;
position: sticky;
top: 0;
z-index: 9999;
}
.dc-nav-brand {
display: flex;
align-items: center;
gap: .65rem;
text-decoration: none;
}
.dc-nav-logo {
width: 38px; height: 38px;
background: linear-gradient(135deg, #c9a84c, #e2c97a);
border-radius: 10px;
display: flex; align-items: center; justify-content: center;
font-size: 1.1rem;
box-shadow: 0 4px 16px rgba(201,168,76,.28);
flex-shrink: 0;
}
.dc-nav-name {
font-family: 'DM Serif Display', serif !important;
font-size: 1.3rem;
font-weight: 400;
color: #e2c97a;
letter-spacing: -.2px;
}
.dc-nav-links {
display: flex;
align-items: center;
gap: .15rem;
}
.dc-nav-links a {
color: #8a9e80;
text-decoration: none;
padding: .42rem .85rem;
border-radius: 8px;
font-size: .8rem;
font-weight: 500;
transition: all .2s;
white-space: nowrap;
}
.dc-nav-links a:hover  { color: #e2c97a; background: rgba(201,168,76,.1); }
.dc-nav-links a.active { color: #e2c97a; background: rgba(201,168,76,.12);
border: .5px solid rgba(201,168,76,.25); }
.dc-nav-cta {
background: linear-gradient(135deg,#c9a84c,#a8852c) !important;
color: #0f1a0f !important;
font-weight: 700 !important;
border-radius: 9px !important;
padding: .42rem 1.1rem !important;
}
.dc-nav-cta:hover { opacity: .88; }

/* ════════════════════════════════════════
PAGE WRAPPER — consistent side padding
════════════════════════════════════════ */
.dc-page {
padding: 0 0 3rem;
max-width: 1280px;
margin: 0 auto;
}

/* ════════════════════════════════════════
HERO
════════════════════════════════════════ */
.dc-hero {
position: relative;
border-radius: 20px;
overflow: hidden;
margin: 2rem 0 0;
box-shadow: 0 24px 80px rgba(0,0,0,.55);
min-height: 420px;
background: linear-gradient(135deg, #1a2e1a, #0f1f0f);
}
.dc-hero-img {
width: 100%; height: 420px;
object-fit: cover; display: block;
opacity: .65;
}
.dc-hero-overlay {
position: absolute;
inset: 0;
background: linear-gradient(105deg,
rgba(8,14,8,.96) 0%,
rgba(8,14,8,.75) 45%,
rgba(8,14,8,.15) 100%);
display: flex;
flex-direction: column;
justify-content: center;
padding: 3rem 3.5rem;
}
.dc-hero-eyebrow {
font-size: .7rem; font-weight: 700; letter-spacing: .18em;
text-transform: uppercase; color: #c9a84c;
margin-bottom: .7rem;
display: flex; align-items: center; gap: .5rem;
}
.dc-hero-eyebrow::before {
content: ''; display: inline-block;
width: 24px; height: 1.5px; background: #c9a84c;
}
.dc-hero h1 {
font-family: 'DM Serif Display', serif !important;
font-size: 3.1rem !important;
font-weight: 400 !important;
color: #f0ede6 !important;
line-height: 1.12 !important;
margin: 0 0 .8rem !important;
max-width: 520px;
}
.dc-hero h1 em { font-style: italic; color: #e2c97a; }
.dc-hero-desc {
color: #9aaa8a;
font-size: .95rem;
line-height: 1.75;
max-width: 440px;
margin-bottom: 1.75rem;
}
.dc-hero-cta {
display: inline-flex; align-items: center; gap: .5rem;
background: linear-gradient(135deg, #c9a84c, #a8852c);
color: #0f1a0f !important;
padding: .8rem 2rem;
border-radius: 12px;
font-weight: 700; font-size: .9rem;
text-decoration: none;
box-shadow: 0 8px 28px rgba(201,168,76,.35);
transition: all .22s;
width: fit-content;
}
.dc-hero-cta:hover { transform: translateY(-2px); box-shadow: 0 14px 40px rgba(201,168,76,.5); }

/* Carousel dots */
.dc-dots {
display: flex; gap: 7px;
margin-top: 1.5rem;
}
.dc-dot {
height: 6px; border-radius: 3px;
background: rgba(255,255,255,.2);
transition: all .3s;
width: 22px;
}
.dc-dot.on { background: #c9a84c; width: 32px; }

/* ════════════════════════════════════════
SECTION HEADER
════════════════════════════════════════ */
.dc-sec {
margin: 3.5rem 0 1.5rem;
display: flex;
align-items: flex-end;
justify-content: space-between;
gap: 1rem;
}
.dc-sec-left {}
.dc-sec-eyebrow {
font-size: .68rem; font-weight: 700; letter-spacing: .14em;
text-transform: uppercase; color: #c9a84c;
margin-bottom: .3rem;
}
.dc-sec-title {
font-family: 'DM Serif Display', serif !important;
font-size: 1.75rem !important; font-weight: 400 !important;
color: #f0ede6 !important; margin: 0 !important;
line-height: 1.2 !important;
}
.dc-sec-title em { font-style: italic; color: #e2c97a; }
.dc-sec-sub {
color: #6a7a60; font-size: .8rem; margin: .3rem 0 0;
}
.dc-sec-link {
color: #c9a84c; font-size: .78rem; font-weight: 600;
text-decoration: none; white-space: nowrap;
display: flex; align-items: center; gap: .3rem;
transition: gap .2s;
}
.dc-sec-link:hover { gap: .55rem; }

/* ════════════════════════════════════════
STAT CARDS
════════════════════════════════════════ */
.dc-stats {
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: 1rem;
margin-bottom: .5rem;
}
.dc-stat {
background: rgba(15,25,15,.7);
border: .5px solid rgba(201,168,76,.15);
border-radius: 16px;
padding: 1.4rem 1.5rem;
transition: all .3s;
position: relative;
overflow: hidden;
}
.dc-stat::before {
content: '';
position: absolute;
top: 0; left: 0; right: 0;
height: 2px;
background: linear-gradient(90deg, #c9a84c, transparent);
opacity: 0;
transition: opacity .3s;
}
.dc-stat:hover { transform: translateY(-4px); border-color: rgba(201,168,76,.32);
box-shadow: 0 12px 36px rgba(0,0,0,.3); }
.dc-stat:hover::before { opacity: 1; }
.dc-stat-icon { font-size: 1.4rem; margin-bottom: .55rem; display: block; }
.dc-stat-num {
font-family: 'DM Serif Display', serif !important;
font-size: 1.65rem !important; font-weight: 400 !important;
color: #e2c97a !important;
line-height: 1.1; margin-bottom: .2rem;
}
.dc-stat-label { color: #6a7a60; font-size: .75rem; font-weight: 500; }

/* ════════════════════════════════════════
PROGRAM CARDS
════════════════════════════════════════ */
.dc-programs {
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 1.25rem;
}
.dc-prog {
background: rgba(12,20,12,.65);
border: .5px solid rgba(255,255,255,.06);
border-radius: 18px;
overflow: hidden;
transition: all .35s cubic-bezier(.4,0,.2,1);
}
.dc-prog:hover {
transform: translateY(-6px);
border-color: rgba(201,168,76,.22);
box-shadow: 0 20px 56px rgba(0,0,0,.4);
}
.dc-prog-img {
width: 100%; height: 186px; object-fit: cover; display: block;
}
.dc-prog-img-placeholder {
width: 100%; height: 186px;
display: flex; align-items: center; justify-content: center;
font-size: 3.5rem;
}
.dc-prog-body { padding: 1.2rem 1.35rem 1.4rem; }
.dc-prog-badge {
display: inline-block;
padding: .2rem .7rem;
border-radius: 20px;
font-size: .66rem; font-weight: 700;
letter-spacing: .06em; text-transform: uppercase;
margin-bottom: .55rem;
}
.badge-pendidikan { background: rgba(96,165,250,.15); color: #60a5fa; border: .5px solid rgba(96,165,250,.25); }
.badge-kesehatan  { background: rgba(52,211,153,.15); color: #34d399; border: .5px solid rgba(52,211,153,.25); }
.badge-lingkungan { background: rgba(74,222,128,.15); color: #4ade80; border: .5px solid rgba(74,222,128,.25); }
.badge-bencana    { background: rgba(251,146,60,.15);  color: #fb923c; border: .5px solid rgba(251,146,60,.25); }
.badge-ekonomi    { background: rgba(167,139,250,.15); color: #a78bfa; border: .5px solid rgba(167,139,250,.25); }

.dc-prog-title {
color: #e8e4da;
font-size: .92rem; font-weight: 700;
line-height: 1.4;
margin: 0 0 .4rem;
}
.dc-prog-desc {
color: #6a7a60;
font-size: .78rem; line-height: 1.65;
margin: 0 0 1rem;
}
.dc-prog-bar-bg {
background: rgba(255,255,255,.07);
border-radius: 6px; height: 5px; overflow: hidden; margin-bottom: .45rem;
}
.dc-prog-bar-fill {
height: 100%; border-radius: 6px;
background: linear-gradient(90deg, #c9a84c, #86efac);
}
.dc-prog-meta {
display: flex; justify-content: space-between; align-items: center;
}
.dc-prog-collected { font-size: .75rem; color: #9aaa8a; }
.dc-prog-collected strong { color: #e2c97a; font-weight: 700; }
.dc-prog-pct {
font-family: 'DM Serif Display', serif !important;
font-size: .85rem !important; color: #c9a84c !important;
font-weight: 400 !important;
}

/* ════════════════════════════════════════
DISTRIBUTION BAR (replaces pie chart)
════════════════════════════════════════ */
.dc-distrib {
background: rgba(12,20,12,.7);
border: .5px solid rgba(201,168,76,.15);
border-radius: 18px;
padding: 1.75rem 2rem;
}
.dc-distrib-bar {
display: flex; border-radius: 8px; overflow: hidden;
height: 12px; margin: 1rem 0;
}
.dc-distrib-legend {
display: grid;
grid-template-columns: repeat(5, 1fr);
gap: .75rem;
margin-top: 1.25rem;
}
.dc-distrib-item {}
.dc-distrib-dot {
display: inline-block;
width: 8px; height: 8px; border-radius: 50%;
margin-right: 6px; vertical-align: middle;
}
.dc-distrib-name { font-size: .75rem; color: #9aaa8a; font-weight: 500; }
.dc-distrib-val  { font-size: 1.1rem; font-weight: 700; color: #e2c97a;
font-family: 'DM Serif Display',serif !important; }

/* ════════════════════════════════════════
TESTIMONIALS
════════════════════════════════════════ */
.dc-testi {
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: 1rem;
}
.dc-testi-card {
background: rgba(12,20,12,.65);
border: .5px solid rgba(255,255,255,.06);
border-radius: 16px;
padding: 1.4rem 1.35rem;
transition: all .3s;
position: relative;
}
.dc-testi-card:hover { border-color: rgba(201,168,76,.2); transform: translateY(-3px); }
.dc-testi-quote {
font-family: Georgia, serif !important;
font-size: 2.8rem; color: rgba(201,168,76,.2);
position: absolute; top: .6rem; right: 1.1rem;
line-height: 1;
}
.dc-testi-stars { color: #c9a84c; font-size: .78rem; letter-spacing: 2px; margin-bottom: .6rem; }
.dc-testi-text {
color: #8a9e80; font-size: .8rem; line-height: 1.75;
font-style: italic; margin-bottom: 1.1rem;
}
.dc-testi-author { display: flex; align-items: center; gap: .7rem; }
.dc-testi-av {
width: 38px; height: 38px; border-radius: 50%;
display: flex; align-items: center; justify-content: center;
font-size: .78rem; font-weight: 700; color: #0f1a0f;
flex-shrink: 0;
}
.dc-testi-name { color: #d4c9b0; font-size: .82rem; font-weight: 600; }
.dc-testi-role { color: #4a5a40; font-size: .7rem; margin-top: 1px; }

/* ════════════════════════════════════════
CTA BAND
════════════════════════════════════════ */
.dc-cta {
background: rgba(201,168,76,.06);
border: .5px solid rgba(201,168,76,.2);
border-radius: 20px;
padding: 3.5rem 3rem;
text-align: center;
margin: 3rem 0 0;
position: relative;
overflow: hidden;
}
.dc-cta::before {
content: '';
position: absolute; inset: 0;
background: radial-gradient(ellipse 60% 70% at 50% 0%, rgba(201,168,76,.1), transparent);
pointer-events: none;
}
.dc-cta-title {
font-family: 'DM Serif Display', serif !important;
font-size: 2.2rem !important; font-weight: 400 !important;
color: #f0ede6 !important;
margin: 0 0 .6rem !important;
}
.dc-cta-title em { font-style: italic; color: #e2c97a; }
.dc-cta-sub { color: #6a7a60; font-size: .9rem; max-width: 480px; margin: 0 auto 1.75rem; line-height: 1.7; }

/* ════════════════════════════════════════
FOOTER — 4-column layout
════════════════════════════════════════ */
.dc-footer-wrap {
border-top: .5px solid rgba(255,255,255,.07);
margin-top: 3.5rem;
padding: 4rem 0 2.5rem;
max-width: 1280px;
margin-left: auto;
margin-right: auto;
}
.dc-footer-grid {
display: grid;
grid-template-columns: 1.6fr 1fr 1fr 1.4fr;
gap: 2.5rem 3rem;
margin-bottom: 3rem;
}
.dc-footer-col-title {
font-family: 'DM Serif Display', serif !important;
font-size: 1.1rem !important;
font-weight: 400 !important;
color: #f0ede6 !important;
margin: 0 0 1.25rem !important;
letter-spacing: -.1px;
}
.dc-footer-brand-name {
font-family: 'DM Serif Display', serif !important;
font-size: 1.5rem !important;
font-weight: 400 !important;
color: #e2c97a !important;
margin: 0 0 1.1rem !important;
display: flex; align-items: center; gap: .55rem;
}
.dc-footer-desc {
color: #4a5a40;
font-size: .8rem;
line-height: 1.85;
margin: 0 0 .85rem;
}
.dc-footer-links {
list-style: none;
margin: 0; padding: 0;
display: flex; flex-direction: column; gap: .8rem;
}
.dc-footer-links li a {
color: #6a7a60;
text-decoration: none;
font-size: .82rem;
font-weight: 500;
transition: color .18s;
display: inline-block;
}
.dc-footer-links li a:hover { color: #e2c97a; }
.dc-footer-contact {
display: flex; flex-direction: column; gap: .75rem;
}
.dc-footer-contact-item {
display: flex; align-items: flex-start; gap: .65rem;
font-size: .8rem; color: #6a7a60; line-height: 1.6;
}
.dc-footer-contact-item .ci {
flex-shrink: 0; font-size: .95rem; margin-top: .05rem;
}
.dc-footer-socials {
display: flex; gap: .55rem; margin-top: 1rem;
}
.dc-footer-social-btn {
width: 36px; height: 36px; border-radius: 50%;
display: flex; align-items: center; justify-content: center;
font-size: .95rem; text-decoration: none;
transition: transform .18s, opacity .18s;
font-style: normal;
}
.dc-footer-social-btn:hover { transform: translateY(-2px); opacity: .85; }
.dc-footer-bottom {
border-top: .5px solid rgba(255,255,255,.05);
padding-top: 1.5rem;
display: flex; align-items: center; justify-content: space-between;
gap: 1rem;
}
.dc-footer-copy {
color: #2e3e2e; font-size: .73rem;
}
.dc-footer-copy a { color: #4a5a40; text-decoration: none; }
.dc-footer-copy a:hover { color: #c9a84c; }

/* ════════════════════════════════════════
STREAMLIT BUTTON OVERRIDES
════════════════════════════════════════ */
.stButton > button {
border-radius: 10px !important;
border: .5px solid rgba(201,168,76,.35) !important;
color: #e2c97a !important;
background: transparent !important;
font-weight: 600 !important;
font-size: .78rem !important;
padding: .45rem 1rem !important;
transition: all .18s !important;
}
.stButton > button:hover {
background: rgba(201,168,76,.1) !important;
border-color: rgba(201,168,76,.6) !important;
transform: translateY(-1px) !important;
}
[data-testid="baseButton-primary"] {
background: linear-gradient(135deg,#c9a84c,#a8852c) !important;
color: #0f1a0f !important;
font-weight: 700 !important;
border: none !important;
border-radius: 12px !important;
padding: .7rem 2rem !important;
font-size: .88rem !important;
box-shadow: 0 6px 22px rgba(201,168,76,.3) !important;
}
[data-testid="baseButton-primary"]:hover {
opacity: .9 !important;
transform: translateY(-2px) !important;
box-shadow: 0 10px 32px rgba(201,168,76,.45) !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# NAVBAR
# ══════════════════════════════════════════════════════════════════════
def render_navbar():
    st.markdown("""
<div class="dc-nav">
<a class="dc-nav-brand" href="#">
<div class="dc-nav-logo">💚</div>
<span class="dc-nav-name">DonasiCare</span>
</a>
<nav class="dc-nav-links">
<a href="home"         class="active" target="_self">Beranda</a>
<a href="programdonasi"               target="_self">Program</a>
<a href="aichatbot"                   target="_self">AI Assistant</a>
<a href="transparansi"                target="_self">Transparansi</a>
<a href="volunteercenter"             target="_self">Volunteer</a>
<a href="tentangkami"                 target="_self">Tentang Kami</a>
<a href="donasi"  class="dc-nav-cta"  target="_self">💛 Donasi</a>
</nav>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════════════
BANNERS = [
    {"key": "banner_food.png",
     "title": "Bantuan Pangan<br>untuk <em>Sesama</em>",
     "desc": "Distribusi paket sembako untuk keluarga yang membutuhkan di seluruh pelosok Indonesia. Setiap donasi Anda memberi harapan baru.",
     "emoji": "🍚"},
    {"key": "banner_education.png",
     "title": "Pendidikan untuk<br><em>Masa Depan</em>",
     "desc": "Bantu anak-anak Indonesia mendapatkan akses pendidikan yang layak. Donasi perlengkapan sekolah dan beasiswa.",
     "emoji": "📚"},
    {"key": "banner_health.png",
     "title": "Kesehatan untuk<br><em>Semua</em>",
     "desc": "Program kesehatan gratis di daerah terpencil. Bersama kita wujudkan Indonesia yang lebih sehat.",
     "emoji": "🏥"},
]

def render_hero():
    if "banner_idx" not in st.session_state:
        st.session_state.banner_idx = 0
    idx = st.session_state.banner_idx
    b = BANNERS[idx]

    # Try to load image
    img_path = os.path.join(ASSETS, b["key"])
    img_tag = ""
    has_img = os.path.exists(img_path)
    if has_img:
        b64 = img_to_base64(img_path)
        if b64:
            img_tag = f'<img class="dc-hero-img" src="{b64}" alt="banner" />'

    placeholder_bg = ["linear-gradient(135deg,#1a2e1a,#2d4a1a)",
                       "linear-gradient(135deg,#1a2044,#0e2d5e)",
                       "linear-gradient(135deg,#2e1a1a,#4a1a2d)"][idx]

    dots_html = "".join(
        f'<div class="dc-dot {"on" if i == idx else ""}"></div>'
        for i in range(len(BANNERS))
    )

    # Placeholder emoji if no image
    overlay_extra = "" if has_img else f'<div style="position:absolute;right:3rem;top:50%;transform:translateY(-50%);font-size:7rem;opacity:.18;">{b["emoji"]}</div>'

    st.markdown(f"""
<div class="dc-hero" style="{'background:'+placeholder_bg if not has_img else ''}">
{img_tag}
{overlay_extra}
<div class="dc-hero-overlay">
<div class="dc-hero-eyebrow">DonasiCare · Platform Donasi Terpercaya</div>
<h1>{b["title"]}</h1>
<p class="dc-hero-desc">{b["desc"]}</p>
<a class="dc-hero-cta" href="donasi" target="_self">
💛 Donasi Sekarang
</a>
<div class="dc-dots">{dots_html}</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Carousel nav
    c1, c2, c3 = st.columns([1, 8, 1])
    with c1:
        if st.button("◀", key="prev_b", use_container_width=True):
            st.session_state.banner_idx = (idx - 1) % len(BANNERS)
            st.rerun()
    with c3:
        if st.button("▶", key="next_b", use_container_width=True):
            st.session_state.banner_idx = (idx + 1) % len(BANNERS)
            st.rerun()


# ══════════════════════════════════════════════════════════════════════
# STATS
# ══════════════════════════════════════════════════════════════════════
def render_stats():
    st.markdown("""
<div class="dc-sec">
<div class="dc-sec-left">
<div class="dc-sec-eyebrow">Dampak Nyata</div>
<h2 class="dc-sec-title">Angka yang <em>Berbicara</em></h2>
<p class="dc-sec-sub">Bersama ribuan donatur, kami terus berkembang</p>
</div>
</div>
""", unsafe_allow_html=True)

    total  = get_total_donasi()
    donors = get_donation_count()
    count  = get_campaign_count()

    # Format total nicely
    if total >= 1_000_000_000:
        total_str = f"{total/1_000_000_000:.1f}M"
    elif total >= 1_000_000:
        total_str = f"{total/1_000_000:.0f}Jt"
    else:
        total_str = format_rupiah(total)

    stats = [
        ("💰", f"Rp {total_str}", "Total Dana Terkumpul"),
        ("👥", f"{donors:,}".replace(",","."), "Donatur Aktif"),
        ("📋", str(count), "Program Berjalan"),
        ("🌍", "34", "Provinsi Terjangkau"),
    ]

    st.markdown('<div class="dc-stats">', unsafe_allow_html=True)
    for icon, num, label in stats:
        st.markdown(f"""
<div class="dc-stat">
<span class="dc-stat-icon">{icon}</span>
<div class="dc-stat-num">{num}</div>
<div class="dc-stat-label">{label}</div>
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# PROGRAM CARDS
# ══════════════════════════════════════════════════════════════════════
BADGE_MAP = {
    "Pendidikan":   "badge-pendidikan",
    "Kesehatan":    "badge-kesehatan",
    "Lingkungan":   "badge-lingkungan",
    "Bencana Alam": "badge-bencana",
    "Ekonomi":      "badge-ekonomi",
}
CAT_EMOJI = {
    "Pendidikan": "📚", "Kesehatan": "🏥", "Lingkungan": "🌿",
    "Bencana Alam": "🆘", "Ekonomi": "💼",
}
CAT_BG = {
    "Pendidikan":   "linear-gradient(135deg,#1a2044,#0e2d5e)",
    "Kesehatan":    "linear-gradient(135deg,#0d2e1f,#0a3d28)",
    "Lingkungan":   "linear-gradient(135deg,#0d2e14,#133d18)",
    "Bencana Alam": "linear-gradient(135deg,#2e1a0a,#3d280a)",
    "Ekonomi":      "linear-gradient(135deg,#1e0d2e,#2d1a3d)",
}

def render_programs():
    st.markdown("""
<div class="dc-sec">
<div class="dc-sec-left">
<div class="dc-sec-eyebrow">Program Pilihan</div>
<h2 class="dc-sec-title">Program <em>Populer</em></h2>
<p class="dc-sec-sub">Yang paling banyak mendapat dukungan donatur</p>
</div>
<a class="dc-sec-link" href="programdonasi" target="_self">Lihat semua →</a>
</div>
""", unsafe_allow_html=True)

    campaigns = get_all_campaigns()
    top3 = sorted(campaigns, key=lambda c: c.get("dana_terkumpul", 0), reverse=True)[:3]

    st.markdown('<div class="dc-programs">', unsafe_allow_html=True)
    for prog in top3:
        cat   = prog.get("kategori", "")
        badge = BADGE_MAP.get(cat, "badge-ekonomi")
        emoji = CAT_EMOJI.get(cat, "🌿")
        bg    = CAT_BG.get(cat, "linear-gradient(135deg,#1a2e1a,#0f1f0f)")
        pct   = calc_progress(prog["dana_terkumpul"], prog["target_dana"])
        pct   = min(pct, 100)

        # Try real image
        img_html = ""
        if UTILS_OK:
            try:
                img_path = get_image_for_category(cat)
                b64 = img_to_base64(img_path) if img_path else None
                if b64:
                    img_html = f'<img class="dc-prog-img" src="{b64}" alt="{cat}" />'
            except:
                pass
        if not img_html:
            img_html = f'<div class="dc-prog-img-placeholder" style="background:{bg};">{emoji}</div>'

        st.markdown(f"""
<div class="dc-prog">
{img_html}
<div class="dc-prog-body">
<span class="dc-prog-badge {badge}">{cat}</span>
<div class="dc-prog-title">{prog['judul']}</div>
<div class="dc-prog-desc">{prog['deskripsi']}</div>
<div class="dc-prog-bar-bg">
<div class="dc-prog-bar-fill" style="width:{pct}%"></div>
</div>
<div class="dc-prog-meta">
<span class="dc-prog-collected">
Terkumpul <strong>{format_rupiah(prog['dana_terkumpul'])}</strong>
</span>
<span class="dc-prog-pct">{pct}%</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# IMPACT DISTRIBUTION
# ══════════════════════════════════════════════════════════════════════
def render_distribution():
    st.markdown("""
<div class="dc-sec">
<div class="dc-sec-left">
<div class="dc-sec-eyebrow">Transparansi</div>
<h2 class="dc-sec-title">Distribusi <em>Donasi</em></h2>
<p class="dc-sec-sub">Alokasi dana ke setiap kategori program</p>
</div>
<a class="dc-sec-link" href="transparansi" target="_self">Laporan lengkap →</a>
</div>
""", unsafe_allow_html=True)

    cats = [
        ("#f59e0b", "Pangan",     35),
        ("#60a5fa", "Pendidikan", 28),
        ("#34d399", "Kesehatan",  22),
        ("#fb923c", "Bencana",    10),
        ("#a78bfa", "Lainnya",     5),
    ]

    bar_segs = "".join(
        f'<div style="width:{pct}%;background:{col};height:100%;'
        f'transition:width 1.2s ease;" title="{name} {pct}%"></div>'
        for col, name, pct in cats
    )
    legend = "".join(f"""
<div class="dc-distrib-item">
<div class="dc-distrib-val">{pct}%</div>
<div class="dc-distrib-name">
<span class="dc-distrib-dot" style="background:{col}"></span>{name}
</div>
</div>""" for col, name, pct in cats)

    st.markdown(f"""
<div class="dc-distrib">
<div class="dc-distrib-bar">{bar_segs}</div>
<div class="dc-distrib-legend">{legend}</div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TESTIMONIALS
# ══════════════════════════════════════════════════════════════════════
def render_testimonials():
    st.markdown("""
<div class="dc-sec">
<div class="dc-sec-left">
<div class="dc-sec-eyebrow">Komunitas</div>
<h2 class="dc-sec-title">Kata Mereka tentang<br><em>DonasiCare</em></h2>
</div>
</div>
""", unsafe_allow_html=True)

    testi = [
        {"text":"DonasiCare membuat saya yakin donasi saya benar-benar sampai. Transparansinya luar biasa!",
         "name":"Siti Nurhaliza","role":"Donatur tetap sejak 2023","bg":"#c9a84c","ini":"SN"},
        {"text":"Fitur AI-nya membantu saya memilih program sesuai passion saya di bidang pendidikan.",
         "name":"Ahmad Fauzi","role":"Donatur & Volunteer","bg":"#60a5fa","ini":"AF"},
        {"text":"Saya bisa melihat dampak donasi saya melalui peta bantuan. Ini yang membuat saya terus berdonasi.",
         "name":"Dewi Kartika","role":"Donatur bulanan","bg":"#34d399","ini":"DK"},
        {"text":"Sebagai volunteer, DonasiCare memberikan pengalaman tak ternilai berkontribusi langsung.",
         "name":"Rizky Pratama","role":"Volunteer aktif","bg":"#f472b6","ini":"RP"},
    ]

    st.markdown('<div class="dc-testi">', unsafe_allow_html=True)
    for t in testi:
        st.markdown(f"""
<div class="dc-testi-card">
<div class="dc-testi-quote">"</div>
<div class="dc-testi-stars">★★★★★</div>
<p class="dc-testi-text">"{t['text']}"</p>
<div class="dc-testi-author">
<div class="dc-testi-av" style="background:{t['bg']}">{t['ini']}</div>
<div>
<div class="dc-testi-name">{t['name']}</div>
<div class="dc-testi-role">{t['role']}</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# CTA
# ══════════════════════════════════════════════════════════════════════
def render_cta():
    st.markdown("""
<div class="dc-cta">
<h2 class="dc-cta-title">Mulai <em>Berbagi</em> Hari Ini</h2>
<p class="dc-cta-sub">
Tidak ada donasi yang terlalu kecil. Setiap rupiah Anda adalah
harapan nyata bagi mereka yang membutuhkan.
</p>
</div>
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2.5, 1, 2.5])
    with c2:
        if st.button("💛 Donasi Sekarang", key="cta_btn", type="primary", use_container_width=True):
            try:
                st.switch_page("pages/donasi.py")
            except:
                st.info("Menuju halaman donasi…")


# ══════════════════════════════════════════════════════════════════════
# FOOTER — 4 kolom seperti referensi gambar
# ══════════════════════════════════════════════════════════════════════
def render_footer():
    st.markdown("""
<div class="dc-footer-wrap">
<div class="dc-footer-grid">

<!-- Kolom 1: Brand & deskripsi -->
<div>
<div class="dc-footer-brand-name">💚 DonasiCare</div>
<p class="dc-footer-desc">
Platform donasi digital terpercaya yang menghubungkan
kebaikan Anda dengan mereka yang membutuhkan di seluruh
penjuru Indonesia.
</p>
<p class="dc-footer-desc">
Setiap rupiah yang Anda donasikan dikelola secara
transparan dan akuntabel, tersalurkan langsung kepada
penerima manfaat yang tepat.
</p>
</div>

<!-- Kolom 2: Tautan Cepat -->
<div>
<h4 class="dc-footer-col-title">Tautan Cepat</h4>
<ul class="dc-footer-links">
<li><a href="home"          target="_self">Beranda</a></li>
<li><a href="programdonasi" target="_self">Program Donasi</a></li>
<li><a href="aichatbot"     target="_self">AI Assistant</a></li>
<li><a href="donasi"        target="_self">Donasi Sekarang</a></li>
<li><a href="riwayatdonasi" target="_self">Riwayat Donasi</a></li>
</ul>
</div>

<!-- Kolom 3: Kategori -->
<div>
<h4 class="dc-footer-col-title">Kategori</h4>
<ul class="dc-footer-links">
<li><a href="programdonasi" target="_self">🎓 Pendidikan</a></li>
<li><a href="programdonasi" target="_self">🏥 Kesehatan</a></li>
<li><a href="programdonasi" target="_self">🌿 Lingkungan</a></li>
<li><a href="programdonasi" target="_self">🆘 Bencana Alam</a></li>
<li><a href="programdonasi" target="_self">💼 Pemberdayaan</a></li>
</ul>
</div>

<!-- Kolom 4: Kontak -->
<div>
<h4 class="dc-footer-col-title">Hubungi Kami</h4>
<div class="dc-footer-contact">
<div class="dc-footer-contact-item">
<span class="ci">📞</span>
<span>+62 812-3456-7890</span>
</div>
<div class="dc-footer-contact-item">
<span class="ci">✉️</span>
<span>halo@donasicare.id</span>
</div>
<div class="dc-footer-contact-item">
<span class="ci">🕐</span>
<span>Sen–Jum 08.00–17.00 WIB<br><strong style="color:#e2c97a;">Sabtu–Minggu – Tutup</strong></span>
</div>
<div class="dc-footer-contact-item">
<span class="ci">📍</span>
<span>Jl. Kebaikan No. 1, Jakarta Selatan, Indonesia</span>
</div>
</div>
<!-- Social icons -->
<div class="dc-footer-socials">
<a class="dc-footer-social-btn" style="background:#1877f2;"
href="#" title="Facebook">f</a>
<a class="dc-footer-social-btn" style="background:linear-gradient(135deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);"
href="#" title="Instagram">ig</a>
<a class="dc-footer-social-btn" style="background:#1da1f2;"
href="#" title="Twitter / X">𝕏</a>
<a class="dc-footer-social-btn" style="background:#25d366;"
href="#" title="WhatsApp">wa</a>
</div>
</div>

</div><!-- /grid -->

<!-- Bottom bar -->
<div class="dc-footer-bottom">
<span class="dc-footer-copy">
© 2024 <a href="#">DonasiCare</a> · Platform Donasi Terpercaya Indonesia
</span>
<span class="dc-footer-copy">
Dibuat dengan 💚 untuk Indonesia yang lebih baik
</span>
</div>

</div><!-- /footer-wrap -->
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════
def main():
    inject_css()
    render_navbar()

    # Konten utama — padding seragam 3rem kiri-kanan, max-width terpusat
    st.markdown('<div class="dc-page">', unsafe_allow_html=True)
    render_hero()
    render_stats()
    render_programs()
    render_distribution()
    render_testimonials()
    render_cta()
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer di luar dc-page agar full-width dengan padding sendiri
    render_footer()


main()