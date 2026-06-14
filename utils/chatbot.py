import re
import time
import random
import datetime
from utils.campaign import get_all_campaigns, get_total_donasi, get_campaign_count, get_campaigns_by_category
from utils.helpers import format_rupiah, get_donation_count

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – Smart Chatbot Engine (Pure Python, No External API)
# Features: Intent classification, sentiment detection, context memory,
#           randomized natural responses, campaign data integration
# ═══════════════════════════════════════════════════════════════════════

DETAILED_PROGRAMS = {
    "banjir_demak": {
        "id": "banjir_demak",
        "judul": "Banjir Demak 2026",
        "kategori": "Bencana Alam",
        "tanggal_kejadian": "5 Juni 2026",
        "waktu_kejadian": "02.15 WIB",
        "deskripsi": "Banjir terjadi akibat curah hujan tinggi dan meluapnya Sungai Wulan yang menyebabkan genangan di beberapa wilayah Kabupaten Demak. Curah hujan ekstrem berlangsung selama kurang lebih 8 jam.",
        "wilayah_terdampak": ["Kecamatan Karanganyar", "Kecamatan Gajah", "Kecamatan Sayung", "Kecamatan Bonang", "Kecamatan Mijen"],
        "detail_wilayah": "37 desa terdampak dengan ketinggian air 30 cm hingga 150 cm. Luas wilayah terdampak diperkirakan mencapai 1.250 hektar.",
        "jumlah_jiwa": 3240,
        "jumlah_keluarga": 815,
        "detail_korban": "Di antaranya:\n👶 412 anak-anak\n👵 156 lansia\n🤰 48 ibu hamil\n🤕 17 korban luka ringan\n🚑 3 korban luka berat\nSaat ini sebagian warga masih berada di lokasi pengungsian.",
        "kebutuhan": ["🍚 Makanan siap saji", "💧 Air bersih", "👶 Susu dan perlengkapan bayi", "🛏️ Selimut dan tikar", "🧼 Paket kebersihan", "📚 Perlengkapan sekolah anak-anak"],
        "dampak_100k": "🍚 Paket makanan untuk 2 keluarga\n💧 Air bersih untuk 20 orang\n🧼 Paket kebersihan darurat untuk 2 keluarga",
        "dampak_500k": "🍚 Paket makanan untuk 10 keluarga\n💧 Air bersih untuk 100 orang\n🧼 Paket kebersihan darurat untuk 10 keluarga"
    },
    "pendidikan": {
        "id": "pendidikan",
        "judul": "Program Beasiswa Anak Indonesia",
        "kategori": "Pendidikan",
        "deskripsi": "Program ini membantu anak-anak dari keluarga kurang mampu agar tetap dapat melanjutkan pendidikan.",
        "wilayah_terdampak": ["Jawa Tengah", "Jawa Barat", "Nusa Tenggara Timur"],
        "detail_wilayah": "42 sekolah",
        "jumlah_jiwa": 850,
        "detail_korban": "👨‍🎓 850 siswa aktif\n📚 320 siswa SD\n📖 290 siswa SMP\n🎓 240 siswa SMA\nMayoritas berasal dari keluarga dengan penghasilan di bawah UMR daerah setempat.",
        "dampak_100k": "✅ 10 buku tulis\n✅ 20 pensil\n✅ 10 pulpen\n✅ 5 penghapus\n✅ 2 kotak pensil\natau\n🎒 Mendukung perlengkapan belajar 1 siswa selama beberapa minggu.",
        "dampak_500k": "✅ 50 buku tulis\n✅ 100 pensil\n✅ 25 pulpen\n✅ 10 penggaris\n✅ 5 tas sekolah\n✅ 5 paket alat tulis lengkap"
    },
    "kesehatan": {
        "id": "kesehatan",
        "judul": "Program Bantuan Pengobatan Pasien Tidak Mampu",
        "kategori": "Kesehatan",
        "deskripsi": "Program ini membantu masyarakat yang kesulitan mendapatkan akses layanan kesehatan.",
        "wilayah_terdampak": ["Jawa Tengah", "Jawa Timur"],
        "jumlah_jiwa": 1200,
        "detail_korban": "Penerima manfaat: 1.200 pasien",
        "kebutuhan": ["💊 Obat-obatan dasar", "🩺 Pemeriksaan kesehatan", "🚑 Transportasi pasien", "🧪 Tes laboratorium", "🥛 Nutrisi tambahan pasien"],
        "dampak_100k": "💊 Membantu penyediaan obat dasar untuk 2 pasien\n🩺 Membantu biaya pemeriksaan kesehatan\n🥛 Menyediakan paket nutrisi pasien selama beberapa hari"
    },
    "lingkungan": {
        "id": "lingkungan",
        "judul": "Program Penanaman Pohon Indonesia Hijau",
        "kategori": "Lingkungan",
        "deskripsi": "Program ini bertujuan memulihkan lahan kritis dan meningkatkan kualitas lingkungan hidup.",
        "wilayah_terdampak": ["Jawa Tengah", "Jawa Barat", "Kalimantan"],
        "detail_wilayah": "Di 23 lokasi penghijauan",
        "jumlah_jiwa": 500,
        "detail_korban": "Melibatkan lebih dari 500 relawan lingkungan. Saat ini telah berhasil ditanam 18.750 pohon.",
        "dampak_100k": "✅ 5 bibit pohon produktif\n✅ Pupuk dan media tanam\n✅ Perawatan awal pohon\nEstimasi penyerapan karbon dari pohon yang ditanam dapat mencapai puluhan kilogram CO₂ selama masa pertumbuhannya."
    }
}

