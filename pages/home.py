import streamlit as st
from utils.navbar_dark import render_navbar
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

# ── Fallback helpers ──────────────────────────────────────────────────────────
def format_rupiah(amount):
    return "Rp {:,}".format(int(amount)).replace(",", ".")

def calc_progress(a, b):
    return round((a / b) * 100) if b else 0

def get_total_donasi():   return 4_870_000_000
def get_donation_count(): return 14_872
def get_campaign_count(): return 8

def get_all_campaigns():
    return [
        {
            "judul": "Beasiswa Anak Pelosok Jawa Tengah",
            "deskripsi": "Mendukung 120 anak putus sekolah dengan kebutuhan nutrisi, alat tulis, dan biaya pendidikan.",
            "kategori": "Pendidikan",
            "dana_terkumpul": 8_200_000,
            "target_dana": 10_000_000,
        },
        {
            "judul": "Klinik Desa Terpencil Kalimantan",
            "deskripsi": "Layanan kesehatan dasar untuk 5 desa terpencil di Kalimantan Tengah yang sulit dijangkau.",
            "kategori": "Kesehatan",
            "dana_terkumpul": 6_500_000,
            "target_dana": 12_000_000,
        },
        {
            "judul": "Reboisasi Mangrove Pesisir Demak",
            "deskripsi": "Penanaman 20.000 bibit mangrove untuk mencegah abrasi pesisir dan melindungi ekosistem laut.",
            "kategori": "Lingkungan",
            "dana_terkumpul": 14_300_000,
            "target_dana": 20_000_000,
        },
    ]

ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        ext = Path(path).suffix.lstrip(".")
        if ext == "jpg": ext = "jpeg"
        return f"data:image/{ext};base64,{data}"
    except:
        return None

# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DonasiCare - Platform Donasi Terpercaya",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS — MarketBot Redesign
# ══════════════════════════════════════════════════════════════════════════════
def inject_css():
    st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Sora:wght@400;600;700&display=swap');

:root {
  --ink:        #f0ede6;
  --ink-2:      #d4c9b0;
  --ink-3:      #8a9e80;
  --paper:      #0a140a;
  --white:      rgba(12, 20, 12, 0.7);
  --brand:      #c9a84c;
  --brand-2:    #a8852c;
  --brand-glow: rgba(201,168,76,.5);
  --accent:     #86efac;
  --success:    #4ade80;
  --warn:       #f59e0b;
  --surface:    rgba(20, 30, 20, 0.6);
  --surface-2:  rgba(201,168,76,.08);
  --border:     rgba(201,168,76,.15);
  --shadow-sm:  0 4px 12px rgba(0,0,0,.3);
  --shadow-md:  0 8px 24px rgba(0,0,0,.4);
  --shadow-lg:  0 12px 32px rgba(0,0,0,.5);
  --r-sm:       8px;
  --r-md:       14px;
  --r-lg:       20px;
  --r-xl:       28px;
  --font-ui:    'Plus Jakarta Sans', sans-serif;
  --font-head:  'DM Serif Display', serif;
  --nav-h:      64px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body, .stApp, [class*="css"] {
  font-family: var(--font-ui) !important;
  background: linear-gradient(160deg, #111c11 0%, #0a140a 55%, #101a10 100%) !important;
  color: var(--ink) !important;
  line-height: 1.6;
}
a { text-decoration: none; color: inherit; }

/* ── Hide Streamlit chrome ── */
header[data-testid="stHeader"] { 
    background: transparent !important; 
    pointer-events: none !important; 
}
#MainMenu, footer, .stDeployButton { display: none !important; }
[data-testid="stSidebar"]       { display: none !important; }

/* ── Block container reset ── */
[data-testid="stAppViewContainer"] > .main > .block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: var(--ink-3); border-radius: 4px; }

/* ── NAVBAR ── */
nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 99999;
  height: var(--nav-h);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 clamp(20px,5vw,60px);
  background: rgba(5, 10, 5, 0.96);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  transition: background .3s;
}
.nav-logo {
  display: flex; align-items: center; gap: 10px;
  font-family: var(--font-head); font-weight: 700; font-size: 1.15rem;
  color: var(--brand); cursor: pointer;
}
.nav-logo-dot {
  width: 32px; height: 32px; border-radius: 8px;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: .85rem; font-weight: 800;
}
.nav-links {
  display: flex; align-items: center; gap: 4px;
  list-style: none; margin: 0; padding: 0;
}
.nav-links a {
  padding: 8px 16px; border-radius: var(--r-sm);
  font-weight: 500; font-size: .9rem; color: var(--ink-2);
  transition: all .2s; cursor: pointer;
}
.nav-links a:hover, .nav-links a.active {
  background: var(--surface-2); color: var(--brand);
}
.nav-cta {
  background: linear-gradient(135deg, var(--brand), var(--brand-2)) !important;
  color: #fff !important; padding: 9px 20px !important;
  border-radius: var(--r-sm) !important;
  box-shadow: 0 2px 12px rgba(16,185,129,.3);
  transition: transform .15s, box-shadow .15s !important;
}
.nav-cta:hover { transform: translateY(-1px); box-shadow: 0 4px 18px rgba(16,185,129,.4) !important; }

