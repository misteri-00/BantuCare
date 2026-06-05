import streamlit as st

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – TENTANG KAMI PAGE
# Profil, Visi Misi, Tim Pengembang, dan Kontak
# ═══════════════════════════════════════════════════════════════════════

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #0a0f1c 0%, #121a2e 50%, #0d1520 100%); }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* ── Header ── */
    .page-header {
        text-align: center;
        margin: 1rem 0 3rem 0;
        animation: fadeIn 0.8s ease;
    }
    .page-header h1 { color: #f1f5f9; font-size: 2.8rem; font-weight: 800; margin-bottom: 0.5rem; }
    .page-header h1 span { background: linear-gradient(135deg, #f7c737, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .page-header p { color: #94a3b8; font-size: 1.1rem; max-width: 600px; margin: 0 auto; }

    /* ── Section Blocks ── */
    .glass-box {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }
    .glass-box:hover {
        border-color: rgba(247, 199, 55, 0.2);
    }
    .glass-box h3 {
        color: #f7c737;
        margin-top: 0;
        margin-bottom: 1rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .glass-box p {
        color: #e2e8f0;
        line-height: 1.7;
        font-size: 0.95rem;
    }

    /* ── Team Cards ── */
    .team-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .team-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 30px rgba(247, 199, 55, 0.1);
        border-color: rgba(247, 199, 55, 0.3);
    }
    .team-avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #f7c737, #f59e0b);
        color: #0f172a;
        font-size: 2rem;
        font-weight: 800;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem auto;
    }
    .team-name { color: #f1f5f9; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.2rem; }
    .team-role { color: #f59e0b; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.8rem; }
    .team-desc { color: #94a3b8; font-size: 0.8rem; line-height: 1.5; }

    /* ── Contact Info ── */
    .contact-item {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 1.2rem;
        color: #e2e8f0;
    }
    .contact-icon {
        width: 45px;
        height: 45px;
        border-radius: 10px;
        background: rgba(247, 199, 55, 0.1);
        color: #f7c737;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)


def main():
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
        <p style="margin-bottom: 1.5rem;">Punya pertanyaan, tawaran kerja sama, atau ingin melaporkan kendala? Jangan ragu untuk menghubungi tim kami.</p>
        
        <div class="contact-item">
            <div class="contact-icon">📧</div>
            <div>
                <strong style="color: #f7c737;">Email</strong><br>
                halo@donasicare.id
            </div>
        </div>
        
        <div class="contact-item">
            <div class="contact-icon">📱</div>
            <div>
                <strong style="color: #f7c737;">WhatsApp / Telepon</strong><br>
                +62 811-1234-5678 (Senin-Jumat, 09.00 - 17.00)
            </div>
        </div>
        
        <div class="contact-item">
            <div class="contact-icon">📍</div>
            <div>
                <strong style="color: #f7c737;">Alamat Kantor</strong><br>
                Gedung Kebaikan Nusantara, Lt. 8<br>
                Jl. Jend. Sudirman Kav. 24, Jakarta Selatan, 12920
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