# ── Intent Patterns ───────────────────────────────────────────────────
INTENT_PATTERNS = {
    "greeting": [
        r"\b(halo|hai|hi|hey|helo|assalamualaikum)\b",
        r"\b(selamat|pagi|siang|sore|malam)\b"
    ],
    "farewell": [
        r"\b(bye|dadah|sampai jumpa|selamat tinggal)\b",
        r"\b(terima kasih|makasih|thanks|thank you|suwun)\b"
    ],
    
    # ── Detail Program Utama (Program Static) ───────────────────────────
    "ask_disaster_detail": [
        r"\b(banjir demak)\b", 
        r"detail.*banjir", 
        r"info.*banjir", 
        r"tentang.*banjir.*demak"
    ],
    "ask_education_detail": [
        r"(program|bantuan|detail|info).*(pendidikan|beasiswa|sekolah)",
        r"(pendidikan|beasiswa|sekolah).*(program|bantuan|detail|info)",
        r"tentang.*(pendidikan|beasiswa|sekolah)"
    ],
    "ask_health_detail": [
        r"(program|bantuan|detail|info).*(kesehatan|medis|pengobatan|sakit)",
        r"(kesehatan|medis|pengobatan|sakit).*(program|bantuan|detail|info)",
        r"tentang.*(kesehatan|medis|pengobatan|sakit)"
    ],
    "ask_environment_detail": [
        r"(program|bantuan|detail|info).*(lingkungan|penghijauan|pohon|alam)",
        r"(lingkungan|penghijauan|pohon|alam).*(program|bantuan|detail|info)",
        r"tentang.*(lingkungan|penghijauan|pohon|alam)"
    ],
    
    # ── Pertanyaan Kontekstual Program (Mendukung Follow-up Pendek) ──
    "ask_date_time": [
        r"\bkapan\b",
        r"\b(tanggal|waktu|hari|jam)\b",
        r"kapan.*(terjadi|mulai|kejadian)",
        r"(tanggal|waktu).*(kejadian|mulai)"
    ],
    "ask_location": [
        r"\b(dimana|di mana|mana|lokasi|wilayah|tempat|daerah)\b",
        r"lokasi.*terdampak",
        r"di.*mana.*kejadian"
    ],
    "ask_victim_count": [
        r"\bberapa\b.*\b(korban|jiwa|orang|anak|siswa|keluarga|pengungsi|pasien)\b",
        r"\bjumlah\b.*\b(korban|jiwa|orang|anak|siswa|keluarga|pengungsi|pasien)\b",
        r"\b(berapa|jumlah)\s+(korban|jiwa|terdampak|pengungsi)\b",
        r"\b(korban|jiwa|pengungsi|penerima manfaat)\b"
    ],
    "ask_needs": [
        r"\b(kebutuhan|dibutuhkan|perlu|diperlukan|mendesak|logistik)\b",
        r"butuh\s+apa",
        r"apa\s+saja\s+yang\s+diperlukan"
    ],
    
    # ── Simulasi Dampak Berdasarkan Nominal (Score-Boosted) ────────────
    "ask_impact_100k": [
        r"\b100(\.000)?\b",
        r"100\s*(ribu|rb)",
        r"seratus\s*ribu",
        r"donasi.*100",
        r"dampak.*100",
        r"bantuan.*100"
    ],
    "ask_impact_500k": [
        r"\b500(\.000)?\b",
        r"500\s*(ribu|rb)",
        r"lima\s*ratus\s*ribu",
        r"donasi.*500",
        r"dampak.*500",
        r"bantuan.*500"
    ],
    "ask_impact_simulation": [
        r"(jika|kalau|misal|seandainya|dampak|manfaat|bantuan).*(donasi|berdonasi|menyumbang|sumbang).*(rp|Rp)?\s*(\d+)",
        r"(rp|Rp)\s*\d+",
        r"\b\d+\s*(ribu|rb|juta|jt)\b",
        r"nominal.*\d+"
    ],

    # ── Statistik & Kategori Kampanye Dinamis ──────────────────────────
    "ask_total_donation": [
        r"(total|berapa|jumlah).*(donasi|dana|uang|terkumpul|sumbangan)",
        r"(dana|donasi|uang|sumbangan).*(terkumpul|masuk|diterima|total)",
        r"sudah\s+(berapa|terkumpul)",
        r"total\s+dana"
    ],
    "ask_program_count": [
        r"(berapa|jumlah|ada|daftar).*(program|kampanye|kegiatan|proyek|opsi)",
        r"(program|kampanye|kegiatan|proyek).*(berapa|aktif|jumlah|banyak)",
        r"berapa\s+program",
        r"jumlah\s+kampanye"
    ],
    "ask_donor_count": [
        r"(berapa|jumlah|ada).*(donatur|penyumbang|orang|donor)",
        r"(donatur|penyumbang|donor).*(berapa|jumlah|banyak)",
        r"berapa\s+donatur",
        r"jumlah\s+penyumbang"
    ],
    
    # Intent khusus mencari kategori dinamis (Diwajibkan ada keyword pencarian)
    "search_education": [
        r"(cari|lihat|daftar|kategori|tampilkan|semua|kumpulan|jelajahi).*(pendidikan|sekolah|beasiswa|belajar|siswa)",
        r"(pendidikan|sekolah|beasiswa|belajar|siswa).*(cari|lihat|daftar|kategori|tampilkan|kumpulan|jelajahi)",
        r"kategori\s+pendidikan"
    ],
    "search_health": [
        r"(cari|lihat|daftar|kategori|tampilkan|semua|kumpulan|jelajahi).*(kesehatan|medis|sakit|obat|dokter|klinik)",
        r"(kesehatan|medis|sakit|obat|dokter|klinik).*(cari|lihat|daftar|kategori|tampilkan|kumpulan|jelajahi)",
        r"kategori\s+kesehatan"
    ],
    "search_disaster": [
        r"(cari|lihat|daftar|kategori|tampilkan|semua|kumpulan|jelajahi).*(bencana|banjir|gempa|longsor|kebakaran)",
        r"(bencana|banjir|gempa|longsor|kebakaran).*(cari|lihat|daftar|kategori|tampilkan|kumpulan|jelajahi)",
        r"kategori\s+(bencana|alam)"
    ],
    "search_environment": [
        r"(cari|lihat|daftar|kategori|tampilkan|semua|kumpulan|jelajahi).*(lingkungan|hutan|mangrove|sampah|alam)",
        r"(lingkungan|hutan|mangrove|sampah|alam).*(cari|lihat|daftar|kategori|tampilkan|kumpulan|jelajahi)",
        r"kategori\s+lingkungan"
    ],
    
    # ── Prosedur Platform & Informasi Umum ─────────────────────────────
    "ask_how_to_donate": [
        r"(cara|gimana|bagaimana|langkah|step|panduan).*(donasi|bayar|sumbang|transfer|bantu|berdonasi)",
        r"(donasi|bayar|sumbang|transfer|berdonasi).*(cara|gimana|bagaimana|langkah|panduan)",
        r"(bisa|mau|ingin|pengen|cara).*(donasi|sumbang|bantu|bayar|berdonasi|menyumbang)",
        r"prosedur.*(donasi|menyumbang)"
    ],
    "ask_payment_method": [
        r"(metode|jenis|pilihan|opsi|apa saja).*(bayar|pembayaran|transfer)",
        r"(bayar|pembayaran|transfer).*(metode|jenis|pilihan|pake|pakai|lewat|via|melalui)",
        r"\b(gopay|ovo|dana|qris|bca|mandiri|bni|bri|linkaja|shopeepay|transfer)\b"
    ],
    "ask_transparency": [
        r"(transparan|laporan|bukti|audit|akuntabel|jujur|terbuka)",
        r"(dana|uang|donasi).*(digunakan|disalurkan|dipakai|kemana|ke mana|larinya)",
        r"(kemana|ke mana).*(uang|dana|donasi|penyaluran)"
    ],
    "ask_security": [
        r"(aman|keamanan|terpercaya|penipuan|bodong|percaya|legal|resmi|izin)",
        r"apakah.*(aman|penipuan|beneran)"
    ],
    "ask_volunteer": [
        r"\b(volunteer|relawan|sukarelawan)\b",
        r"(jadi|mau|ingin|pengen|gabung|daftar|bergabung).*(relawan|volunteer|sukarelawan)",
        r"cara.*(jadi|gabung).*relawan"
    ],
    "ask_about": [
        r"(apa itu|tentang|mengenai|jelaskan|profil).*(donasicare|platform|organisasi|yayasan|apps|aplikasi)",
        r"(siapa|apa).*(donasicare|kalian|kamu|anda|carebot)"
    ],
    "ask_recommendation": [
        r"(rekomendasi|rekomen|saran|sarankan|suggest|rekomendasikan)",
        r"(program|kampanye|donasi).*(terbaik|populer|unggulan|favorit|bagus|mendesak)",
        r"(mau|ingin|pengen).*(donasi|bantu|sumbang).*(apa|mana|kemana|ke mana)"
    ],
    "positive_sentiment": [
        r"\b(bagus|keren|mantap|hebat|luar biasa|amazing|wow|good|great|suka|senang|terbantu)\b"
    ],
    "negative_sentiment": [
        r"\b(jelek|buruk|mengecewakan|kecewa|tidak suka|benci|marah|kesal|lelet|lambat|error|bug)\b"
    ],
}
def classify_intent(text: str) -> str:
    """Klasifikasikan intent dari teks pengguna menggunakan regex pattern matching."""
    text_lower = text.lower().strip()
    scores = {}
    for intent, patterns in INTENT_PATTERNS.items():
        score = 0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            score += len(matches)
        if score > 0:
            scores[intent] = score
    
    if not scores:
        return "unknown"
    return max(scores, key=scores.get)

