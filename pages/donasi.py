import streamlit as st
import time
import datetime
import random
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.campaign import get_all_campaigns, get_campaign_by_id
from utils.helpers import format_rupiah, save_donation

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – DONASI SEKARANG PAGE
# Connected to SQLite database
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
        margin: 1rem 0 2rem 0;
        animation: fadeIn 0.8s ease;
    }
    .page-header h1 { color: #f1f5f9; font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; }
    .page-header h1 span { background: linear-gradient(135deg, #f7c737, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .page-header p { color: #94a3b8; font-size: 1.1rem; }

    /* ── Receipt ── */
    .receipt-box {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 2rem;
        color: #0a0f1c;
        max-width: 500px;
        margin: 2rem auto;
        border-top: 8px solid #f7c737;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        position: relative;
    }
    .receipt-box::before, .receipt-box::after {
        content: "";
        position: absolute;
        top: 0;
        width: 20px;
        height: 20px;
        background: #121a2e;
        border-radius: 50%;
    }
    .receipt-box::before { left: -10px; }
    .receipt-box::after { right: -10px; }
    
    .receipt-header {
        text-align: center;
        border-bottom: 2px dashed #cbd5e1;
        padding-bottom: 1rem;
        margin-bottom: 1rem;
    }
    .receipt-header h2 { color: #0a0f1c; margin: 0; font-weight: 800; font-size: 1.5rem; }
    .receipt-header p { color: #64748b; margin: 5px 0 0 0; font-size: 0.9rem; }
    
    .receipt-row { display: flex; justify-content: space-between; margin-bottom: 0.8rem; font-size: 0.95rem; }
    .receipt-row .label { color: #64748b; }
    .receipt-row .value { font-weight: 700; color: #0f172a; text-align: right; max-width: 60%; }
    
    .receipt-total {
        display: flex;
        justify-content: space-between;
        margin-top: 1.5rem;
        padding-top: 1rem;
        border-top: 2px dashed #cbd5e1;
        font-size: 1.2rem;
        font-weight: 900;
        color: #0f172a;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)


def init_session():
    if 'donation_success' not in st.session_state:
        st.session_state.donation_success = False
    if 'last_receipt' not in st.session_state:
        st.session_state.last_receipt = None


def render_receipt():
    receipt = st.session_state.last_receipt
    if not receipt:
        return

    st.markdown(f"""
    <div class="receipt-box animate-in">
        <div class="receipt-header">
            <h2>BUKTI TRANSAKSI</h2>
            <p>DonasiCare - Terpercaya & Transparan</p>
            <p style="font-size:0.75rem;">{receipt['date']}</p>
        </div>
        <div class="receipt-row">
            <span class="label">ID Transaksi</span>
            <span class="value">{receipt['tx_id']}</span>
        </div>
        <div class="receipt-row">
            <span class="label">Nama Donatur</span>
            <span class="value">{receipt['name']}</span>
        </div>
        <div class="receipt-row">
            <span class="label">Program</span>
            <span class="value">{receipt['program']}</span>
        </div>
        <div class="receipt-row">
            <span class="label">Metode Pembayaran</span>
            <span class="value">{receipt['method']}</span>
        </div>
        <div class="receipt-row">
            <span class="label">Status</span>
            <span class="value" style="color: #10b981;">Berhasil / Terverifikasi</span>
        </div>
        <div class="receipt-total">
            <span>TOTAL</span>
            <span style="color:#f59e0b;">{format_rupiah(receipt['amount'])}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Lihat Riwayat Donasi", use_container_width=True, type="primary"):
            st.session_state.donation_success = False 
            st.switch_page("pages/riwayatdonasi.py")
        if st.button("Donasi Lagi", use_container_width=True):
            st.session_state.donation_success = False
            st.rerun()


def render_form():
    # ── Ambil daftar kampanye dari DB ──
    campaigns = get_all_campaigns()
    if not campaigns:
        st.warning("Belum ada program kampanye yang tersedia.")
        return

    program_names = [c["judul"] for c in campaigns]
    campaign_map = {c["judul"]: c for c in campaigns}
    
    # Pre-select jika dari halaman Program Donasi
    default_idx = 0
    if 'selected_campaign_id' in st.session_state:
        cid = st.session_state.selected_campaign_id
        for i, c in enumerate(campaigns):
            if c["id"] == cid:
                default_idx = i
                break

    st.markdown("<h3 style='color:#f1f5f9; margin-top:0;'>1. Pilih Program Bantuan</h3>", unsafe_allow_html=True)
    selected_program = st.selectbox("Pilih program donasi:", program_names, index=default_idx, label_visibility="collapsed")

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 2rem 0;'>", unsafe_allow_html=True)

    # ── Nominal Donasi ──
    st.markdown("<h3 style='color:#f1f5f9; margin-top:0;'>2. Nominal Donasi</h3>", unsafe_allow_html=True)
    
    if 'nominal' not in st.session_state:
        st.session_state.nominal = 50000

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("Rp 50 Ribu", use_container_width=True): st.session_state.nominal = 50000
    if col2.button("Rp 100 Ribu", use_container_width=True): st.session_state.nominal = 100000
    if col3.button("Rp 250 Ribu", use_container_width=True): st.session_state.nominal = 250000
    if col4.button("Rp 500 Ribu", use_container_width=True): st.session_state.nominal = 500000

    custom_nominal = st.number_input("Atau masukkan nominal lainnya (Rp)", min_value=10000, step=10000, value=st.session_state.nominal)

    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 2rem 0;'>", unsafe_allow_html=True)

    # ── Profil & Metode ──
    st.markdown("<h3 style='color:#f1f5f9; margin-top:0;'>3. Detail Pembayaran</h3>", unsafe_allow_html=True)
    
    donor_name = st.text_input("Nama Lengkap Anda", placeholder="John Doe")
    is_anon = st.checkbox("Sembunyikan nama saya (Donasi sebagai Hamba Allah / Anonim)")
    
    metode_list = ["BCA Virtual Account", "Mandiri Virtual Account", "GoPay", "OVO", "DANA", "QRIS", "Transfer Bank Manual"]
    payment_method = st.selectbox("Metode Pembayaran", metode_list)
    
    uploaded_file = None
    bukti_filename = ""
    if payment_method == "Transfer Bank Manual":
        uploaded_file = st.file_uploader("Upload Bukti Transfer (JPG, PNG, PDF)", type=["jpg", "png", "pdf"])
        if uploaded_file:
            bukti_filename = uploaded_file.name
            st.success("Bukti transfer berhasil diunggah.")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Mulai Donasi", type="primary", use_container_width=True):
        if not is_anon and not donor_name:
            st.error("Silakan masukkan nama Anda atau centang kotak Anonim.")
        elif payment_method == "Transfer Bank Manual" and not uploaded_file:
            st.error("Silakan upload bukti transfer manual Anda.")
        else:
            with st.spinner("Memproses transaksi Anda..."):
                time.sleep(2)
                
                final_name = "Hamba Allah (Anonim)" if is_anon else donor_name
                tx_id = f"TRX-{random.randint(100000, 999999)}"
                dt_now = datetime.datetime.now().strftime("%d %b %Y, %H:%M WIB")

                # Simpan ke database
                selected_campaign = campaign_map[selected_program]
                save_donation(
                    user_id=None,  # Belum ada login
                    campaign_id=selected_campaign["id"],
                    nominal=custom_nominal,
                    metode=payment_method,
                    anonim=is_anon,
                    bukti=bukti_filename,
                    pesan=f"Donasi oleh {final_name}"
                )

                receipt = {
                    "tx_id": tx_id,
                    "name": final_name,
                    "program": selected_program,
                    "amount": custom_nominal,
                    "method": payment_method,
                    "date": dt_now
                }

                # Simpan ke session untuk receipt
                if 'riwayat_donasi' not in st.session_state:
                    st.session_state.riwayat_donasi = []
                st.session_state.riwayat_donasi.append(receipt)
                st.session_state.last_receipt = receipt
                st.session_state.donation_success = True
                
                if 'selected_campaign_id' in st.session_state:
                    del st.session_state['selected_campaign_id']
                    
                st.rerun()


def main():
    inject_custom_css()
    init_session()

    st.markdown("""
    <div class="page-header">
        <h1>Mulai <span>Berdonasi</span></h1>
        <p>Setiap kebaikan Anda adalah harapan baru bagi mereka</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.donation_success:
        st.balloons()
        render_receipt()
    else:
        render_form()


if __name__ == "__main__":
    main()
