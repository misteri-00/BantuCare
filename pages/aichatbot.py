import streamlit as st
import time
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.chatbot import save_chat, get_chat_history
from utils.recommendation import get_recommendations
from utils.helpers import format_rupiah, calc_progress
from utils.campaign import get_all_campaigns

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – AI ASSISTANT PAGE
# Connected to SQLite: Chatbot history, Rekomendasi dari DB, Generator
# ═══════════════════════════════════════════════════════════════════════

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #0a0f1c 0%, #121a2e 50%, #0d1520 100%); }
    header[data-testid="stHeader"] { background: transparent !important; }

    .page-header {
        text-align: center;
        margin: 1rem 0 2rem 0;
        animation: fadeIn 0.8s ease;
    }
    .page-header h1 { color: #f1f5f9; font-size: 2.8rem; font-weight: 800; margin-bottom: 0.5rem; }
    .page-header h1 span { background: linear-gradient(135deg, #f7c737, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .page-header p { color: #94a3b8; font-size: 1.1rem; }

    div[data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(30, 41, 59, 0.4);
        padding: 0.5rem 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    div[data-baseweb="tab"] {
        color: #94a3b8 !important;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    div[data-baseweb="tab"][aria-selected="true"] {
        background: rgba(247, 199, 55, 0.15) !important;
        color: #f7c737 !important;
    }
    div[data-baseweb="tab-highlight"] { display: none; }

    .ai-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1rem;
    }
    .ai-card h3 { color: #f7c737; margin-top: 0; }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)


def tab_chatbot():
    st.markdown("""
    <div class="ai-card">
        <h3>Chatbot DonasiCare</h3>
        <p style="color:#94a3b8;">Tanyakan apa saja tentang penyaluran donasi, transparansi, atau cara berpartisipasi.</p>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Halo! Saya AI Assistant DonasiCare. Ada yang bisa saya bantu terkait program donasi hari ini?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Tulis pertanyaan Anda di sini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Berpikir..."):
                time.sleep(1)
                
                # Cari konteks dari database kampanye
                campaigns = get_all_campaigns()
                campaign_info = ", ".join([f"{c['judul']} ({c['kategori']})" for c in campaigns[:5]])
                
                response = (
                    f"Terima kasih atas pertanyaannya! "
                    f"Saat ini kami memiliki {len(campaigns)} program aktif, antara lain: {campaign_info}. "
                    f"Kami memastikan transparansi dana 100% dan Anda dapat melihat laporannya secara real-time di menu Transparansi. "
                    f"Anda juga bisa berdonasi melalui dompet digital atau transfer bank di halaman Donasi Sekarang."
                )
                st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Simpan ke database
        save_chat(user_id=None, pertanyaan=prompt, jawaban=response)


def tab_recommendation():
    st.markdown("""
    <div class="ai-card">
        <h3>Rekomendasi Berdasarkan Minat</h3>
        <p style="color:#94a3b8;">AI akan mencocokkan program donasi dari database yang paling berdampak sesuai dengan preferensi Anda.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    minat = st.multiselect("Pilih area yang paling Anda pedulikan:", 
                           ["Pendidikan Anak", "Kesehatan & Medis", "Pelestarian Lingkungan", "Pemberdayaan Ekonomi", "Bantuan Bencana Alam"])
    budget = st.selectbox("Rentang donasi per bulan (opsional):", ["< Rp 50.000", "Rp 50.000 - Rp 200.000", "> Rp 200.000"])

    if st.button("Generate Rekomendasi", type="primary"):
        if not minat:
            st.warning("Silakan pilih minimal satu minat terlebih dahulu.")
        else:
            with st.spinner("AI sedang menganalisis program terbaik untuk Anda..."):
                time.sleep(1.5)
                
                # Ambil rekomendasi dari database
                results = get_recommendations(minat)
                
                if results:
                    st.success(f"Ditemukan {len(results)} program yang cocok dengan minat Anda!")
                    for r in results:
                        progress = calc_progress(r["dana_terkumpul"], r["target_dana"])
                        st.markdown(f"""
                        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                            <h4 style="color:#34d399; margin-top:0;">{r['judul']}</h4>
                            <p style="color:#e2e8f0;">{r['deskripsi']}</p>
                            <p style="color:#94a3b8; font-size:0.85rem;">Kategori: <b>{r['kategori']}</b> | Lokasi: <b>{r.get('lokasi', '-')}</b></p>
                            <p style="color:#f7c737; font-size:0.9rem;">Terkumpul: <b>{format_rupiah(r['dana_terkumpul'])}</b> dari {format_rupiah(r['target_dana'])} ({progress}%)</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Belum ada program yang cocok. Coba pilih area minat lain.")


def tab_education():
    st.markdown("""
    <div class="ai-card">
        <h3>Edukasi Sosial & Dampak</h3>
        <p style="color:#94a3b8;">Dapatkan wawasan berbasis data tentang isu sosial dan bagaimana donasi skala kecil berdampak besar.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("Mengapa Pendidikan Anak Pelosok Sangat Krusial?"):
        st.write("""
        Menurut data analisis AI kami tahun 2023, anak di daerah terpencil memiliki tingkat putus sekolah 3x lebih tinggi. 
        Donasi sebesar Rp 150.000 dapat menutup kebutuhan nutrisi dan buku mereka selama sebulan penuh.
        Pendidikan memutus rantai kemiskinan dengan efektivitas hingga **68%** dalam satu generasi.
        """)
        
    with st.expander("Dampak Reboisasi Hutan Bakau (Mangrove)"):
        st.write("""
        1 Hektar hutan Mangrove dapat menyerap emisi karbon 4x lebih banyak dari hutan tropis biasa. 
        Program donasi lingkungan di DonasiCare memfokuskan pada pesisir yang terancam abrasi, menyelamatkan ekosistem biota laut sekaligus tempat tinggal nelayan.
        """)

    with st.expander("Transparansi Dana Menggunakan Teknologi"):
        st.write("""
        Setiap aliran dana donasi dianalisis menggunakan sistem cerdas kami untuk memastikan tidak ada biaya overhead tersembunyi.
        Laporan dikirim otomatis tiap akhir bulan dengan rincian pembelian barang hingga ke tangan penerima manfaat.
        """)


def tab_generator():
    st.markdown("""
    <div class="ai-card">
        <h3>Generator Kampanye AI</h3>
        <p style="color:#94a3b8;">Membantu relawan dan NGO membuat deskripsi kampanye yang menggugah empati dalam hitungan detik.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        judul_tujuan = st.text_input("Judul / Tujuan Kampanye", placeholder="Contoh: Bantuan Air Bersih Gunung Kidul")
        target_penerima = st.text_input("Target Penerima", placeholder="Contoh: 50 Kepala Keluarga di Desa X")
    with col2:
        kategori_gen = st.selectbox("Kategori", ["Kesehatan", "Lingkungan", "Pendidikan", "Kemanusiaan"])
        target_dana = st.number_input("Target Dana (Rp)", min_value=1000000, step=500000)

    if st.button("Generate Deskripsi", type="primary"):
        if not judul_tujuan or not target_penerima:
            st.error("Lengkapi judul dan target penerima terlebih dahulu.")
        else:
            with st.spinner("AI sedang merangkai kata-kata yang menyentuh hati..."):
                time.sleep(2)
                generated_text = f"""
**{judul_tujuan.upper()}**

Bayangkan jika setiap tetes air yang kita minum adalah hasil perjuangan berjam-jam. Di sisi lain negeri kita, {target_penerima} sedang berjuang menghadapi krisis harian yang mengancam {kategori_gen.lower()} mereka.

Mereka tidak meminta banyak, hanya uluran tangan kecil dari kita untuk bisa hidup lebih layak. 

Dengan target pengumpulan dana sebesar **{format_rupiah(target_dana)}**, setiap rupiah yang Anda sisihkan akan diwujudkan langsung menjadi solusi nyata untuk merubah masa depan mereka. 

Mari bersama menjadi alasan mereka tersenyum hari ini. Bantuan Anda adalah harapan terbesar mereka!
"""
                st.success("Deskripsi berhasil dibuat!")
                st.text_area("Hasil Generate (Bisa disalin):", value=generated_text, height=250)


def main():
    inject_custom_css()
    
    st.markdown("""
    <div class="page-header">
        <h1><span>AI</span> Assistant</h1>
        <p>Pendamping cerdas Anda untuk perjalanan donasi yang lebih bermakna</p>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs([
        "Chatbot Donasi", 
        "Rekomendasi Minat", 
        "Edukasi & Dampak", 
        "Generator Kampanye"
    ])

    with t1:
        tab_chatbot()
    with t2:
        tab_recommendation()
    with t3:
        tab_education()
    with t4:
        tab_generator()


if __name__ == "__main__":
    main()