def detect_mood(text: str) -> str:
    """Deteksi mood/sentimen sederhana dari teks."""
    text_lower = text.lower()
    positive_words = ["bagus", "keren", "mantap", "hebat", "senang", "suka", "terima kasih", "makasih", "thanks"]
    negative_words = ["jelek", "buruk", "kecewa", "marah", "kesal", "tidak suka", "benci"]
    
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    
    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"

# ── Context Management ───────────────────────────────────────────────
def detect_context(history: list) -> str:
    if not history: return None
    # Cari ke belakang hingga 5 pesan terakhir untuk mendeteksi program aktif
    for msg in reversed(history[-5:]):
        text = msg.get("content", "").lower() if isinstance(msg, dict) else str(msg).lower()
        if "banjir demak" in text: return "banjir_demak"
        if "pendidikan" in text or "beasiswa" in text: return "pendidikan"
        if "kesehatan" in text or "pengobatan" in text: return "kesehatan"
        if "penghijauan" in text or "lingkungan" in text or "pohon" in text: return "lingkungan"
    return None

def _get_active_program_data(context: str, default_intent: str):
    prog_id = context
    if not prog_id:
        if default_intent == "ask_disaster_detail": prog_id = "banjir_demak"
        elif default_intent == "ask_education_detail": prog_id = "pendidikan"
        elif default_intent == "ask_health_detail": prog_id = "kesehatan"
        elif default_intent == "ask_environment_detail": prog_id = "lingkungan"
    
    return DETAILED_PROGRAMS.get(prog_id)