/* ── HERO SLIDER ── */
.hero-slider-wrap {
  position: relative;
  overflow: hidden;
  width: 100%;
}
.hero-slide {
  display: none;
  animation: fade-in 0.8s ease-in-out;
}
.hero-slide.active {
  display: block;
}
@keyframes fade-in {
  from { opacity: 0; transform: translateX(20px); }
  to { opacity: 1; transform: translateX(0); }
}
.hero-dots {
  display: flex; gap: 8px; margin-top: 24px;
}
.hero-dot {
  width: 10px; height: 10px; border-radius: 50%;
  background: rgba(16,185,129,.3); cursor: pointer;
  transition: all .3s;
}
.hero-dot.active {
  background: var(--brand); transform: scale(1.2);
}

/* ── MAIN CONTENT ── */
#mainContent { overflow-x: hidden; }
.section { display: block; scroll-margin-top: var(--nav-h); }

/* ── HOME ── */
#home {
  background: transparent;
  padding-bottom: 40px;
}
.hero {
  max-width: 1100px; margin: 0 auto;
  padding: clamp(40px,6vh,80px) clamp(20px,5vw,60px) 40px;
  display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center;
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(16,185,129,.08); border: 1px solid rgba(16,185,129,.18);
  color: var(--brand); padding: 6px 14px; border-radius: 99px;
  font-size: .8rem; font-weight: 600; margin-bottom: 20px;
}
.hero-badge-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--success); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
.hero h1 {
  font-family: var(--font-head); font-size: clamp(2rem,3.8vw,3rem);
  font-weight: 700; line-height: 1.15; margin-bottom: 18px; color: var(--ink);
}
.hero h1 span { color: var(--brand); }
.hero-sub { font-size: 1.02rem; color: var(--ink-3); max-width: 480px; margin-bottom: 32px; line-height: 1.7; }
.hero-btns { display: flex; gap: 12px; flex-wrap: wrap; }
.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  color: #fff; padding: 13px 26px; border-radius: var(--r-md);
  font-weight: 600; font-size: .95rem; border: none; cursor: pointer;
  box-shadow: 0 4px 20px rgba(16,185,129,.35); transition: all .2s;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(16,185,129,.45); }
.btn-outline {
  display: inline-flex; align-items: center; gap: 8px;
  border: 1.5px solid var(--border); background: var(--white);
  color: var(--ink-2); padding: 12px 24px; border-radius: var(--r-md);
  font-weight: 600; font-size: .95rem; cursor: pointer; transition: all .2s;
}
.btn-outline:hover { border-color: var(--brand); color: var(--brand); background: rgba(16,185,129,.04); }

.hero-visual { position: relative; display: flex; justify-content: center; align-items: center; }
.hero-card {
  background: var(--white); border-radius: var(--r-xl); padding: 28px;
  box-shadow: var(--shadow-lg); width: 100%; max-width: 380px;
  border: 1px solid var(--border);
}
.hero-card-header {
  display: flex; align-items: center; gap: 10px; margin-bottom: 20px;
  padding-bottom: 14px; border-bottom: 1px solid var(--border);
}
.hc-avatar {
  width: 40px; height: 40px; border-radius: 12px;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  display: flex; align-items: center; justify-content: center; color: #fff; font-size: 1.1rem;
}
.hc-name { font-weight: 700; font-size: .9rem; }
.hc-status { font-size: .75rem; color: var(--success); display: flex; align-items: center; gap: 4px; }
.hc-status::before { content:''; width:6px; height:6px; border-radius:50%; background:var(--success); display:inline-block; }
.chat-bubble { padding: 10px 14px; border-radius: 12px; margin-bottom: 10px; font-size: .85rem; max-width: 90%; }
.chat-bubble.bot { background: var(--surface-2); color: var(--ink-2); border-bottom-left-radius: 4px; }
.chat-bubble.user {
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  color: #fff; margin-left: auto; border-bottom-right-radius: 4px;
}

