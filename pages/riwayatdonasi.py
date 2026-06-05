import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.helpers import format_rupiah, get_all_donations

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – RIWAYAT DONASI PAGE
# Connected to SQLite: Menampilkan transaksi dari tabel donations
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

    .history-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(247, 199, 55, 0.3);
        border-left: 5px solid #f7c737;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.3s ease;
    }
    .history-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .history-info h4 { color: #f1f5f9; margin: 0 0 0.5rem 0; font-size: 1.1rem; }
    .history-meta { color: #94a3b8; font-size: 0.85rem; margin: 0; line-height: 1.5; }
    
    .history-amount { text-align: right; }
    .amount-value { font-size: 1.4rem; font-weight: 800; color: #10b981; }
    .status-badge { 
        display: inline-block; 
        background: rgba(16, 185, 129, 0.2); 
        color: #34d399; 
        padding: 0.2rem 0.6rem; 
        border-radius: 20px; 
        font-size: 0.75rem; 
        font-weight: 600;
        margin-top: 0.5rem;
    }

    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: rgba(30, 41, 59, 0.3);
        border-radius: 16px;
        border: 1px dashed rgba(255,255,255,0.2);
    }
    .empty-state h3 { color: #f1f5f9; }
    .empty-state p { color: #94a3b8; margin-bottom: 1.5rem; }

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
        <h1>Riwayat <span>Donasi</span></h1>
        <p>Jejak langkah kebaikan yang telah Anda lakukan</p>
    </div>
    """, unsafe_allow_html=True)

    # Ambil riwayat dari database
    db_donations = get_all_donations()
    
    # Gabungkan juga riwayat dari session (untuk transaksi yang baru saja dilakukan)
    session_donations = st.session_state.get('riwayat_donasi', [])

    if not db_donations and not session_donations:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📭</div>
            <h3>Belum ada riwayat donasi</h3>
            <p>Anda belum melakukan transaksi donasi.</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Mulai Berdonasi", type="primary", use_container_width=True):
                st.switch_page("pages/donasi.py")
    else:
        # Tampilkan dari database (terbaru di atas)
        if db_donations:
            st.markdown("<h4 style='color:#f1f5f9;'>Riwayat Tersimpan di Database</h4>", unsafe_allow_html=True)
            for tx in db_donations:
                nama_donatur = "Hamba Allah (Anonim)" if tx.get("anonim") else tx.get("pesan", "Donatur")
                program_judul = tx.get("program_judul", "Program Donasi")
                st.markdown(f"""
                <div class="history-card">
                    <div class="history-info">
                        <h4>{program_judul}</h4>
                        <p class="history-meta">
                            Donatur: <b>{nama_donatur}</b><br>
                            Metode: {tx.get('metode_pembayaran', '-')}<br>
                            Tanggal: {tx.get('tanggal_donasi', '-')}
                        </p>
                    </div>
                    <div class="history-amount">
                        <div class="amount-value">{format_rupiah(tx.get('nominal', 0))}</div>
                        <div class="status-badge">Berhasil</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Tampilkan dari session (transaksi saat ini)
        if session_donations:
            st.markdown("<h4 style='color:#f1f5f9; margin-top:2rem;'>Transaksi Sesi Ini</h4>", unsafe_allow_html=True)
            for tx in reversed(session_donations):
                st.markdown(f"""
                <div class="history-card">
                    <div class="history-info">
                        <h4>{tx['program']}</h4>
                        <p class="history-meta">
                            ID: <b>{tx['tx_id']}</b><br>
                            Metode: {tx['method']}<br>
                            Tanggal: {tx['date']}
                        </p>
                    </div>
                    <div class="history-amount">
                        <div class="amount-value">{format_rupiah(tx['amount'])}</div>
                        <div class="status-badge">Berhasil</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