# ── Response Templates (Humanist, Empathetic, Persuasive) ──────────────────
GREETING_RESPONSES = [
    "Halo, Kak! 👋 Senang sekali bisa mengobrol dengan Anda. Saya CareBot, siap membantu menjawab pertanyaan seputar program kebaikan di DonasiCare. Ada yang bisa saya bantu hari ini? 😊",
    "Hai! Selamat datang di DonasiCare. 🌿 Saya di sini untuk menemani Anda mencari cara terbaik berbagi kebaikan. Ada program spesifik yang ingin Kakak tanyakan?",
]

FAREWELL_RESPONSES = [
    "Sama-sama! Terima kasih banyak sudah berkunjung dan peduli pada sesama, Kak! ❤️ Semoga hari Anda penuh berkah. Jangan ragu untuk kembali jika ada yang ingin ditanyakan lagi ya. 👋",
    "Terima kasih kembali atas kepedulian Anda. 🙏 Sekecil apapun kebaikan kita, pasti sangat berarti bagi mereka yang membutuhkan. Sampai jumpa lagi! ✨",
]

VOLUNTEER_RESPONSES = [
    "Ingin jadi relawan? Luar biasa! 🦺\n\n"
    "Anda bisa mendaftar melalui halaman **Volunteer Center** di menu navigasi. "
    "Di sana Anda akan menemukan berbagai peluang kerelawanan, mulai dari distribusi bantuan "
    "langsung di lapangan hingga kegiatan edukasi untuk anak-anak.\n\n"
    "Mari bergabung dengan ribuan relawan DonasiCare lainnya!",
]

ABOUT_RESPONSES = [
    "**DonasiCare** adalah wadah digital yang mempertemukan orang-orang berhati baik seperti Anda dengan mereka yang sedang membutuhkan bantuan. 💚\n\n"
    "Kami hadir untuk memastikan setiap rupiah yang Anda donasikan tersalurkan dengan **aman, transparan, dan tepat sasaran**. Kami bekerja sama dengan mitra terpercaya di lapangan untuk program Pendidikan, Kesehatan, Bencana Alam, dan banyak lagi.\n\n"
    "Bersama DonasiCare, mari kita buat perubahan nyata, karena kepedulian Anda adalah harapan bagi mereka! 🌟",
]

POSITIVE_RESPONSES = [
    "Senang mendengarnya! 😊 Terima kasih atas apresiasi Anda. Kami terus berusaha memberikan yang terbaik untuk para donatur dan penerima manfaat.",
    "Terima kasih banyak! 🌟 Dukungan dan semangat Anda membuat kami semakin termotivasi untuk menyalurkan kebaikan lebih banyak lagi.",
]

NEGATIVE_RESPONSES = [
    "Mohon maaf atas ketidaknyamanannya. 🙏 Masukan Anda sangat berharga bagi kami. Bisakah Anda jelaskan lebih detail agar kami bisa memperbaikinya?",
    "Kami minta maaf jika ada yang kurang berkenan. Kami selalu terbuka untuk saran dan perbaikan. Silakan hubungi kami melalui halaman **Tentang Kami** untuk feedback lebih lanjut.",
]

def _get_time_greeting() -> str:
    hour = datetime.datetime.now().hour
    if hour < 11:
        return "Selamat pagi"
    elif hour < 15:
        return "Selamat siang"
    elif hour < 18:
        return "Selamat sore"
    return "Selamat malam"

