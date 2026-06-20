import streamlit as st
from utils.navbar_dark import render_navbar
import time
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.volunteer import register_volunteer, get_volunteer_count

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – VOLUNTEER PAGE
# Connected to SQLite: Daftar Relawan, Event Sosial, Pendaftaran
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

    div[data-baseweb="tab-list"] {
        gap: 8px !important;
        background: rgba(12, 20, 12, 0.6) !important;
        padding: 6px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(247, 199, 55, 0.1) !important;
        justify-content: center;
        margin-bottom: 2rem;
    }
    div[data-baseweb="tab"] {
        color: #8a9e80 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        padding: 0.8rem 2rem !important;
        border: none !important;
    }
    div[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(247, 199, 55, 0.15), rgba(245, 158, 11, 0.05)) !important;
        color: #e2c97a !important;
        box-shadow: inset 0 0 0 1px rgba(247, 199, 55, 0.4) !important;
    }

    .glass-box {
        background: rgba(20, 30, 20, 0.4);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    .glass-box h3 {
        font-family: 'DM Serif Display', serif !important;
        color: #e2c97a;
        font-size: 1.8rem;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-weight: 400;
    }

    .event-card {
        background: rgba(12, 20, 12, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 16px;
        padding: 1.8rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        position: relative;
        overflow: hidden;
    }
    .event-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #e2c97a, #c9a84c);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .event-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(247, 199, 55, 0.1);
        border-color: rgba(247, 199, 55, 0.3);
    }
    .event-card:hover::before { opacity: 1; }
    
    .event-icon {
        font-size: 3rem;
        margin-bottom: 1.2rem;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));
    }
    .event-title {
        color: #f0ede6;
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 0.8rem;
        line-height: 1.3;
    }
    .event-desc {
        color: #8a9e80;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        flex-grow: 1;
    }
    .event-meta {
        font-size: 0.85rem;
        color: #a0b098;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 0.5rem;
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
    }
    
    .kuota-mendesak { color: #ef4444; font-weight: 700; animation: pulse 2s infinite; text-shadow: 0 0 10px rgba(239, 68, 68, 0.4); }
    .kuota-aman { color: #10b981; font-weight: 700; }

    div[data-testid="stTextInput"] input, 
    div[data-testid="stMultiSelect"] > div {
        background-color: rgba(12, 20, 12, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f0ede6 !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #e2c97a !important;
        box-shadow: 0 0 0 2px rgba(247, 199, 55, 0.2) !important;
        background-color: rgba(12, 20, 12, 0.8) !important;
    }
    
    button[kind="primary"] {
        background: linear-gradient(135deg, #e2c97a, #c9a84c) !important;
        color: #0a140a !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(247, 199, 55, 0.3) !important;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    </style>
    """, unsafe_allow_html=True)


@st.dialog("Pendaftaran Kegiatan Sosial")
def register_event_dialog(event_name):
    st.markdown(f"### Mendaftar untuk:<br><span style='color:#e2c97a;'>{event_name}</span>", unsafe_allow_html=True)
    st.write("Silakan isi formulir di bawah ini untuk mengonfirmasi kehadiran Anda pada event sosial ini.")
    
    nama = st.text_input("Nama Lengkap", key=f"nama_{event_name}")
    no_hp = st.text_input("No. WhatsApp", key=f"hp_{event_name}")
    email = st.text_input("Email", key=f"email_{event_name}")
    
    if st.button("Kirim Pendaftaran", use_container_width=True, type="primary"):
        if nama and no_hp and email:
            with st.spinner("Memproses pendaftaran..."):
                # Simpan ke database
                register_volunteer(nama, email, no_hp, event_name)
                time.sleep(1)
                st.success("Pendaftaran berhasil! Data Anda telah tersimpan di sistem kami.")
                time.sleep(2)
                st.rerun()
        else:
            st.error("Harap isi Nama, No. WhatsApp, dan Email.")


def main():
    render_navbar("volunteer")
    inject_custom_css()

    vol_count = get_volunteer_count()

    st.markdown(f"""
    <div class="page-header">
        <h1>Pusat <span>Volunteer</span></h1>
        <p>Sudah {vol_count} relawan bergabung. Aksi nyata lebih berharga!</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Event Sosial", "Pendaftaran Anggota Relawan"])

    with tab1:
        st.markdown("""
        <div class="glass-box" style="padding: 1.5rem;">
            <h3>Event Sosial Terdekat</h3>
            <p style="color:#8a9e80; font-size:0.9rem;">Daftarkan diri Anda untuk berpartisipasi turun langsung ke lapangan.</p>
        </div>
        """, unsafe_allow_html=True)

        events = [
            {
                "id": "evt_1",
                "icon": "🌳",
                "title": "Penanaman 1.000 Pohon Mangrove",
                "desc": "Bantu kami menanam bibit mangrove untuk menyelamatkan pesisir pantai utara dari abrasi.",
                "date": "24 Juni 2026",
                "location": "Pantai Indah Kapuk, Jakarta",
                "kuota": "Tersisa 15 Kuota"
            },
            {
                "id": "evt_2",
                "icon": "📚",
                "title": "Mengajar Anak Panti Asuhan",
                "desc": "Program kelas inspirasi sehari mengajar matematika dasar dan bahasa Inggris untuk anak yatim.",
                "date": "10 Juli 2026",
                "location": "Panti Asuhan Kasih Bunda, Depok",
                "kuota": "Tersisa 5 Kuota"
            },
            {
                "id": "evt_3",
                "icon": "🆘",
                "title": "Bantuan Distribusi Sembako Bencana",
                "desc": "Membantu proses pengepakan dan penyaluran sembako darurat untuk korban banjir bandang.",
                "date": "Akhir Pekan Ini",
                "location": "Gudang Logistik DonasiCare, Bekasi",
                "kuota": "Dibutuhkan Mendesak!"
            }
        ]

        cols = st.columns(3)
        for idx, evt in enumerate(events):
            with cols[idx]:
                kuota_class = "kuota-mendesak" if "Mendesak" in evt['kuota'] else "kuota-aman"
                html_card = f"""
<div class="event-card">
<div class="event-icon">{evt['icon']}</div>
<div class="event-title">{evt['title']}</div>
<div class="event-desc">{evt['desc']}</div>
<div class="event-meta"><span>📅</span> <span>{evt['date']}</span></div>
<div class="event-meta"><span>📍</span> <span>{evt['location']}</span></div>
<div class="event-meta"><span>👥</span> <span>Kuota: <span class="{kuota_class}">{evt['kuota']}</span></span></div>
</div>
<br>
"""
                st.markdown(html_card, unsafe_allow_html=True)

                if st.button("Ikut Kegiatan Ini", key=evt['id'], use_container_width=True):
                    register_event_dialog(evt['title'])


    with tab2:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown("<h3>Daftar Menjadi Anggota Relawan Inti</h3>", unsafe_allow_html=True)
        st.write("Dapatkan informasi prioritas setiap kali ada event sosial baru.")
        
        with st.form("form_relawan"):
            col1, col2 = st.columns(2)
            with col1:
                nama_lengkap = st.text_input("Nama Lengkap")
                email = st.text_input("Alamat Email")
            with col2:
                no_hp = st.text_input("No. WhatsApp")
                domisili = st.text_input("Kota Domisili")
                
            minat = st.multiselect("Area Minat Volunteer", 
                                   ["Pendidikan & Pengajaran", "Kesehatan & Medis", "Lingkungan", "Logistik & Distribusi", "Dokumentasi & Media"])
            
            submit = st.form_submit_button("Daftar Menjadi Relawan", type="primary", use_container_width=True)
            if submit:
                if nama_lengkap and email and no_hp:
                    # Simpan ke database
                    minat_str = ", ".join(minat) if minat else "Umum"
                    register_volunteer(nama_lengkap, email, no_hp, f"Relawan Inti - {minat_str}")
                    st.success("Pendaftaran berhasil! Profil Anda telah tersimpan di database relawan kami.")
                else:
                    st.error("Mohon lengkapi Nama, Email, dan No. WhatsApp.")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
