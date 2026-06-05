import streamlit as st
import base64
import os
import time
import sys
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.campaign import get_all_campaigns, get_total_donasi, get_campaign_count
from utils.helpers import format_rupiah, calc_progress, get_image_for_category, get_donation_count

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – HOME PAGE
# Landing page with: Header Nav, Banner Carousel, Stats, Popular
# Programs, Testimonials, and CTA "Donasi Sekarang" button.
# Uses: streamlit-card, streamlit-elements
# ═══════════════════════════════════════════════════════════════════════

# ── Helper: encode local image to base64 data URI ──────────────────
def img_to_base64(path: str) -> str:
    """Return a base64 data-URI string for the given image file."""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(path).suffix.lstrip(".")
    if ext == "jpg":
        ext = "jpeg"
    return f"data:image/{ext};base64,{data}"


ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


# ═══════════════════════════════════════════════════════════════════════
# CUSTOM CSS  –  Premium golden-accent + modern glassmorphism look
# ═══════════════════════════════════════════════════════════════════════
def inject_custom_css():
    st.markdown("""
    <style>
    /* ── Google Font ─────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Global Reset ────────────────────────────────────────────── */
    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #0a0f1c 0%, #121a2e 50%, #0d1520 100%); }

    /* Hide default header & footer */
    header[data-testid="stHeader"] { background: transparent !important; }
    .stDeployButton { display: none; }

    /* ── Custom Navbar ───────────────────────────────────────────── */
    .navbar-container {
        background: rgba(10, 15, 28, 0.85);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(247, 199, 55, 0.15);
        padding: 0.6rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: sticky;
        top: 0;
        z-index: 9999;
        margin: -1rem -1rem 2rem -1rem;
    }
    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .navbar-brand .logo-icon {
        width: 42px; height: 42px;
        background: linear-gradient(135deg, #f7c737, #f59e0b);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem;
        box-shadow: 0 4px 15px rgba(247, 199, 55, 0.3);
    }
    .navbar-brand .brand-text {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f7c737, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .navbar-links {
        display: flex;
        gap: 0.3rem;
        flex-wrap: wrap;
    }
    .navbar-links a {
        color: #cbd5e1;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.3s ease;
        white-space: nowrap;
    }
    .navbar-links a:hover, .navbar-links a.active {
        color: #f7c737;
        background: rgba(247, 199, 55, 0.1);
    }

    /* ── Section Titles ──────────────────────────────────────────── */
    .section-title {
        text-align: center;
        margin: 3rem 0 0.5rem 0;
    }
    .section-title h2 {
        color: #f1f5f9;
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .section-title h2 span {
        background: linear-gradient(135deg, #f7c737, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .section-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* ── Hero Banner / Carousel ──────────────────────────────────── */
    .hero-banner {
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    }
    .hero-banner img {
        width: 100%;
        height: 420px;
        object-fit: cover;
        display: block;
    }
    .hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(
            to right,
            rgba(10, 15, 28, 0.92) 0%,
            rgba(10, 15, 28, 0.6) 50%,
            transparent 100%
        );
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 3rem 3.5rem;
    }
    .hero-overlay h1 {
        color: #f7c737;
        font-size: 2.6rem;
        font-weight: 900;
        line-height: 1.15;
        margin-bottom: 0.8rem;
        text-shadow: 0 2px 20px rgba(0,0,0,0.3);
    }
    .hero-overlay p {
        color: #e2e8f0;
        font-size: 1.05rem;
        max-width: 480px;
        line-height: 1.7;
        margin-bottom: 1.5rem;
    }
    .hero-cta {
        display: inline-block;
        background: linear-gradient(135deg, #f7c737, #f59e0b);
        color: #0a0f1c !important;
        padding: 0.85rem 2.2rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1rem;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(247, 199, 55, 0.35);
        width: fit-content;
    }
    .hero-cta:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(247, 199, 55, 0.5);
    }

    /* Carousel Dots */
    .carousel-dots {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-top: -2.5rem;
        margin-bottom: 2rem;
        position: relative;
        z-index: 10;
    }
    .carousel-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transition: all 0.3s;
    }
    .carousel-dot.active {
        background: #f7c737;
        width: 28px;
        border-radius: 5px;
    }

    /* ── Stat Cards ──────────────────────────────────────────────── */
    .stat-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(247, 199, 55, 0.12);
        border-radius: 16px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stat-card:hover {
        transform: translateY(-6px);
        border-color: rgba(247, 199, 55, 0.35);
        box-shadow: 0 16px 40px rgba(247, 199, 55, 0.12);
    }
    .stat-icon {
        font-size: 2.2rem;
        margin-bottom: 0.6rem;
        display: block;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f7c737, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .stat-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* ── Program Card ────────────────────────────────────────────── */
    .program-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .program-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        border-color: rgba(247, 199, 55, 0.25);
    }
    .program-card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    .program-card-body {
        padding: 1.3rem 1.5rem;
    }
    .program-badge {
        display: inline-block;
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.6rem;
    }
    .badge-education { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
    .badge-food { background: rgba(249, 115, 22, 0.2); color: #fb923c; }
    .badge-health { background: rgba(16, 185, 129, 0.2); color: #34d399; }

    .program-card-body h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .program-card-body p {
        color: #94a3b8;
        font-size: 0.85rem;
        line-height: 1.6;
        margin-bottom: 1rem;
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
    .progress-info {
        display: flex;
        justify-content: space-between;
        font-size: 0.78rem;
        color: #94a3b8;
    }
    .progress-info strong {
        color: #f7c737;
    }

    /* ── Testimonial Card ────────────────────────────────────────── */
    .testimonial-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 1.8rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .testimonial-card:hover {
        transform: translateY(-4px);
        border-color: rgba(247, 199, 55, 0.2);
    }
    .testimonial-quote {
        font-size: 2.5rem;
        color: rgba(247, 199, 55, 0.3);
        position: absolute;
        top: 0.8rem;
        right: 1.5rem;
        font-family: Georgia, serif !important;
    }
    .testimonial-text {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.7;
        margin-bottom: 1.2rem;
        font-style: italic;
    }
    .testimonial-author {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    .testimonial-avatar {
        width: 44px; height: 44px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
        font-weight: 700;
        color: #0a0f1c;
    }
    .testimonial-name {
        color: #f1f5f9;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .testimonial-role {
        color: #64748b;
        font-size: 0.78rem;
    }
    .stars { color: #f7c737; font-size: 0.85rem; letter-spacing: 2px; }

    /* ── CTA Section ─────────────────────────────────────────────── */
    .cta-section {
        background: linear-gradient(135deg, rgba(247, 199, 55, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
        border: 1px solid rgba(247, 199, 55, 0.2);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 3rem 0;
        position: relative;
        overflow: hidden;
    }
    .cta-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(247,199,55,0.05) 0%, transparent 50%);
        animation: pulse-glow 4s ease-in-out infinite;
    }
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
    }
    .cta-section h2 {
        color: #f1f5f9;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
        position: relative;
    }
    .cta-section p {
        color: #94a3b8;
        font-size: 1rem;
        max-width: 550px;
        margin: 0 auto 1.8rem auto;
        position: relative;
    }

    /* ── Footer ──────────────────────────────────────────────────── */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #475569;
        font-size: 0.8rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 2rem;
    }
    .footer a { color: #f7c737; text-decoration: none; }

    /* ── Animation Keyframes ─────────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeInUp 0.7s ease forwards;
    }
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    .delay-4 { animation-delay: 0.4s; }

    /* ── Hide Streamlit Branding ──────────────────────────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# NAVBAR COMPONENT
# ═══════════════════════════════════════════════════════════════════════
def render_navbar():
    st.markdown("""
    <div class="navbar-container">
        <div class="navbar-brand">
            <div class="logo-icon">💚</div>
            <span class="brand-text">DonasiCare</span>
        </div>
        <div class="navbar-links">
            <a href="home" class="active" target="_self">Home</a>
            <a href="programdonasi" target="_self">Program Donasi</a>
            <a href="aichatbot" target="_self">AI Assistant</a>
            <a href="donasi" target="_self">Donasi Sekarang</a>
            <a href="transparansi" target="_self">Transparansi</a>
            <a href="volunteer" target="_self">Volunteer</a>
            <a href="tentangkami" target="_self">Tentang Kami</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# HERO BANNER CAROUSEL
# ═══════════════════════════════════════════════════════════════════════
def render_hero_banner():
    banners = [
        {
            "image": os.path.join(ASSETS, "banner_food.png"),
            "title": "Bantuan Pangan<br>untuk Sesama",
            "desc": "Distribusi paket sembako untuk keluarga yang membutuhkan di seluruh pelosok Indonesia. Setiap donasi Anda memberi harapan baru.",
        },
        {
            "image": os.path.join(ASSETS, "banner_education.png"),
            "title": "Pendidikan untuk<br>Masa Depan",
            "desc": "Bantu anak-anak Indonesia mendapatkan akses pendidikan yang layak. Donasi perlengkapan sekolah dan beasiswa pendidikan.",
        },
        {
            "image": os.path.join(ASSETS, "banner_health.png"),
            "title": "Kesehatan untuk<br>Semua",
            "desc": "Program kesehatan gratis untuk masyarakat di daerah terpencil. Bersama kita wujudkan Indonesia yang lebih sehat.",
        },
    ]

    # Auto-rotate banner based on time
    if "banner_idx" not in st.session_state:
        st.session_state.banner_idx = 0

    idx = st.session_state.banner_idx
    b = banners[idx]
    img_b64 = img_to_base64(b["image"])

    st.markdown(f"""
    <div class="hero-banner animate-in">
        <img src="{img_b64}" alt="campaign banner" />
        <div class="hero-overlay">
            <h1>{b["title"]}</h1>
            <p>{b["desc"]}</p>
            <a class="hero-cta" href="#donasi-sekarang">💛 Donasi Sekarang</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Carousel dots
    dots_html = '<div class="carousel-dots">'
    for i in range(len(banners)):
        active = "active" if i == idx else ""
        dots_html += f'<div class="carousel-dot {active}"></div>'
    dots_html += "</div>"
    st.markdown(dots_html, unsafe_allow_html=True)

    # Navigation buttons
    col_prev, col_spacer, col_next = st.columns([1, 6, 1])
    with col_prev:
        if st.button("◀ Sebelumnya", key="prev_banner", use_container_width=True):
            st.session_state.banner_idx = (idx - 1) % len(banners)
            st.rerun()
    with col_next:
        if st.button("Selanjutnya ▶", key="next_banner", use_container_width=True):
            st.session_state.banner_idx = (idx + 1) % len(banners)
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# STATISTICS SECTION
# ═══════════════════════════════════════════════════════════════════════
def render_statistics():
    st.markdown("""
    <div class="section-title animate-in">
        <h2>Dampak <span>Nyata</span> Donasi Anda</h2>
    </div>
    <p class="section-subtitle">Setiap rupiah yang Anda donasikan membawa perubahan besar</p>
    """, unsafe_allow_html=True)

    # Ambil data real dari database
    total_donasi = get_total_donasi()
    donor_count = get_donation_count()
    campaign_count = get_campaign_count()

    stats = [
        ("💰", format_rupiah(total_donasi), "Total Donasi Terkumpul"),
        ("👥", f"{donor_count:,}".replace(",", "."), "Donatur"),
        ("📦", str(campaign_count), "Program Aktif"),
        ("🌍", "34", "Provinsi Terjangkau"),
    ]

    cols = st.columns(4)
    for i, (icon, number, label) in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div class="stat-card animate-in delay-{i+1}">
                <span class="stat-icon">{icon}</span>
                <div class="stat-number">{number}</div>
                <div class="stat-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# POPULAR PROGRAMS SECTION  (uses streamlit_card)
# ═══════════════════════════════════════════════════════════════════════
def render_popular_programs():
    st.markdown("""
    <div class="section-title animate-in" id="program-donasi">
        <h2>Program <span>Populer</span></h2>
    </div>
    <p class="section-subtitle">Program donasi pilihan yang paling banyak mendapat dukungan</p>
    """, unsafe_allow_html=True)

    # Ambil kampanye dari database (top 3 berdasarkan dana terkumpul)
    campaigns = get_all_campaigns()
    # Sort by dana_terkumpul descending, take top 3
    campaigns_sorted = sorted(campaigns, key=lambda c: c.get('dana_terkumpul', 0), reverse=True)[:3]

    badge_class_map = {
        "Pendidikan": "badge-education",
        "Kesehatan": "badge-health",
        "Bencana Alam": "badge-food",
        "Lingkungan": "badge-education",
        "Panti Asuhan": "badge-food",
    }

    if campaigns_sorted:
        cols = st.columns(len(campaigns_sorted))
        for i, prog in enumerate(campaigns_sorted):
            with cols[i]:
                img_path = get_image_for_category(prog['kategori'])
                img_b64 = img_to_base64(img_path)
                progress = calc_progress(prog['dana_terkumpul'], prog['target_dana'])
                badge_cls = badge_class_map.get(prog['kategori'], 'badge-food')
                html_card = f"""
<div class="program-card animate-in delay-{i+1}">
<img src="{img_b64}" alt="{prog['judul']}" />
<div class="program-card-body">
<span class="program-badge {badge_cls}">{prog['kategori']}</span>
<h3>{prog['judul']}</h3>
<p>{prog['deskripsi']}</p>
<div class="progress-bar-bg">
<div class="progress-bar-fill" style="width:{progress}%"></div>
</div>
<div class="progress-info">
<span>Terkumpul <strong>{format_rupiah(prog['dana_terkumpul'])}</strong></span>
<span>Target {format_rupiah(prog['target_dana'])}</span>
</div>
</div>
</div>
"""
                st.markdown(html_card, unsafe_allow_html=True)
    else:
        st.info("Belum ada program kampanye di database.")

    # ── Use streamlit_card for interactive CTA cards ────────────────
    try:
        from streamlit_card import card

        st.markdown("<br>", unsafe_allow_html=True)

        card_cols = st.columns(3)
        card_data = [
            ("🤖", "AI Assistant", "Dapatkan rekomendasi program donasi yang sesuai dengan minat Anda menggunakan AI."),
            ("📊", "Transparansi Dana", "Lihat laporan penggunaan dana donasi secara real-time dan transparan."),
            ("🤝", "Jadi Volunteer", "Bergabunglah dengan ribuan relawan untuk membantu sesama secara langsung."),
        ]

        for i, (icon, title, desc) in enumerate(card_data):
            with card_cols[i]:
                card(
                    title=f"{icon} {title}",
                    text=desc,
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "180px",
                            "border-radius": "16px",
                            "background": "rgba(30, 41, 59, 0.6)",
                            "border": "1px solid rgba(247, 199, 55, 0.12)",
                            "box-shadow": "0 8px 30px rgba(0,0,0,0.2)",
                        },
                        "title": {
                            "color": "#f1f5f9",
                            "font-size": "1rem",
                            "font-weight": "700",
                        },
                        "text": {
                            "color": "#94a3b8",
                            "font-size": "0.82rem",
                        },
                        "filter": {
                            "background-color": "rgba(247, 199, 55, 0.03)",
                        }
                    },
                    key=f"card_{i}",
                )
    except ImportError:
        pass  # streamlit_card not installed; skip gracefully


# ═══════════════════════════════════════════════════════════════════════
# TESTIMONIALS SECTION
# ═══════════════════════════════════════════════════════════════════════
def render_testimonials():
    st.markdown("""
    <div class="section-title animate-in">
        <h2>Kata Mereka tentang <span>DonasiCare</span></h2>
    </div>
    <p class="section-subtitle">Testimoni dari para donatur yang telah berkontribusi</p>
    """, unsafe_allow_html=True)

    testimonials = [
        {
            "text": "DonasiCare membuat saya yakin bahwa donasi saya benar-benar sampai ke yang membutuhkan. Transparansinya luar biasa!",
            "name": "Siti Nurhaliza",
            "role": "Donatur Tetap sejak 2023",
            "avatar_bg": "#f7c737",
            "initials": "SN",
            "stars": 5,
        },
        {
            "text": "Platform yang sangat mudah digunakan. Fitur AI-nya membantu saya memilih program yang sesuai dengan passion saya di bidang pendidikan.",
            "name": "Ahmad Fauzi",
            "role": "Donatur & Volunteer",
            "avatar_bg": "#60a5fa",
            "initials": "AF",
            "stars": 5,
        },
        {
            "text": "Saya bisa melihat langsung dampak donasi saya melalui peta bantuan. Ini yang membuat saya terus berdonasi setiap bulan.",
            "name": "Dewi Kartika",
            "role": "Donatur Bulanan",
            "avatar_bg": "#34d399",
            "initials": "DK",
            "stars": 5,
        },
        {
            "text": "Sebagai volunteer, DonasiCare memberikan pengalaman yang tak ternilai. Saya bisa berkontribusi langsung di lapangan.",
            "name": "Rizky Pratama",
            "role": "Volunteer Aktif",
            "avatar_bg": "#f472b6",
            "initials": "RP",
            "stars": 5,
        },
    ]

    cols = st.columns(4)
    for i, t in enumerate(testimonials):
        with cols[i]:
            stars = "★" * t["stars"]
            st.markdown(f"""
            <div class="testimonial-card animate-in delay-{i+1}">
                <div class="testimonial-quote">"</div>
                <div class="stars">{stars}</div>
                <p class="testimonial-text">"{t['text']}"</p>
                <div class="testimonial-author">
                    <div class="testimonial-avatar" style="background:{t['avatar_bg']}">{t['initials']}</div>
                    <div>
                        <div class="testimonial-name">{t['name']}</div>
                        <div class="testimonial-role">{t['role']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# CTA SECTION  – "Donasi Sekarang" Call-to-Action
# ═══════════════════════════════════════════════════════════════════════
def render_cta():
    st.markdown("""
    <div class="cta-section animate-in" id="donasi-sekarang">
        <h2>Mulai <span style="color:#f7c737">Berbagi</span> Hari Ini</h2>
        <p>Tidak ada donasi yang terlalu kecil. Setiap rupiah Anda adalah harapan bagi mereka yang membutuhkan.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("💛 DONASI SEKARANG", key="cta_donate", use_container_width=True, type="primary"):
            st.switch_page("pages/donasi.py")


# ═══════════════════════════════════════════════════════════════════════
# STREAMLIT ELEMENTS - IMPACT DASHBOARD MINI
# ═══════════════════════════════════════════════════════════════════════
def render_impact_dashboard():
    """Render a mini dashboard using streamlit-elements (if available)."""
    try:
        from streamlit_elements import elements, mui, html, nivo

        st.markdown("""
        <div class="section-title animate-in" id="transparansi">
            <h2>Dashboard <span>Impact</span></h2>
        </div>
        <p class="section-subtitle">Distribusi donasi berdasarkan kategori program</p>
        """, unsafe_allow_html=True)

        # Nivo pie chart data
        pie_data = [
            {"id": "Pangan", "label": "Pangan", "value": 35, "color": "#f59e0b"},
            {"id": "Pendidikan", "label": "Pendidikan", "value": 28, "color": "#3b82f6"},
            {"id": "Kesehatan", "label": "Kesehatan", "value": 22, "color": "#10b981"},
            {"id": "Bencana", "label": "Bencana", "value": 10, "color": "#ef4444"},
            {"id": "Lainnya", "label": "Lainnya", "value": 5, "color": "#8b5cf6"},
        ]

        with elements("impact_dashboard"):
            with mui.Box(
                sx={
                    "bgcolor": "rgba(30, 41, 59, 0.5)",
                    "borderRadius": "18px",
                    "border": "1px solid rgba(255,255,255,0.06)",
                    "p": 3,
                    "height": 350,
                    "backdropFilter": "blur(12px)",
                }
            ):
                nivo.Pie(
                    data=pie_data,
                    margin={"top": 30, "right": 80, "bottom": 60, "left": 80},
                    innerRadius=0.55,
                    padAngle=2,
                    cornerRadius=6,
                    activeOuterRadiusOffset=8,
                    colors={"datum": "data.color"},
                    borderWidth=0,
                    enableArcLinkLabels=True,
                    arcLinkLabelsSkipAngle=10,
                    arcLinkLabelsTextColor="#94a3b8",
                    arcLinkLabelsColor={"from": "color"},
                    arcLabelsSkipAngle=10,
                    arcLabelsTextColor="#0a0f1c",
                    theme={
                        "background": "transparent",
                        "textColor": "#94a3b8",
                        "fontSize": 12,
                        "tooltip": {
                            "container": {
                                "background": "#1e293b",
                                "color": "#f1f5f9",
                                "borderRadius": "8px",
                                "border": "1px solid rgba(247,199,55,0.2)",
                            }
                        },
                    },
                )

    except ImportError:
        # Fallback: render a simple metric-based dashboard
        st.markdown("""
        <div class="section-title animate-in" id="transparansi">
            <h2>Dashboard <span>Impact</span></h2>
        </div>
        <p class="section-subtitle">Distribusi donasi berdasarkan kategori program</p>
        """, unsafe_allow_html=True)

        categories = [
            ("🍚 Pangan", 35, "#f59e0b"),
            ("📚 Pendidikan", 28, "#3b82f6"),
            ("🏥 Kesehatan", 22, "#10b981"),
            ("🆘 Bencana", 10, "#ef4444"),
            ("📦 Lainnya", 5, "#8b5cf6"),
        ]

        cols = st.columns(5)
        for i, (cat, pct, color) in enumerate(categories):
            with cols[i]:
                st.markdown(f"""
                <div class="stat-card animate-in delay-{i+1}">
                    <div style="font-size:1.6rem; margin-bottom:0.4rem;">{cat.split(' ')[0]}</div>
                    <div class="stat-number" style="background:linear-gradient(135deg, {color}, {color}); -webkit-background-clip:text;">{pct}%</div>
                    <div class="stat-label">{cat.split(' ', 1)[1]}</div>
                </div>
                """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════
def render_footer():
    st.markdown("""
    <div class="footer">
        <p>© 2024 <a href="#">DonasiCare</a> – Platform Donasi Terpercaya Indonesia</p>
        <p>Dibuat dengan 💛 untuk Indonesia yang lebih baik</p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# MAIN RENDER
# ═══════════════════════════════════════════════════════════════════════
def main():
    inject_custom_css()
    render_navbar()
    render_hero_banner()
    render_statistics()
    st.markdown("<br>", unsafe_allow_html=True)
    render_popular_programs()
    st.markdown("<br>", unsafe_allow_html=True)
    render_impact_dashboard()
    st.markdown("<br>", unsafe_allow_html=True)
    render_testimonials()
    render_cta()
    render_footer()


main()