def _build_donation_guide() -> str:
    return (
        "Berdonasi di DonasiCare sangat mudah dan aman kok, Kak! 📋\n\n"
        "1️⃣ Pilih program yang mengetuk hati Kakak di halaman **Donasi Sekarang**\n"
        "2️⃣ Masukkan nominal donasi yang ingin disumbangkan\n"
        "3️⃣ Pilih metode pembayaran favorit Kakak (Bisa GoPay, QRIS, BCA, dll)\n"
        "4️⃣ Selesaikan pembayaran dan dana akan langsung tercatat!\n\n"
        "Kakak juga punya opsi untuk menyembunyikan nama (anonim) jika ingin berdonasi secara tertutup. 🔒\n"
        "Setiap kontribusi Kakak, sekecil apapun, akan membawa senyum bagi mereka."
    )

def _build_payment_info() -> str:
    return (
        "Kami menyediakan berbagai metode pembayaran untuk kemudahan Anda: 💳\n\n"
        "**Virtual Account:**\n"
        "• BCA Virtual Account\n"
        "• Mandiri Virtual Account\n\n"
        "**E-Wallet:**\n"
        "• GoPay\n"
        "• OVO\n"
        "• DANA\n\n"
        "**Lainnya:**\n"
        "• QRIS (Semua e-wallet)\n"
        "• Transfer Bank Manual\n\n"
        "Semua metode aman dan terverifikasi. Bukti donasi akan langsung tersimpan di riwayat Anda. ✅"
    )

def _build_campaign_response(kategori: str, intro: str) -> str:
    campaigns = get_campaigns_by_category(kategori)
    if not campaigns:
        all_campaigns = get_all_campaigns()
        if all_campaigns:
            response = f"Maaf, saat ini belum ada program khusus kategori **{kategori}**. Namun, berikut program lain yang bisa Anda bantu:\n\n"
            for c in all_campaigns[:3]:
                progress = min(int((c['dana_terkumpul'] / c['target_dana']) * 100), 100) if c['target_dana'] > 0 else 0
                response += f"📌 **{c['judul']}** ({c['kategori']})\n"
                response += f"   Terkumpul: {format_rupiah(c['dana_terkumpul'])} dari {format_rupiah(c['target_dana'])} ({progress}%)\n\n"
            return response
        return f"Maaf, saat ini belum ada program aktif untuk kategori {kategori}."
    
    response = intro + "\n\n"
    for c in campaigns[:3]:
        progress = min(int((c['dana_terkumpul'] / c['target_dana']) * 100), 100) if c['target_dana'] > 0 else 0
        response += f"📌 **{c['judul']}**\n"
        response += f"   {c.get('deskripsi', '')[:100]}...\n"
        response += f"   Terkumpul: {format_rupiah(c['dana_terkumpul'])} dari {format_rupiah(c['target_dana'])} ({progress}%)\n\n"
    response += "Kunjungi halaman **Donasi Sekarang** untuk mulai membantu! 💛"
    return response

def _build_recommendation_response() -> str:
    campaigns = get_all_campaigns()
    if not campaigns:
        return "Maaf, belum ada program kampanye yang tersedia saat ini."
    
    sorted_campaigns = sorted(campaigns, key=lambda c: c.get('dana_terkumpul', 0), reverse=True)[:3]
    response = "Berikut **3 program unggulan** kami yang paling banyak mendapat dukungan: 🏆\n\n"
    for i, c in enumerate(sorted_campaigns, 1):
        progress = min(int((c['dana_terkumpul'] / c['target_dana']) * 100), 100) if c['target_dana'] > 0 else 0
        response += f"**{i}. {c['judul']}** ({c['kategori']})\n"
        response += f"   Terkumpul: {format_rupiah(c['dana_terkumpul'])} dari {format_rupiah(c['target_dana'])} ({progress}%)\n\n"
    response += "Anda bisa melihat detail lengkapnya di halaman **Program Donasi**."
    return response

