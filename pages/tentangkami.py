import streamlit as st
from utils.navbar_dark import render_navbar

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – TENTANG KAMI PAGE
# Profil, Visi Misi, Tim Pengembang, dan Kontak
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

    /* ── Header ── */
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

    /* ── Section Blocks ── */
    .glass-box {
        background: rgba(20, 30, 20, 0.4);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .glass-box:hover {
        border-color: rgba(201, 168, 76, 0.25);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3), 0 0 20px rgba(201, 168, 76, 0.05);
        transform: translateY(-4px);
    }
    .glass-box h3 {
        font-family: 'DM Serif Display', serif !important;
        color: #e2c97a;
        font-size: 1.8rem;
        margin-top: 0;
        margin-bottom: 1rem;
        font-weight: 400;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .glass-box p {
        color: #a0b098;
        line-height: 1.7;
        font-size: 0.95rem;
    }

    /* ── Team Cards ── */
    .team-card {
        background: rgba(12, 20, 12, 0.65);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .team-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #e2c97a, #c9a84c);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .team-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px rgba(201, 168, 76, 0.1);
        border-color: rgba(201, 168, 76, 0.3);
    }
    .team-card:hover::before { opacity: 1; }
    
    .team-avatar {
        width: 85px;
        height: 85px;
        border-radius: 50%;
        background: linear-gradient(135deg, #e2c97a, #c9a84c);
        color: #0a140a;
        font-size: 2.2rem;
        font-family: 'DM Serif Display', serif !important;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1.2rem auto;
        box-shadow: 0 8px 20px rgba(201, 168, 76, 0.3);
        transition: transform 0.3s ease;
    }
    .team-card:hover .team-avatar { transform: scale(1.1); }
    .team-name { color: #f0ede6; font-weight: 700; font-size: 1.25rem; margin-bottom: 0.2rem; }
    .team-role { color: #c9a84c; font-size: 0.9rem; font-weight: 600; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px;}
    .team-desc { color: #8a9e80; font-size: 0.9rem; line-height: 1.6; }

    /* ── Contact Info ── */
    .contact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-top: 1.5rem;
    }
    .contact-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        background: rgba(12, 20, 12, 0.5);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.03);
        transition: transform 0.3s ease;
    }
    .contact-item:hover {
        transform: translateY(-4px);
        border-color: rgba(201, 168, 76, 0.2);
    }
    .contact-icon {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(201, 168, 76, 0.15), rgba(201, 168, 76, 0.05));
        color: #e2c97a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: inset 0 0 0 1px rgba(201, 168, 76, 0.3);
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    render_navbar("tentangkami")
    inject_custom_css()

    st.markdown("""
    <div class="page-header">
        <h1>Tentang <span>Kami</span></h1>
        <p>Mengenal lebih dekat siapa kami, tujuan kami, dan orang-orang di balik DonasiCare AI.</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. Profil DonasiCare AI
    st.markdown("""
    <div class="glass-box">
        <h3>🤖 Profil DonasiCare AI</h3>
        <p><b>DonasiCare AI</b> adalah platform filantropi modern berbasis kecerdasan buatan pertama di Indonesia. Kami mengombinasikan empati kemanusiaan dengan teknologi mutakhir untuk memastikan setiap rupiah donasi disalurkan secara transparan, tepat sasaran, dan membawa dampak terukur.</p>
        <p>Diluncurkan pada tahun 2024, sistem AI kami mampu menganalisis ribuan data masyarakat pra-sejahtera, mengkategorikan urgensi bantuan, dan mencocokkan donatur dengan program yang paling sesuai dengan kepedulian mereka. Dengan DonasiCare, berbuat baik menjadi lebih mudah, aman, dan berdampak nyata.</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Visi dan Misi
    col_visi, col_misi = st.columns(2)
    with col_visi:
        st.markdown("""
        <div class="glass-box" style="height: 100%;">
            <h3>👁️ Visi</h3>
            <p>Menjadi ekosistem kebaikan digital terbesar di Asia Tenggara yang menghubungkan jutaan orang baik melalui transparansi penuh, inovasi AI, dan kepedulian tanpa batas, untuk mengentaskan kemiskinan dan ketidaksetaraan.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_misi:
        st.markdown("""
        <div class="glass-box" style="height: 100%;">
            <h3>🚀 Misi</h3>
            <ul style="color: #e2e8f0; line-height: 1.7; font-size: 0.95rem; padding-left: 20px;">
                <li>Membangun platform donasi yang 100% transparan dan bebas potongan tersembunyi.</li>
                <li>Memanfaatkan AI untuk menyalurkan bantuan dengan tingkat akurasi dan urgensi maksimal.</li>
                <li>Membangun komunitas donatur dan relawan yang teredukasi terkait isu-isu sosial.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Tim Pengembang
    st.markdown("<h3 style='text-align:center; color:#f1f5f9; margin-bottom: 2rem;'>Tim Pengembang Kami</h3>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    
    with t1:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">AK</div>
            <div class="team-name">Adi K.</div>
            <div class="team-role">Founder & CEO</div>
            <div class="team-desc">Penggagas DonasiCare dengan pengalaman 10 tahun di NGO sosial dan teknologi.</div>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">NR</div>
            <div class="team-name">Nadia R.</div>
            <div class="team-role">Head of AI & Data</div>
            <div class="team-desc">Pakar machine learning yang memastikan algoritma rekomendasi berjalan transparan & adil.</div>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="team-card">
            <div class="team-avatar">BS</div>
            <div class="team-name">Bima S.</div>
            <div class="team-role">Community Manager</div>
            <div class="team-desc">Penghubung utama antara relawan lapangan, yayasan partner, dan donatur setia.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 4. Kontak
    st.markdown("""
    <div class="glass-box">
        <h3>📞 Hubungi Kami</h3>
        <p>Punya pertanyaan, tawaran kerja sama, atau ingin melaporkan kendala? Jangan ragu untuk menghubungi tim kami.</p>
        
        <div class="contact-grid">
            <div class="contact-item">
                <div class="contact-icon">📧</div>
                <strong style="color: #f0ede6; font-size: 1.1rem; margin-bottom: 0.2rem;">Email</strong>
                <span style="color: #8a9e80; font-size: 0.9rem;">halo@donasicare.id</span>
            </div>
            
            <div class="contact-item">
                <div class="contact-icon">📱</div>
                <strong style="color: #f0ede6; font-size: 1.1rem; margin-bottom: 0.2rem;">WhatsApp</strong>
                <span style="color: #8a9e80; font-size: 0.9rem;">+62 811-1234-5678</span>
            </div>
            
            <div class="contact-item">
                <div class="contact-icon">📍</div>
                <strong style="color: #f0ede6; font-size: 1.1rem; margin-bottom: 0.2rem;">Kantor Pusat</strong>
                <span style="color: #8a9e80; font-size: 0.9rem;">Gedung Kebaikan Nusantara<br>Jl. Jend. Sudirman Kav. 24, Jakarta</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
