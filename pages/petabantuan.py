import streamlit as st
import pandas as pd

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

    .card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 1rem;
        color: #f1f5f9;
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
        <h1><span>Peta</span> Bantuan</h1>
        <p>Sebaran lokasi program donasi dan penerima bantuan di seluruh Indonesia</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>📍 Titik Penyaluran Bantuan</h3>
        <p style="color:#94a3b8;">Peta di bawah ini menunjukkan lokasi-lokasi di mana DonasiCare telah menyalurkan bantuan kepada yang membutuhkan. Setiap titik merepresentasikan satu area program aktif atau yang telah selesai.</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

    # Data dummy lokasi bantuan di Indonesia
    data_lokasi = pd.DataFrame({
        'latitude': [-6.2088, -7.2504, -6.9175, 3.5952, -5.1477, -7.7956, -0.9471, -3.3167, 1.4748, -8.6500],
        'longitude': [106.8456, 112.7688, 107.6191, 98.6722, 119.4327, 110.3695, 100.3658, 114.5901, 124.8421, 115.2167],
        'kota': ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Makassar', 'Yogyakarta', 'Padang', 'Banjarmasin', 'Manado', 'Denpasar'],
        'bantuan': ['Pendidikan', 'Kesehatan', 'Lingkungan', 'Bencana Alam', 'Pemberdayaan', 'Pendidikan', 'Bencana Alam', 'Kesehatan', 'Lingkungan', 'Pemberdayaan']
    })

    # Filter berdasarkan kategori
    kategori_pilihan = st.selectbox("Filter berdasarkan Kategori Bantuan:", 
                                    ["Semua Kategori", "Pendidikan", "Kesehatan", "Lingkungan", "Bencana Alam", "Pemberdayaan"])
    
    if kategori_pilihan != "Semua Kategori":
        data_tampil = data_lokasi[data_lokasi['bantuan'] == kategori_pilihan]
    else:
        data_tampil = data_lokasi

    # Tampilkan peta
    if not data_tampil.empty:
        st.map(data_tampil, zoom=4)
        
        st.markdown(f"**Menampilkan {len(data_tampil)} titik penyaluran bantuan.**")
        
        # Tampilkan detail dalam bentuk tabel sederhana
        with st.expander("Lihat Detail Lokasi"):
            st.dataframe(data_tampil[['kota', 'bantuan']], use_container_width=True)
    else:
        st.warning("Belum ada data untuk kategori ini.")

if __name__ == "__main__":
    main()
