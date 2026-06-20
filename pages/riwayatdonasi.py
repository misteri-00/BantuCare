import streamlit as st
from utils.navbar_dark import render_navbar
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.helpers import format_rupiah, get_all_donations

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – RIWAYAT DONASI · Forest Luxury Theme
# ═══════════════════════════════════════════════════════════════════════

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp {
    background: linear-gradient(160deg, #111c11 0%, #0a140a 55%, #101a10 100%) !important;
    min-height: 100vh;
}
header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, .stDeployButton { display: none !important; visibility: hidden !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #2d4a2d; border-radius: 4px; }

/* ── Page Header ── */
.rd-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
}
.rd-header .eyebrow {
    font-size: .68rem; font-weight: 700; letter-spacing: .14em;
    text-transform: uppercase; color: #c9a84c; display: block; margin-bottom: .4rem;
}
.rd-header h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.2rem !important; font-weight: 400 !important;
    color: #f0ede6 !important; line-height: 1.15 !important;
    margin: 0 0 .4rem !important;
}
.rd-header h1 em { font-style: italic; color: #e2c97a; }
.rd-header p { color: #6a7a60; font-size: .88rem; margin: 0; max-width: 520px; margin: 0 auto; }

/* ── Page Wrapper ── */
.rd-page { padding: 0 2rem 3rem; max-width: 1000px; margin: 0 auto; }

/* ── Summary Stats ── */
.rd-summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem; }
.rd-sum-card {
    background: rgba(15,25,15,.7);
    border: .5px solid rgba(201,168,76,.15);
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    text-align: center;
    transition: all .3s;
}
.rd-sum-card:hover { transform: translateY(-3px); border-color: rgba(201,168,76,.3); }
.rd-sum-icon { font-size: 1.4rem; margin-bottom: .3rem; display: block; }
.rd-sum-num {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.5rem !important; font-weight: 400 !important;
    color: #e2c97a !important; margin-bottom: .1rem;
}
.rd-sum-label { color: #6a7a60; font-size: .72rem; font-weight: 500; }

/* ── Section Label ── */
.rd-sec-label {
    font-size: .7rem; font-weight: 700; letter-spacing: .12em;
    text-transform: uppercase; color: #c9a84c; margin: 1.5rem 0 .8rem;
}

/* ── Donation Card ── */
.rd-card {
    background: rgba(12,20,12,.65);
    border: .5px solid rgba(201,168,76,.12);
    border-left: 3px solid #c9a84c;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: .75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all .3s;
}
.rd-card:hover {
    border-color: rgba(201,168,76,.3);
    transform: translateX(4px);
    box-shadow: 0 8px 24px rgba(0,0,0,.2);
}
.rd-card-info {}
.rd-card-title {
    color: #f0ede6; font-size: .92rem; font-weight: 600;
    margin-bottom: .35rem;
}
.rd-card-meta {
    color: #6a7a60; font-size: .78rem; line-height: 1.65;
}
.rd-card-meta strong { color: #8a9e80; font-weight: 600; }
.rd-card-right { text-align: right; flex-shrink: 0; }
.rd-card-amount {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.2rem !important; font-weight: 400 !important;
    color: #e2c97a !important; margin-bottom: .3rem;
}
.rd-card-badge {
    display: inline-block;
    background: rgba(74,222,128,.12);
    color: #4ade80;
    padding: .2rem .65rem;
    border-radius: 20px;
    font-size: .68rem; font-weight: 700;
    letter-spacing: .04em;
}

/* ── Empty State ── */
.rd-empty {
    text-align: center;
    padding: 4rem 2rem;
    background: rgba(12,20,12,.5);
    border: .5px dashed rgba(201,168,76,.2);
    border-radius: 18px;
}
.rd-empty-icon { font-size: 3.5rem; margin-bottom: 1rem; display: block; }
.rd-empty h3 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.3rem !important; font-weight: 400 !important;
    color: #f0ede6 !important; margin: 0 0 .4rem !important;
}
.rd-empty p { color: #6a7a60; font-size: .85rem; margin: 0 0 1.5rem; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    border: .5px solid rgba(201,168,76,.35) !important;
    color: #e2c97a !important;
    background: transparent !important;
    font-weight: 600 !important; font-size: .78rem !important;
    padding: .45rem 1rem !important; transition: all .18s !important;
}
.stButton > button:hover {
    background: rgba(201,168,76,.1) !important;
    border-color: rgba(201,168,76,.6) !important;
}
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg,#c9a84c,#a8852c) !important;
    color: #0f1a0f !important; font-weight: 700 !important;
    border: none !important; border-radius: 12px !important;
    padding: .7rem 2rem !important; font-size: .88rem !important;
    box-shadow: 0 6px 22px rgba(201,168,76,.3) !important;
}
</style>
""", unsafe_allow_html=True)


def main():
    render_navbar("riwayat")
    inject_css()

    # ── Header ──
    st.markdown("""
<div class="rd-header">
<span class="eyebrow">DonasiCare · Riwayat</span>
<h1>Riwayat <em>Donasi</em></h1>
<p>Jejak langkah kebaikan yang telah Anda lakukan</p>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="rd-page">', unsafe_allow_html=True)

    # ── Get Data ──
    db_donations = get_all_donations()
    session_donations = st.session_state.get('riwayat_donasi', [])

    all_donations = list(db_donations or []) + list(session_donations or [])

    if not all_donations:
        st.markdown("""
<div class="rd-empty">
<span class="rd-empty-icon">📭</span>
<h3>Belum Ada Riwayat Donasi</h3>
<p>Anda belum melakukan transaksi donasi. Mulailah perjalanan kebaikan Anda hari ini.</p>
</div>
""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.5, 1, 1.5])
        with c2:
            if st.button("💛 Mulai Berdonasi", type="primary", use_container_width=True):
                st.switch_page("pages/donasi.py")
    else:
        # ── Summary Stats ──
        total_amount_db = sum(tx.get('nominal', 0) for tx in (db_donations or []))
        total_amount_ses = sum(tx.get('amount', 0) for tx in (session_donations or []))
        total_amount = total_amount_db + total_amount_ses
        total_count = len(all_donations)

        st.markdown(f"""
<div class="rd-summary">
<div class="rd-sum-card">
<span class="rd-sum-icon">💰</span>
<div class="rd-sum-num">{format_rupiah(total_amount)}</div>
<div class="rd-sum-label">Total Donasi Anda</div>
</div>
<div class="rd-sum-card">
<span class="rd-sum-icon">📋</span>
<div class="rd-sum-num">{total_count}</div>
<div class="rd-sum-label">Total Transaksi</div>
</div>
<div class="rd-sum-card">
<span class="rd-sum-icon">⭐</span>
<div class="rd-sum-num">{"Gold" if total_amount >= 1_000_000 else "Silver" if total_amount >= 500_000 else "Bronze"}</div>
<div class="rd-sum-label">Level Donatur</div>
</div>
</div>
""", unsafe_allow_html=True)

        # ── DB Donations ──
        if db_donations:
            st.markdown('<div class="rd-sec-label">📂 Riwayat Tersimpan</div>', unsafe_allow_html=True)
            for tx in db_donations:
                nama_donatur = "Hamba Allah (Anonim)" if tx.get("anonim") else tx.get("pesan", "Donatur")
                program_judul = tx.get("program_judul", "Program Donasi")
                st.markdown(f"""
<div class="rd-card">
<div class="rd-card-info">
<div class="rd-card-title">{program_judul}</div>
<div class="rd-card-meta">
Donatur: <strong>{nama_donatur}</strong><br>
Metode: {tx.get('metode_pembayaran', '-')} · Tanggal: {tx.get('tanggal_donasi', '-')}
</div>
</div>
<div class="rd-card-right">
<div class="rd-card-amount">{format_rupiah(tx.get('nominal', 0))}</div>
<div class="rd-card-badge">✓ Berhasil</div>
</div>
</div>
""", unsafe_allow_html=True)

        # ── Session Donations ──
        if session_donations:
            st.markdown('<div class="rd-sec-label">⚡ Transaksi Sesi Ini</div>', unsafe_allow_html=True)
            for tx in reversed(session_donations):
                st.markdown(f"""
<div class="rd-card">
<div class="rd-card-info">
<div class="rd-card-title">{tx['program']}</div>
<div class="rd-card-meta">
ID: <strong>{tx['tx_id']}</strong><br>
Metode: {tx['method']} · Tanggal: {tx['date']}
</div>
</div>
<div class="rd-card-right">
<div class="rd-card-amount">{format_rupiah(tx['amount'])}</div>
<div class="rd-card-badge">✓ Berhasil</div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # close rd-page


if __name__ == "__main__":
    main()