/* STATS */
.stats-row {
  max-width: 1100px; margin: 0 auto;
  padding: 20px clamp(20px,5vw,60px);
  display: grid; grid-template-columns: repeat(4,1fr); gap: 20px;
}
.stat-card {
  background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg);
  padding: 24px; text-align: center; box-shadow: var(--shadow-sm); transition: box-shadow .2s;
}
.stat-card:hover { box-shadow: var(--shadow-md); }
.stat-num { font-family: var(--font-head); font-size: 2rem; font-weight: 700; color: var(--brand); }
.stat-label { font-size: .82rem; color: var(--ink-3); margin-top: 4px; }

/* FEATURES / PROGRAMS */
.features { max-width: 1100px; margin: 0 auto; padding: 0 clamp(20px,5vw,60px) 40px; margin-top:40px;}
.features-title { text-align: center; margin-bottom: 40px; }
.features-title h2 { font-family: var(--font-head); font-size: 1.9rem; font-weight: 700; margin-bottom: 10px; }
.features-title p { color: var(--ink-3); font-size: 1rem; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.program-card {
  background: var(--white); border: 1px solid var(--border); border-radius: var(--r-lg);
  overflow: hidden; transition: all .25s; display:flex; flex-direction:column;
}
.program-card:hover { transform: translateY(-6px); box-shadow: var(--shadow-md); border-color: var(--brand-glow); }
.program-img-wrapper { position: relative; width: 100%; height: 186px; overflow: hidden; }
.program-img-wrapper img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.program-card:hover .program-img-wrapper img { transform: scale(1.08); }
.program-badge {
  position: absolute; top: 15px; left: 15px; background: rgba(10, 15, 28, 0.85); backdrop-filter: blur(4px);
  color: var(--brand); padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700;
  border: 1px solid rgba(247, 199, 55, 0.3); box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.program-card-body { padding: 1.8rem; display: flex; flex-direction: column; flex-grow: 1; }
.program-card-body h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; color: var(--ink); }
.program-card-body p { font-size: .88rem; color: var(--ink-3); line-height: 1.6; flex:1; margin-bottom: 1.5rem; }
.prog-bar-bg { background:var(--surface-2); border-radius:6px; height:6px; overflow:hidden; margin:14px 0 8px; }
.prog-bar { height:100%; background:linear-gradient(90deg,var(--brand),var(--accent)); border-radius:6px; }
.prog-meta { display:flex; justify-content:space-between; font-size:.75rem; color:var(--ink-3); }
.prog-meta strong { color:var(--brand); font-weight:700; }
.card-btn {
  display: block; width: 100%; text-align: center; margin-top: auto;
  background: rgba(201,168,76,0.08); color: var(--brand);
  border: 1px solid rgba(201,168,76,0.3); border-radius: 12px;
  font-weight: 700; padding: 0.7rem; transition: all 0.3s; font-size: 0.9rem; text-decoration: none;
}
.card-btn:hover {
  background: linear-gradient(135deg, var(--brand), var(--brand-2)); text-decoration: none;
  color: var(--paper); box-shadow: 0 4px 15px rgba(201,168,76,0.3); transform: translateY(-2px);
}

/* ABOUT / DISTRIBUTION */
#about { background: var(--paper); padding-top: 40px; }
.about-inner { max-width: 1000px; margin: 0 auto; padding: clamp(30px,5vh,60px) clamp(20px,5vw,60px) 40px; }
.section-badge {
  display: inline-block; background: rgba(16,185,129,.08); color: var(--brand);
  padding: 5px 14px; border-radius: 99px; font-size: .78rem; font-weight: 600;
  margin-bottom: 14px; border: 1px solid rgba(16,185,129,.15);
}
.about-inner h2 { font-family: var(--font-head); font-size: clamp(1.7rem,3vw,2.4rem); font-weight: 700; margin-bottom: 20px; }
.about-inner > p { color: var(--ink-3); line-height: 1.8; margin-bottom: 14px; font-size: .97rem; }

.distrib-box { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-xl); padding: 32px; box-shadow: var(--shadow-md); margin-top:32px; }
.distrib-bar { display:flex; border-radius:8px; overflow:hidden; height:18px; gap:3px; margin: 1.2rem 0 1.8rem; }
.distrib-seg { height:100%; border-radius:4px; }
.distrib-legend { display:grid; grid-template-columns:repeat(5,1fr); gap:1rem; }
.dval { font-family:var(--font-head); font-size:1.5rem; font-weight:700; color:var(--brand); margin-bottom:.2rem; }
.dlabel { display:flex; align-items:center; gap:.4rem; font-size:.8rem; color:var(--ink-3); font-weight:500; }
.ddot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }

