import streamlit as st
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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif !important; }
    .stApp { background: linear-gradient(135deg, #0a0f1c 0%, #121a2e 50%, #0d1520 100%); }
    header[data-testid="stHeader"] { background: transparent !important; }

    .page-header {
        text-align: center;
        margin: 1rem 0 3rem 0;
        animation: fadeIn 0.8s ease;
    }
    .page-header h1 { color: #f1f5f9; font-size: 2.8rem; font-weight: 800; margin-bottom: 0.5rem; }
    .page-header h1 span { background: linear-gradient(135deg, #f7c737, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .page-header p { color: #94a3b8; font-size: 1.1rem; }

    .glass-box {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    .glass-box h3 { color: #f7c737; margin-top: 0; margin-bottom: 1rem; }

    .event-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .event-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 10px 30px rgba(247, 199, 55, 0.1);
        border-color: rgba(247, 199, 55, 0.3);
    }
    .event-icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .event-title { color: #f1f5f9; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem; }
    .event-desc { color: #94a3b8; font-size: 0.85rem; line-height: 1.5; margin-bottom: 1rem; flex-grow: 1; }
    .event-meta { font-size: 0.8rem; color: #cbd5e1; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 8px;}

    div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(247, 199, 55, 0.3) !important;
        color: #f1f5f9 !important;
        border-radius: 10px !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)


@st.dialog("Pendaftaran Kegiatan Sosial")
def register_event_dialog(event_name):
    st.markdown(f"### Mendaftar untuk:<br><span style='color:#f7c737;'>{event_name}</span>", unsafe_allow_html=True)
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
            <p style="color:#94a3b8; font-size:0.9rem;">Daftarkan diri Anda untuk berpartisipasi turun langsung ke lapangan.</p>
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
                html_card = f"""
<div class="event-card">
<div class="event-icon">{evt['icon']}</div>
<div class="event-title">{evt['title']}</div>
<div class="event-desc">{evt['desc']}</div>
<div class="event-meta">Tanggal: {evt['date']}</div>
<div class="event-meta">Lokasi: {evt['location']}</div>
<div class="event-meta">Kuota: <span style="color:#f59e0b; font-weight:bold;">{evt['kuota']}</span></div>
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