# ── Smart Response Generator ──────────────────────────────────────────
def generate_smart_response(text: str, history: list = None, chat_history: list = None) -> str:
    """
    Mesin respons utama chatbot DonasiCare.
    Mendukung argument 'history' maupun 'chat_history' untuk menjamin fleksibilitas integrasi UI.
    """
    if history is None:
        history = chat_history if chat_history is not None else []
        
    intent = classify_intent(text)
    mood = detect_mood(text)
    
    # Prioritaskan rasa empati jika mood terdeteksi negatif/positif saat intent tak dikenal
    if mood == "negative" and intent == "unknown":
        intent = "negative_sentiment"
    elif mood == "positive" and intent == "unknown":
        intent = "positive_sentiment"
    
    fillers_info = ["Tentu saja! ", "Baiklah, ", "Siap! ", "Oh, tentu bisa. ", "Ini dia detailnya: ", "Mari saya jelaskan. "]
    fillers_search = ["Hmm, sebentar ya saya carikan... 🤔\n\n", "Beri saya waktu sejenak untuk mengecek... 🔍\n\n", "Wah, niat yang sangat mulia! Ini beberapa daftarnya:\n\n"]
    
    # 1. Program Introduction Intents (Statis - Program 1)
    if intent == "ask_disaster_detail":
        p = DETAILED_PROGRAMS["banjir_demak"]
        return f"📍 **{p['judul']}**\n\n{p['deskripsi']}\n\n📅 Tanggal kejadian:\n{p['tanggal_kejadian']}\n\n⏰ Waktu awal kejadian:\n{p['waktu_kejadian']}\n\nSaat ini proses evakuasi dan distribusi bantuan masih terus dilakukan."
    
    elif intent == "ask_education_detail":
        p = DETAILED_PROGRAMS["pendidikan"]
        return f"📚 **{p['judul']}**\n\n{p['deskripsi']}\n\n👧 Penerima manfaat:\n{p['jumlah_jiwa']} siswa\n\n📍 Wilayah:\n{', '.join(p['wilayah_terdampak'])}\n\n🏫 Sekolah yang terlibat:\n{p['detail_wilayah']}"
        
    elif intent == "ask_health_detail":
        p = DETAILED_PROGRAMS["kesehatan"]
        return f"🏥 **{p['judul']}**\n\n{p['deskripsi']}\n\n👥 Penerima manfaat:\n{p['jumlah_jiwa']} pasien\n\n📍 Wilayah:\n{', '.join(p['wilayah_terdampak'])}"
        
    elif intent == "ask_environment_detail":
        p = DETAILED_PROGRAMS["lingkungan"]
        return f"🌱 **{p['judul']}**\n\n{p['deskripsi']}\n\n📍 Lokasi:\n{', '.join(p['wilayah_terdampak'])}\n\n🌳 Target:\n{p['jumlah_jiwa']} relawan"

    # 2. Contextual Questions (Program 1 Context Flow)
    context = detect_context(history)
    p = _get_active_program_data(context, intent)
    
    if p:
        if intent == "ask_date_time":
            if "tanggal_kejadian" in p:
                return f"📅 {p['judul']} mulai terjadi pada:\n\n{p['tanggal_kejadian']}\n\n⏰ Sekitar pukul {p['waktu_kejadian']}.\n\n{p['deskripsi']}"
            return f"Program {p['judul']} berjalan sepanjang tahun."
            
        elif intent == "ask_location":
            resp = f"📍 Wilayah untuk {p['judul']}:\n\n"
            for i, w in enumerate(p['wilayah_terdampak'], 1):
                resp += f"{i}. {w}\n"
            if "detail_wilayah" in p:
                resp += f"\nTotal:\n{p['detail_wilayah']}"
            return resp
            
        elif intent == "ask_victim_count":
            return f"👥 Data untuk {p['judul']}:\n\nTotal jiwa:\n{p['jumlah_jiwa']}\n\n{p.get('detail_korban', '')}"
            
        elif intent == "ask_needs":
            if "kebutuhan" in p:
                resp = f"Saat ini kebutuhan utama untuk {p['judul']} adalah:\n\n"
                for n in p['kebutuhan']: resp += f"{n}\n"
                return resp
            return f"Kami menggalang dana tunai untuk disalurkan ke berbagai kebutuhan mendesak {p['judul']}."
            
        elif intent == "ask_impact_100k":
            return f"Terima kasih atas kepedulian Kakak ❤️\n\nDengan donasi Rp100.000 untuk {p['judul']}, bantuan yang dapat diberikan antara lain:\n\n{p['dampak_100k']}"
            
        elif intent == "ask_impact_500k":
            if "dampak_500k" in p:
                return f"Dengan donasi Rp500.000 untuk {p['judul']}, bantuan yang dapat diberikan antara lain:\n\n{p['dampak_500k']}"
            return f"Terima kasih! Donasi Rp500.000 akan sangat berarti untuk mendukung program {p['judul']} secara luas."

    # 3. Category Search Intents (Dinamis dari Database - Program 2)
    if intent == "search_education":
        return random.choice(fillers_search) + _build_campaign_response("Pendidikan", "📚 Berikut program **pendidikan** yang sedang membutuhkan bantuan:")
    
    elif intent == "search_health":
        return random.choice(fillers_search) + _build_campaign_response("Kesehatan", "🏥 Berikut program **kesehatan** yang sedang berjalan:")
    
    elif intent == "search_disaster":
        return random.choice(fillers_search) + _build_campaign_response("Bencana Alam", "🆘 Berikut program **bantuan bencana** darurat:")
    
    elif intent == "search_environment":
        return random.choice(fillers_search) + _build_campaign_response("Lingkungan", "🌿 Berikut program **lingkungan** yang bisa didukung:")

    # 4. Generic & Informational Intents (Penggabungan Program 1 & 2)
    if intent == "greeting":
        return random.choice(GREETING_RESPONSES)
        
    elif intent == "farewell":
        return random.choice(FAREWELL_RESPONSES)
        
    elif intent == "ask_total_donation":
        total = get_total_donasi()
        donor_count = get_donation_count()
        campaign_count = get_campaign_count()
        prefix = random.choice(["Wah, pertanyaan yang bagus! ", "Saat ini, ", "Alhamdulillah, "])
        return (
            f"{prefix}📊 **Statistik DonasiCare Terkini:**\n\n"
            f"💰 Total donasi terkumpul: **{format_rupiah(total)}**\n"
            f"👥 Jumlah donatur: **{donor_count:,}** orang\n"
            f"📋 Program aktif: **{campaign_count}** program\n\n"
            f"Angka ini terus bertambah berkat kebaikan para donatur seperti Anda! 🙏"
        )
        
    elif intent == "ask_program_count":
        count = get_campaign_count()
        prefix = random.choice(fillers_info)
        return (
            f"{prefix}Saat ini DonasiCare memiliki **{count} program kampanye aktif** yang tersebar "
            f"di berbagai kategori seperti Pendidikan, Kesehatan, Bencana Alam, dan lainnya.\n\n"
            f"Anda bisa mengunjungi halaman **Program Donasi** untuk melihat detail setiap program!"
        )
        
    elif intent == "ask_donor_count":
        donor_count = get_donation_count()
        prefix = random.choice(["Luar biasa, ", "Sampai detik ini, ", "Tercatat, "])
        return (
            f"{prefix}sudah ada **{donor_count:,} donasi** yang masuk di platform kami! 🎉\n\n"
            f"Setiap orang yang berdonasi turut menciptakan perubahan nyata. "
            f"Bergabunglah dan jadilah bagian dari gerakan kebaikan ini!"
        )
        
    elif intent == "ask_how_to_donate":
        return _build_donation_guide()
        
    elif intent == "ask_payment_method":
        return _build_payment_info()
        
    elif intent == "ask_transparency":
        return (
            "Pertanyaan yang sangat bagus dan penting, Kak! 💡\n\n"
            "Di DonasiCare, kami sangat menjunjung tinggi **transparansi dan amanah**. Bagaimana dana disalurkan?\n"
            "1. Dana yang masuk dicatat secara *real-time* di sistem kami. 📝\n"
            "2. Bantuan disalurkan langsung ke penerima manfaat melalui mitra lapangan kami yang telah diverifikasi ketat. 🤝\n"
            "3. Kami selalu memberikan *update* laporan penyaluran berupa foto dokumentasi dan rincian penggunaan dana di halaman masing-masing program. 📸\n\n"
            "Jadi, Kakak bisa memantau terus jejak kebaikan Kakak. Kami pastikan amanah Anda tersalurkan dengan benar! 🛡️"
        )
        
    elif intent == "ask_security":
        return (
            "Jangan khawatir, Kak! 🛡️ Keamanan dan kepercayaan donatur adalah prioritas utama kami.\n\n"
            "Platform DonasiCare menggunakan sistem enkripsi data tingkat tinggi dan bekerja sama dengan payment gateway resmi (Gopay, OVO, Bank). "
            "Setiap penggalang dana dan program juga telah melewati proses verifikasi identitas yang ketat untuk mencegah penipuan. 🔒\n\n"
            "Donasi Kakak dijamin 100% aman. Ada program yang ingin Kakak dukung hari ini? 😊"
        )
        
    elif intent == "ask_impact_simulation":
        matches = re.findall(r"(?:rp|Rp)?\s*(\d{1,3}(?:\.\d{3})*|\d+)", text.lower())
        nom = 0
        if matches:
            clean_m = matches[0].replace(".", "")
            if clean_m.isdigit():
                nom = int(clean_m)
                
        if nom > 0:
            if nom <= 50000:
                dampak = (
                    "🍚 Membantu penyediaan kebutuhan pangan dasar\n"
                    "👨‍👩‍👧 Membantu 1-2 keluarga penerima manfaat\n"
                    "❤️ Mendukung distribusi bantuan ke wilayah yang membutuhkan"
                )
            elif nom <= 150000:
                dampak = (
                    "🍚 Bantuan pangan untuk beberapa keluarga sekaligus\n"
                    "📚 Dukungan perlengkapan belajar atau sekolah anak\n"
                    "💧 Memenuhi kebutuhan dasar harian penerima manfaat\n"
                    "❤️ Menjangkau lebih banyak wilayah yang membutuhkan bantuan"
                )
            else:
                dampak = (
                    "🏡 Membantu perbaikan fasilitas umum atau penyediaan tempat tinggal sementara\n"
                    "🎒 Beasiswa dan fasilitas pendidikan lengkap untuk anak kurang mampu\n"
                    "🩺 Bantuan paket medis dan pengobatan intensif\n"
                    "🌟 Memberikan dampak jangka panjang yang signifikan bagi komunitas"
                )
                
            return (
                f"Terima kasih atas niat baik Anda ❤️\n\n"
                f"Dengan donasi sebesar **Rp {nom:,}**, Anda dapat membantu mendukung program-program kebaikan kami.\n\n"
                f"Perkiraan dampak dari kebaikan Anda:\n{dampak}\n\n"
                f"Meskipun nominalnya terlihat sederhana, setiap bantuan ini dapat memberikan manfaat yang luar biasa dan senyuman bagi mereka yang sedang kesulitan. "
                f"Semakin besar kontribusi yang diberikan, tentu semakin luas dan banyak manfaat yang dapat dirasakan oleh mereka yang membutuhkan.\n\n"
                f"Apakah Anda ingin mengetahui dampak spesifik untuk program tertentu seperti pendidikan, kesehatan, atau bantuan bencana alam?"
            )
        else:
            return (
                "Terima kasih atas niat baik Anda ❤️\n\n"
                "Setiap donasi, berapapun nominalnya, sangat berarti dan memiliki dampak nyata untuk meringankan beban saudara kita yang membutuhkan. "
                "Bantuan Anda bisa menjadi makanan bagi yang lapar, obat bagi yang sakit, atau harapan bagi anak yang ingin sekolah.\n\n"
                "Ada program spesifik yang ingin Kakak ketahui lebih lanjut?"
            )
            
    elif intent == "ask_volunteer":
        return random.choice(VOLUNTEER_RESPONSES)
        
    elif intent == "ask_about":
        return random.choice(ABOUT_RESPONSES)
        
    elif intent == "ask_recommendation":
        return random.choice(["Tentu, saya punya beberapa saran nih! ", "Ini dia program-program pilihan kami: ", "Berdasarkan data kami, "]) + _build_recommendation_response()
        
    elif intent == "positive_sentiment":
        return random.choice(POSITIVE_RESPONSES)
        
    elif intent == "negative_sentiment":
        return random.choice(NEGATIVE_RESPONSES)

    # 5. Fallback jika pertanyaannya spesifik butuh konteks (Program 1)
    if intent in ["ask_date_time", "ask_location", "ask_victim_count", "ask_needs", "ask_impact_100k", "ask_impact_500k"]:
        return "Program mana yang Kakak maksud? (Contoh: Banjir Demak, Pendidikan, Kesehatan, atau Lingkungan)"

    # 6. Fallback Judul / Keyword matching dari Database Kampanye (Program 2)
    campaigns = get_all_campaigns()
    prompt_lower = text.lower()
    matched = [c for c in campaigns if any(word in c['judul'].lower() for word in prompt_lower.split() if len(word) > 3)]
    
    if matched:
        response = random.choice(["Sepertinya saya menemukan sesuatu yang pas dengan pencarian Anda:\n\n", "Coba lihat beberapa program ini, mungkin sesuai dengan maksud Anda:\n\n"])
        for c in matched[:2]:
            progress = min(int((c['dana_terkumpul'] / c['target_dana']) * 100), 100) if c['target_dana'] > 0 else 0
            response += f"📌 **{c['judul']}** ({c['kategori']})\n"
            response += f"   Terkumpul: {format_rupiah(c['dana_terkumpul'])} dari {format_rupiah(c['target_dana'])} ({progress}%)\n\n"
        response += "Untuk informasi lebih lengkap, Anda bisa cek di halaman **Program Donasi** ya."
        return response

    # 7. Final Fallback (Program 2)
    time_greeting = _get_time_greeting()
    fallback_responses = [
        f"Hmm... {time_greeting.lower()}, maaf ya, saya agak kesulitan menangkap maksud Anda. 🤔\n\n"
        "Tapi jangan khawatir! Berikut beberapa hal yang bisa saya bantu jawab:\n"
        "• 💰 Info total donasi terkumpul\n"
        "• 📋 Rekomendasi program donasi\n"
        "• 📝 Cara dan panduan berdonasi\n"
        "• 💳 Pilihan metode pembayaran\n"
        "• 📊 Transparansi penyaluran dana\n\n"
        "Silakan ketik ulang atau pilih topik di atas ya!",
        
        f"Aduh, sepertinya pertanyaan itu di luar pengetahuan saya saat ini. 😅\n\n"
        "Sebagai asisten DonasiCare, saya sangat mahir menjawab tentang program, cara donasi, "
        "dan laporan transparansi. Ada yang bisa saya bantu dari topik-topik tersebut?",
    ]
    return random.choice(fallback_responses)

# ── Streaming / Typing Effect Generator ───────────────────────────────
def stream_text(text: str, delay_min: float = 0.01, delay_max: float = 0.04, by_char: bool = False):
    """
    Generator untuk efek mengetik (typing effect). 
    Mendukung mode karakter (by_char=True dari Progam 1) maupun mode kata natural (by_char=False dari Program 2).
    """
    if by_char:
        for char in text:
            yield char
            time.sleep(random.uniform(0.005, 0.02))
    else:
        for word in text.split(" "):
            yield word + " "
            if word.endswith(".") or word.endswith("!") or word.endswith("?") or word.endswith("\n"):
                time.sleep(random.uniform(delay_min * 8, delay_max * 8))
            elif word.endswith(",") or word.endswith(":"):
                time.sleep(random.uniform(delay_min * 4, delay_max * 4))
            else:
                time.sleep(random.uniform(delay_min, delay_max))

# ── Database Helpers ──────────────────────────────────────────────────
def save_chat(*args, **kwargs):
    """Simpan riwayat percakapan chatbot (No-op kompatibel dengan multi-signature)."""
    pass

def get_chat_history(user_id=None):
    """Ambil riwayat chatbot."""
    return []