/* TESTIMONIALS / SARAN */
#saran { background: linear-gradient(160deg, #0a140a 0%, var(--paper) 100%); padding-top: 40px; padding-bottom:60px; }
.saran-inner { max-width: 1000px; margin: 0 auto; padding: clamp(30px,5vh,60px) clamp(20px,5vw,60px) 40px; }
.saran-inner h2 { font-family: var(--font-head); font-size: clamp(1.7rem,3vw,2.4rem); font-weight: 700; margin-bottom: 8px; }
.saran-inner > p { color: var(--ink-3); margin-bottom: 36px; font-size: .97rem; }
.saran-cards { display: grid; grid-template-columns: repeat(2,1fr); gap: 20px; }
.saran-card { background: var(--white); border: 1px solid var(--border); border-radius: var(--r-xl); padding: 24px; transition: all .25s; position: relative; overflow: hidden; }
.saran-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transform:scaleX(0); transform-origin:left; transition:transform .3s; }
.saran-card:hover::before { transform:scaleX(1); }
.saran-card:hover { box-shadow: var(--shadow-md); transform: translateY(-3px); }
.saran-num { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, var(--brand), var(--brand-2)); color: #fff; font-weight: 800; font-size: .85rem; display: flex; align-items: center; justify-content: center; margin-bottom: 14px; }
.saran-card h3 { font-size: 1rem; font-weight: 700; margin-bottom: 8px; color: var(--ink); }
.saran-card p { font-size: .88rem; color: var(--ink-3); line-height: 1.7; font-style:italic;}
.saran-author { display:flex; align-items:center; gap:10px; margin-top:16px; }
.saran-avatar { width:32px; height:32px; border-radius:50%; background:var(--brand-glow); display:flex; align-items:center; justify-content:center; font-size:.7rem; font-weight:800; color:#fff;}
.saran-name { font-weight:700; font-size:.85rem; color:var(--ink); }

/* FOOTER */
footer { background: var(--ink); color: rgba(255,255,255,.5); text-align: center; padding: 24px 20px; font-size: .82rem; }
footer span { color: rgba(255,255,255,.8); font-weight: 600; }

@media (max-width: 768px) {
  nav .nav-links { display: none; }
  .hero { grid-template-columns: 1fr; }
  .hero-visual { display: none; }
  .stats-row { grid-template-columns: repeat(2,1fr); }
  .features-grid { grid-template-columns: 1fr; }
  .distrib-legend { grid-template-columns: repeat(2,1fr); }
  .saran-cards { grid-template-columns: 1fr; }
}
</style>
""")

# ══════════════════════════════════════════════════════════════════════════════
# COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════
def render_hero():
    hero_img_b64 = img_to_base64(os.path.join(ASSETS, "donasi.png"))
    hero_img_html = f'<img src="{hero_img_b64}" alt="Donasi" style="width:100%; max-width:420px; object-fit:contain; border-radius:var(--r-xl); box-shadow:var(--shadow-lg);"/>' if hero_img_b64 else ''
    html_content = """
<section id="home" class="section">
  <div class="hero">
    <div class="hero-content hero-slider-wrap" id="heroSlider">
      
      <!-- Slide 1 -->
      <div class="hero-slide active">
          <div class="hero-badge">
            <div class="hero-badge-dot"></div>
            Platform Donasi Terpercaya
          </div>
          <h1>Setiap Rupiah,<br>Nyata <span>Mengubah</span><br>Kehidupan</h1>
          <p class="hero-sub" style="text-align: justify;">Bergabung dengan belasan ribu donatur yang telah memberi dampak nyata bagi jutaan keluarga di seluruh penjuru Indonesia melalui DonasiCare.</p>
          <div class="hero-btns">
            <a href="/donasi" target="_self" class="btn-primary">Mulai Berdonasi</a>
            <a href="/programdonasi" target="_self" class="btn-outline">Lihat Program</a>
          </div>
      </div>

      <!-- Slide 2 -->
      <div class="hero-slide">
          <div class="hero-badge">
            <div class="hero-badge-dot"></div>
            Menebar Kebaikan Bersama
          </div>
          <h1>Bersama Kita,<br>Wujudkan <span>Harapan</span><br>Anak Bangsa</h1>
          <p class="hero-sub" style="text-align: justify;">Ratusan program pendidikan dan beasiswa menunggu dukungan Anda. Berikan mereka masa depan yang lebih cerah bersama DonasiCare.</p>
          <div class="hero-btns">
            <a href="/programdonasi" target="_self" class="btn-primary">Dukung Pendidikan</a>
            <a href="/tentangkami" target="_self" class="btn-outline">Pelajari Lebih Lanjut</a>
          </div>
      </div>

      <!-- Slide 3 -->
      <div class="hero-slide">
          <div class="hero-badge">
            <div class="hero-badge-dot"></div>
            Respons Cepat Bencana
          </div>
          <h1>Salurkan Bantuan<br>Tepat pada <span>Waktunya</span></h1>
          <p class="hero-sub" style="text-align: justify;">Dalam setiap krisis, kecepatan adalah kunci. Bantu kami menyalurkan logistik dan bantuan medis darurat ke daerah terdampak bencana.</p>
          <div class="hero-btns">
            <a href="/donasi" target="_self" class="btn-primary">Bantu Sekarang</a>
            <a href="/transparansi" target="_self" class="btn-outline">Lihat Laporan Dampak</a>
          </div>
      </div>
      
      <!-- Slider Dots -->
      <div class="hero-dots">
        <div class="hero-dot active" onclick="setSlide(0)"></div>
        <div class="hero-dot" onclick="setSlide(1)"></div>
        <div class="hero-dot" onclick="setSlide(2)"></div>
      </div>

    </div>
    <div class="hero-visual">
      __HERO_IMAGE__
    </div>
  </div>

  <script>
    let slideIndex = 0;
    let slideInterval;
    
    function showSlide(index) {
        const slides = document.querySelectorAll('.hero-slide');
        const dots = document.querySelectorAll('.hero-dot');
        if(!slides.length) return;
        
        slides.forEach(s => s.classList.remove('active'));
        dots.forEach(d => d.classList.remove('active'));
        
        slideIndex = index;
        if (slideIndex >= slides.length) slideIndex = 0;
        if (slideIndex < 0) slideIndex = slides.length - 1;
        
        slides[slideIndex].classList.add('active');
        dots[slideIndex].classList.add('active');
    }
    
    function setSlide(index) {
        clearInterval(slideInterval);
        showSlide(index);
        startAutoSlide();
    }
    
    function startAutoSlide() {
        slideInterval = setInterval(() => {
            showSlide(slideIndex + 1);
        }, 5000); // 5 seconds per slide
    }
    
    // Attempt to start slider when script runs
    setTimeout(() => {
        showSlide(0);
        startAutoSlide();
    }, 500);
  </script>
</section>
"""
    st.html(html_content.replace('__HERO_IMAGE__', hero_img_html))

def render_stats():
    total  = get_total_donasi()
    donors = get_donation_count()
    count  = get_campaign_count()
    total_str = f"{total/1_000_000_000:.1f}M" if total >= 1_000_000_000 else format_rupiah(total)
    
    st.html(f"""
  <div class="stats-row">
    <div class="stat-card"><div class="stat-num">Rp {total_str}</div><div class="stat-label">Total Dana Terkumpul</div></div>
    <div class="stat-card"><div class="stat-num">{donors:,}</div><div class="stat-label">Donatur Aktif</div></div>
    <div class="stat-card"><div class="stat-num">{count}</div><div class="stat-label">Program Berjalan</div></div>
    <div class="stat-card"><div class="stat-num">34</div><div class="stat-label">Provinsi Terjangkau</div></div>
  </div>
""")

def render_programs():
    campaigns = get_all_campaigns()
    top3 = sorted(campaigns, key=lambda c: c.get("dana_terkumpul", 0), reverse=True)[:3]
    
    html = """
<div class="features">
  <div class="features-title">
    <h2>Program Pilihan Kami</h2>
    <p>Program yang paling banyak mendapat dukungan donatur</p>
  </div>
  <div class="features-grid">
"""
    for prog in top3:
        cat = prog.get("kategori", "")
        pct = min(calc_progress(prog["dana_terkumpul"], prog["target_dana"]), 100)
        
        img_path = get_image_for_category(cat)
        img_b64 = img_to_base64(img_path) if img_path else ""
        
        html += f"""
    <div style="display: flex; flex-direction: column; gap: 1.2rem; height: 100%;">
      <div class="program-card" style="margin: 0; height: 100%;">
        <div class="program-img-wrapper">
          <img src="{img_b64}" alt="{prog['judul']}" />
          <span class="program-badge">{prog['kategori']}</span>
        </div>
        <div class="program-card-body">
          <h3>{prog['judul']}</h3>
          <p>{prog['deskripsi']}</p>
          
          <div class="prog-bar-bg">
            <div class="prog-bar" style="width:{pct}%"></div>
          </div>
          <div class="prog-meta" style="margin-bottom: 0;">
            <strong style="color:var(--brand); font-size:0.85rem;">{format_rupiah(prog['dana_terkumpul'])}</strong>
            <span style="color:var(--ink-3); font-weight:normal; font-size:0.85rem;">{format_rupiah(prog['target_dana'])}</span>
          </div>
        </div>
      </div>
      <a href="/donasi" target="_self" class="card-btn">Lihat Detail & Donasi</a>
    </div>
"""
    html += "</div></div>"
    st.html(html)

def render_distribution():
    cats = [
        ("#f59e0b","Pangan",35),
        ("#10b981","Pendidikan",28), # brand green
        ("#06b6d4","Kesehatan",22),
        ("#6366f1","Bencana",10),
        ("#a855f7","Lainnya",5),
    ]
    segs = "".join(f'<div class="distrib-seg" style="width:{pct}%;background:{col}"></div>' for col,name,pct in cats)
    legend = "".join(f"""
<div>
  <div class="dval">{pct}%</div>
  <div class="dlabel"><div class="ddot" style="background:{col}"></div>{name}</div>
</div>""" for col,name,pct in cats)

    st.html(f"""
<section id="about" class="section">
  <div class="about-inner">
    <div class="section-badge">Transparansi</div>
    <h2>Distribusi Donasi</h2>
    <p style="text-align: justify;">DonasiCare berkomitmen memberikan transparansi penuh atas setiap rupiah yang Anda salurkan. Berikut adalah alokasi dana donatur ke berbagai kategori program.</p>
    
    <div class="distrib-box">
      <div class="distrib-bar">{segs}</div>
      <div class="distrib-legend">{legend}</div>
    </div>
  </div>
</section>
""")

def render_testimonials():
    st.html("""
<section id="saran" class="section">
  <div class="saran-inner">
    <div class="section-badge">Komunitas</div>
    <h2>Kata Mereka tentang DonasiCare</h2>
    <p>Bergabunglah dengan ribuan orang yang telah merasakan indahnya berbagi.</p>
    
    <div class="saran-cards">
      <div class="saran-card">
        <div class="saran-num">"</div>
        <h3>Sangat Transparan</h3>
        <p>"DonasiCare benar-benar mengubah cara saya berdonasi. Laporan yang transparan membuat saya yakin ke mana dana saya pergi."</p>
        <div class="saran-author">
            <div class="saran-avatar" style="background:#10b981">SN</div>
            <div>
                <div class="saran-name">Siti Nurhaliza</div>
                <div style="font-size:0.7rem;color:var(--ink-3)">Donatur tetap sejak 2023</div>
            </div>
        </div>
      </div>
      
      <div class="saran-card">
        <div class="saran-num">"</div>
        <h3>Fitur AI Membantu</h3>
        <p>"Fitur AI-nya membantu saya memilih program sesuai passion saya di bidang pendidikan. Sangat personal dan interaktif!"</p>
        <div class="saran-author">
            <div class="saran-avatar" style="background:#06b6d4">AF</div>
            <div>
                <div class="saran-name">Ahmad Fauzi</div>
                <div style="font-size:0.7rem;color:var(--ink-3)">Donatur & Volunteer</div>
            </div>
        </div>
      </div>
    </div>
  </div>
</section>
""")

def render_footer():
    st.html("""
<footer>
  &copy; 2026 <span>DonasiCare </span> Dibuat dengan 💚 untuk Indonesia yang lebih baik.
</footer>
</div> <!-- MainContent Close -->
""")

def main():
    inject_css()
    st.html('<div id="mainContent">')
    render_navbar("home")
    render_hero()
    render_stats()
    render_programs()
    render_distribution()
    render_testimonials()
    render_footer()

if __name__ == "__main__":
    main()