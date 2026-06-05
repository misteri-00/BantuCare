from utils.database import get_connection

# ═══════════════════════════════════════════════════════════════════════
# Chatbot helpers
# ═══════════════════════════════════════════════════════════════════════

def get_response(message):
    """Respons sederhana berbasis keyword (fungsi asli user)."""
    message = message.lower()

    if "banjir" in message:
        return "Saya merekomendasikan program Peduli Banjir Jawa Barat."
    elif "pendidikan" in message:
        return "Saya merekomendasikan program Beasiswa Indonesia."
    elif "kesehatan" in message:
        return "Saya merekomendasikan program Bantuan Kesehatan."
    elif "cara donasi" in message:
        return "Pilih program kemudian klik tombol Donasi Sekarang."

    return "Maaf, saya belum memahami pertanyaan tersebut."


def save_chat(user_id, pertanyaan, jawaban):
    """Simpan riwayat percakapan chatbot ke database."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO chatbot_history (user_id, pertanyaan, jawaban) VALUES (?, ?, ?)",
        (user_id, pertanyaan, jawaban)
    )
    conn.commit()
    conn.close()


def get_chat_history(user_id=None):
    """Ambil riwayat chatbot, opsional filter berdasarkan user."""
    conn = get_connection()
    if user_id:
        rows = conn.execute(
            "SELECT * FROM chatbot_history WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM chatbot_history ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]