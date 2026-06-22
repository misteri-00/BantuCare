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
        r"(pay|pembayaran|transfer).*(metode|jenis|pilihan|pake|pakai|lewat|via|melalui)",
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
    "choose_volunteer": [
        r"(pilih|mau|daftar|ikut).*(distribusi|guru|medis|pangan|pelosok|darurat)",
        r"\b(distribusi|guru\s+relawan|medis|pendidikan|bencana)\b"
    ],
    "fill_volunteer_info": [
        r"[a-zA-Z\s]+\s*-\s*\d{1,2}\s*-\s*(08\d+|\+62\d+)\s*-\s*[a-zA-Z\s]+",
        r"(nama|umur|usia|no\s+hp|nomor).*(nama|umur|usia|no\s+hp|nomor)",
        r"(nama\s*:|umur\s*:|hp\s*:|wa\s*:)"
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

    # ✨ ═══════════════════════════════════════════════════════════════
    # 💥 EXTENDED SCENARIO INTENTS (ADDED)
    # ═══════════════════════════════════════════════════════════════════
    "ask_general_donation_guide": [
        r"(panduan|informasi|penjelasan|detail).*(donasi|menyumbang|beramal)",
        r"(pengen|ingin).*(tahu|paham).*(semua|banyak|lengkap).*(donasi)",
        r"ceritakan.*(tentang donasi|proses donasi)"
    ],
    "ask_donation_behalf": [
        r"(donasi|sumbang|sedekah).*(atas\s+nama|untuk|buat|wakilkan).*(orang\s+lain|almarhum|orang\s+tua|keluarga)",
        r"bisa.*(atas\s+nama).*(almarhum)"
    ],
    "ask_donation_asset": [
        r"(donasi|sumbang|wakaf).*(aset|tanah|bangunan|emas|saham|kendaraan)",
        r"bisa.*(donasi|wakaf).*(tanah|rumah)"
    ],
    "ask_verification_process": [
        r"(verifikasi|cek|validasi).*(mitra|lapangan|kampanye|program|penerima)",
        r"mencegah.*(penipuan|fiktif)"
    ],
    "ask_riba_free": [
        r"(bebas|tanpa).*(riba|bunga|potongan\s+bank)",
        r"apakah.*(halal|syariah).*(donasi|sistem|platform)"
    ],
    "ask_refund_donation": [
        r"(salah.*(nominal|transfer|kirim|donasi|input|ketik))",
        r"(salah\s+(ngetik|ketik))",
        r"(batal|refund|tarik|kembali)",
        r"(bisa.*(batal|refund|kembali|tarik|salah))"
    ],
    "ask_tax_deduction": [
        r"(potong.*pajak|pengurang.*pajak|insentif.*pajak)",
        r"(bukti.*(pajak|spt|pajak))",
        r"\bpajak\b"
    ],
    "ask_zakat_infak": [
        r"\b(zakat|infaq|infak|sedekah|shodaqoh|fitrah|maal)\b",
        r"bisa.*(zakat|infak|sedekah)"
    ],
    "ask_corporate_partnership": [
        r"(kerjasama|mitra|partnership|kolaborasi|csr|perusahaan|instansi|komunitas)",
        r"atas\s+nama\s+(pt|perusahaan|komunitas)"
    ],
    "ask_receipt_invoice": [
        r"(kuitansi|kwitansi|nota|invoice|sertifikat|e-sertifikat|bukti.*donasi)"
    ],
    "ask_monthly_donation": [
        r"(donasi.*(rutin|bulanan|tiap bulan|berlangganan))",
        r"(rutinan|autodebet|setiap\s+bulan)"
    ],
    "ask_create_campaign": [
        r"(buat|buka|galang|bikin).*(dana|kampanye|open\s+donasi|fundraising)",
        r"cara\s+galang\s+dana\s+sendiri"
    ],
    "ask_inactive_campaign": [
        r"(kalau|jika).*(tidak.*tercapai|kurang|sisa|target.*tidak)",
        r"target.*dana.*kurang",
        r"bagaimana.*dana.*tidak.*terpenuhi"
    ],
    "ask_goods_donation": [
        r"(donasi|sumbang|bantu).*(barang|baju|pakaian|makanan|buku|sembako)",
        r"bisa\s+pakai\s+barang"
    ],
    "ask_forgot_anonymous": [
        r"(lupa.*(hamba\s+allah|sembunyi|anonim|nama.*muncul|hapus.*nama))",
        r"ingin.*ubah.*anonim"
    ],
    "ask_legality": [
        r"(legalitas|izin|resmi|terdaftar|penipuan|terpercaya|valid|kemensos)"
    ],
    "ask_minimum_donation": [
        r"(minimal|paling\s+kecil|batas\s+bawah).*(donasi|sumbang|transfer)"
    ],
    "ask_cancel_monthly": [
        r"(batal|berhenti|stop|cancel|hapus).*(rutin|autodebet|berlangganan|tiap\s+bulan)"
    ],
    "ask_payment_issue": [
        r"(belum\s+masuk|pending|gagal|error|bermasalah).*(donasi|transfer|pembayaran|saldo)"
    ],
    "ask_change_profile": [
        r"(ubah|ganti|edit|update).*(profil|nama|akun|password|email|nomor)"
    ],
    "ask_annual_report": [
        r"(laporan|report|transparansi|bukti).*(tahunan|penyaluran|penggunaan\s+dana)"
    ],
    "ask_event_invitation": [
        r"(undang|seminar|acara|narasumber|speaker|kunjungan).*(yayasan|donasicare)"
    ],
    "ask_data_privacy": [
        r"(aman|privasi|bocor|data\s+pribadi|ktp|hack)"
    ],
    "ask_emergency_help": [
        r"(darurat|mendesak|kritis|sekarat|butuh\s+bantuan\s+sekarang|tolong\s+segera)"
    ],
    "ask_collab_media": [
        r"(media|jurnalis|liputan|wawancara|press\s+release|berita)"
    ]
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
        
        # Berikan bobot ekstra untuk intent spesifik agar tidak tertutup oleh angka donasi
        if intent in ["ask_refund_donation", "ask_tax_deduction", "ask_zakat_infak", 
                      "ask_corporate_partnership", "ask_receipt_invoice", "ask_monthly_donation", 
                      "ask_create_campaign", "ask_inactive_campaign", "ask_goods_donation", 
                      "ask_forgot_anonymous", "negative_sentiment",
                      "ask_legality", "ask_minimum_donation", "ask_cancel_monthly", 
                      "ask_payment_issue", "ask_change_profile", "ask_annual_report", 
                      "ask_event_invitation", "ask_data_privacy", "ask_emergency_help", "ask_collab_media",
                      "choose_volunteer", "fill_volunteer_info", "ask_general_donation_guide",
                      "ask_donation_behalf", "ask_donation_asset", "ask_verification_process", "ask_riba_free"]:
            score *= 1000
            
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
    "Halo, Kak! 👋 Senang sekali bisa mengobrol dengan Anda. Saya CareBot, siap membantu menjawab pertanyaan seputar program kebaikan di DonasiCare. Kira-kira, program donasi seperti apa yang sedang Kakak cari hari ini? Apakah Kakak tertarik pada program pendidikan, kesehatan, lingkungan, atau mungkin bantuan bencana alam? 😊",
    "Hai, Kak! Selamat datang di DonasiCare. 🌿 Saya di sini untuk menemani Anda mencari cara terbaik berbagi kebaikan. Ada program spesifik yang ingin Kakak ketahui atau tanyakan hari ini?",
]

FAREWELL_RESPONSES = [
    "Sama-sama! Terima kasih banyak sudah berkunjung dan peduli pada sesama, Kak! ❤️ Semoga hari Anda penuh berkah. Jangan ragu untuk kembali jika ada yang ingin ditanyakan lagi ya. 👋",
    "Terima kasih kembali atas kepedulian Anda. 🙏 Sekecil apapun kebaikan kita, pasti sangat berarti bagi mereka yang membutuhkan. Sampai jumpa lagi! ✨",
]

VOLUNTEER_RESPONSES = [
    "Ingin jadi relawan? Luar biasa! 🦺\n\n"
    "Saat ini kami memiliki beberapa divisi relawan yang bisa Kakak pilih:\n"
    "1. **Relawan Distribusi Pangan** (Membantu penyaluran logistik ke daerah bencana)\n"
    "2. **Guru Relawan Pelosok** (Mengajar anak-anak di daerah terpencil)\n"
    "3. **Relawan Medis Darurat** (Tenaga kesehatan pendamping korban bencana)\n\n"
    "Kakak mau pilih menjadi relawan di divisi apa? Balas dengan divisi yang diinginkan ya! 😊",
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
        
    # ── State Machine: Create Campaign Flow ──────────────────────────────
    last_bot_msg = ""
    for msg in reversed(history):
        if isinstance(msg, dict) and msg.get("role") == "assistant":
            last_bot_msg = msg.get("content", "")
            break
            
    stop_words = ["batal", "cancel", "sudah", "tidak jadi", "stop"]
    is_cancel = any(w in text.lower() for w in stop_words)
    
    if "Langkah 1: **Pilih Kategori**" in last_bot_msg:
        if is_cancel: return "Baik Kak, pengisian formulir dibatalkan. Ada hal lain yang bisa dibantu? 😊"
        return (
            f"Baik, kategori '{text.strip()}' telah dicatat.\n\n"
            "Langkah 2: **Judul Kampanye**.\nApa judul kampanye yang ingin Kakak buat? (Misal: 'Bantu Pembangunan Sekolah X' atau 'Bantu Pak Budi Sembuh')"
        )
    elif "Langkah 2: **Judul Kampanye**" in last_bot_msg:
        if is_cancel: return "Baik Kak, pengisian formulir dibatalkan. Ada hal lain yang bisa dibantu? 😊"
        return (
            "Judul yang bagus!\n\n"
            "Langkah 3: **Target Donasi**.\nBerapa perkiraan nominal dana yang dibutuhkan untuk kampanye ini?"
        )
    elif "Langkah 3: **Target Donasi**" in last_bot_msg:
        if is_cancel: return "Baik Kak, pengisian formulir dibatalkan. Ada hal lain yang bisa dibantu? 😊"
        return (
            "Target donasi dicatat!\n\n"
            "Langkah 4: **Cerita/Kronologi**.\nMohon ceritakan secara singkat namun jelas mengenai kondisi penerima manfaat."
        )
    elif "Langkah 4: **Cerita/Kronologi**" in last_bot_msg:
        if is_cancel: return "Baik Kak, pengisian formulir dibatalkan. Ada hal lain yang bisa dibantu? 😊"
        return (
            "Terima kasih Kak atas informasi kronologinya yang lengkap! 🙏\n\n"
            "Langkah 5: **Unggah Dokumen Verifikasi & Kirim**.\n\n"
            "Untuk proses unggah foto pendukung, KTP penggalang dana, dan dokumen pendukung lainnya (seperti dokumen medis atau surat keterangan RT/RW/Aparat Desa), silakan Kakak **menghubungi Customer Service (CS)** kami.\n\n"
            "Tim kurasi kami akan membantu memverifikasi pengajuan Kakak dalam waktu 1x24 jam. Silakan klik tombol 'Hubungi Kami' atau chat via WhatsApp CS. 🤝✨"
        )
        
    intent = classify_intent(text)
    mood = detect_mood(text)
    
    # Prioritaskan rasa empati jika mood terdeteksi negatif/positif saat intent tak dikenal
    if mood == "negative" and intent == "unknown":
        intent = "negative_sentiment"
    elif mood == "positive" and intent == "unknown":
        intent = "positive_sentiment"
    
    fillers_info = ["Tentu saja! ", "Baiklah, ", "Siap! ", "Oh, tentu bisa. ", "Ini dia detailnya: ", "Mari saya jelaskan. "]
    fillers_search = ["Hmm, sebentar ya saya carikan... 🤔\n\n", "Beri saya waktu sejenak untuk mengecek... 🔍\n\n", "Wah, niat yang sangat mulia! Ini beberapa daftarnya:\n\n"]
    
    # ✨ ═══════════════════════════════════════════════════════════════
    # 💥 PRIORITY 10 NEW SCENARIO HANDLERS
    # ═══════════════════════════════════════════════════════════════════
    if intent == "ask_refund_donation":
        return (
            "Aduh, jangan panik dulu ya, Kak! Tenang saja, kami paham hal seperti ini bisa terjadi. 😌\n\n"
            "Kalau Kakak tidak sengaja salah memasukkan nominal donasi atau salah transfer, dana tersebut bisa diproses untuk pengembalian (refund) atau dialihkan ke program lain sesuai kemauan Kakak.\n\n"
            "Hubungi tim CS human kami segera lewat tombol Hubungi Kami atau WhatsApp Official dengan melampirkan:\n\n"
            "Bukti transfer\n\n"
            "Username / Email terdaftar\n\n"
            "Nominal yang seharusnya\n\n"
            "Proses ini biasanya memakan waktu 1-3 hari kerja tergantung metode pembayaran. Kami siap bantu sampai tuntas! 🫶"
        )
    elif intent == "ask_tax_deduction":
        return (
            "Wah, pertanyaan bagus sekali! Niat baik Kakak bisa mendatangkan manfaat ganda. 📄✨\n\n"
            "DonasiCare merupakan lembaga penggalangan dana resmi yang telah diakui pemerintah. Oleh karena itu, setiap donasi tertentu di platform kami bisa digunakan sebagai pengurang penghitungan pajak penghasilan (SPT Tahunan) Kakak.\n\n"
            "Caranya gampang:\n"
            "1️⃣ Pastikan Kakak mengisi nomor NPWP di profil akun DonasiCare.\n"
            "2️⃣ Ajukan permohonan Bukti Potong Pajak di menu riwayat donasi.\n"
            "3️⃣ Tim kami akan mengirimkan dokumen resmi via email untuk dilampirkan saat lapor SPT.\n\n"
            "Berbagi kebaikan jadi makin tenang dan berkah, kan? 😊"
        )
    elif intent == "ask_zakat_infak":
        return (
            "Bisa banget, Kak! Alhamdulillah, DonasiCare tidak hanya menyalurkan donasi umum, tetapi juga mengelola Zakat (Zakat Maal & Zakat Fitrah), Infak, serta Sedekah secara syariah. 🌙\n\n"
            "Kami bekerja sama dengan lembaga amil zakat resmi terverifikasi untuk memastikan penyaluran dana zakat Kakak jatuh tepat kepada 8 golongan asnaf yang berhak menerima.\n\n"
            "Kakak bisa langsung mengunjungi tab Zakat & Infak Center di aplikasi untuk menghitung kewajiban menggunakan Kalkulator Zakat otomatis kami. Praktis dan berkah insyaAllah! 🤲"
        )
    elif intent == "ask_corporate_partnership":
        return (
            "Wah, pintu kolaborasi terbuka lebar banget untuk Kakak! 🤝🏢\n\n"
            "Kami sangat menyambut baik instansi, komunitas, maupun perusahaan yang ingin menyalurkan dana CSR (Corporate Social Responsibility) atau mengadakan program kebaikan bersama secara kolektif.\n\n"
            "DonasiCare menyediakan:\n\n"
            "Laporan audit khusus dan akuntabel.\n\n"
            "Branding logo partner di halaman kampanye.\n\n"
            "Dokumentasi penyaluran eksklusif untuk korporat.\n\n"
            "Biar ngobrolnya lebih enak dan intens, Kakak bisa langsung kirim proposal atau kontak tim kemitraan kami melalui email di partnership@donasicare.org. Mari kita buat dampak yang lebih luas bersama! 🚀"
        )
    elif intent == "ask_receipt_invoice":
        return (
            "Tentu saja bisa, Kak! Bukti transparansi adalah komitmen kami. 🧾🎖️\n\n"
            "Setiap kali donasi Kakak berhasil diverifikasi oleh sistem, DonasiCare akan otomatis menerbitkan e-Sertifikat Penghargaan serta Kuitansi Resmi Digital sebagai bukti sah berkontribusi.\n\n"
            "Cara unduhnya gampang banget:\n"
            "1️⃣ Masuk ke akun DonasiCare Kakak.\n"
            "2️⃣ Buka halaman Riwayat Donasi.\n"
            "3️⃣ Klik transaksi yang diinginkan, lalu pilih tombol Unduh Sertifikat/Kuitansi.\n\n"
            "Dokumen tersebut juga otomatis dikirimkan ke email Kakak, kok. Bisa disimpan rapi buat kenang-kenangan digital! 😉"
        )
    elif intent == "ask_monthly_donation":
        return (
            "MasyaAllah, mulia banget niatnya Kak! Konsisten dalam berbagi itu hal yang luar biasa indah. 🗓️❤️\n\n"
            "Di DonasiCare ada fitur Donasi Rutin (Autodebet). Kakak bisa menyisihkan kebaikan secara otomatis setiap minggu atau setiap bulan tanpa perlu takut lupa transfer lagi.\n\n"
            "Cara mengaktifkannya:\n\n"
            "Pilih salah satu program jangka panjang (seperti Beasiswa Anak atau Pengobatan Pasien).\n\n"
            "Klik tombol 'Donasi Rutin'.\n\n"
            "Atur tanggal pemotongan dan pilih metode pembayaran pendukung (seperti LinkAja, GoPay, atau Kartu Debit).\n\n"
            "Kakak bisa membatalkan atau mengubah nominalnya kapan saja secara fleksibel di menu pengaturan akun. 😊"
        )
    elif intent == "ask_create_campaign":
        return (
            "Halo Kak! Terima kasih banyak atas kepeduliannya. Untuk membuat/mengajukan program donasi (galang dana), caranya sangat mudah kok! 💡\n\n"
            "Berikut langkah-langkah pengisian formulir penggalangan dana di DonasiCare :\n\n"
            "Langkah 1: **Pilih Kategori**.\n"
            "Tentukan apakah donasi untuk Bencana Alam, Medis/Kesehatan, Pendidikan, atau lainnya. Kategori apa yang ingin Kakak pilih?"
        )
    elif intent == "ask_inactive_campaign":
        return (
            "Ini pertanyaan yang kritis dan cerdas sekali, Kak! Tenang, dana kebaikan tidak akan hangus atau sia-sia. 🎯\n\n"
            "Apabila batas waktu pencarian dana berakhir namun target nominal kampanye belum terpenuhi, aturan DonasiCare adalah:\n\n"
            "Tetap Disalurkan: Dana yang sudah terkumpul berapapun jumlahnya akan tetap disalurkan kepada penerima manfaat sesuai dengan skala prioritas kebutuhan mendesak mereka. 🛒\n\n"
            "Pengalihan Kasus Serupa: Jika program tersebut benar-benar tidak bisa dijalankan karena dananya terlalu minim, maka dana akan dialihkan ke program lain yang sejenis (atas persetujuan perwakilan lapangan) dengan transparansi penuh.\n\n"
            "Jadi, setiap rupiah yang Kakak titipkan di sini dipastikan 100% bergerak membawa manfaat! 🌿"
        )
    elif intent == "ask_goods_donation":
        return (
            "Wah, senangnya! Bantuan tidak melulu soal uang kok, Kak. Pakaian layak, buku, atau sembako juga sangat berharga! 📦\n\n"
            "Kabar baiknya, DonasiCare menerima Donasi Berupa Barang fisik untuk program penanganan bencana alam dan pendidikan.\n\n"
            "Cara menyumbang barang:\n"
            "📦 Kirim/antarkan langsung barang Kakak ke Drop Box Center DonasiCare terdekat di kota Kakak (Daftar alamat lengkap ada di halaman hubungi kami).\n"
            "🚚 Kakak juga bisa menggunakan ekspedisi logistik dengan menuliskan kode program di luar paket.\n\n"
            "Mohon pastikan barang yang disumbangkan (terutama pakaian dan buku) dalam kondisi bersih dan masih layak pakai ya, Kak. Terima kasih banyak! 😊"
        )
    elif intent == "ask_forgot_anonymous":
        return (
            "Oalah! Tenang, Kak, privasi Kakak sepenuhnya aman bersama kami. Jangan khawatir ya. 🔒\n\n"
            "Kalau Kakak kemarin lupa mencentang opsi 'Donasikan sebagai Hamba Allah' sehingga nama asli Kakak telanjur muncul di tab donatur publik, hal itu bisa langsung diubah kok!\n\n"
            "Caranya:\n"
            "1️⃣ Masuk ke akun Kakak, pilih menu Riwayat Donasi.\n"
            "2️⃣ Cari transaksi yang ingin diubah privasinya.\n"
            "3️⃣ Klik tanda titik tiga di pojok kanan atas transaksi, lalu aktifkan centang 'Sembunyikan Nama Saya (Anonim)'.\n\n"
            "Sistem akan langsung memperbarui daftar publik dalam hitungan detik menjadi Hamba Allah. Aman terkendali! 👌"
        )
    elif intent == "ask_legality":
        return (
            "Tentu, Kak! Kepercayaan Kakak adalah amanah terbesar kami. 🛡️\n\n"
            "DonasiCare sudah terdaftar resmi dan memiliki izin operasional dari Kementerian Sosial Republik Indonesia sebagai Lembaga Kesejahteraan Sosial (LKS). Kami juga rutin diaudit oleh akuntan publik independen setiap tahunnya dengan predikat Wajar Tanpa Pengecualian (WTP).\n\n"
            "Jadi, Kakak bisa berdonasi dengan tenang dan aman. Ada program yang ingin Kakak dukung hari ini? 😊"
        )
    elif intent == "ask_minimum_donation":
        return (
            "Wah, niat baik sekecil apapun sangat kami hargai, Kak! ❤️\n\n"
            "Di DonasiCare, Kakak bisa mulai berdonasi hanya dengan Rp10.000 saja jika menggunakan metode pembayaran e-Wallet seperti GoPay, OVO, atau Dana. Sedangkan untuk Virtual Account Bank, minimal donasinya adalah Rp50.000 mengikuti kebijakan perbankan.\n\n"
            "Percayalah, satu rupiah dari Kakak bisa jadi senyuman untuk mereka yang membutuhkan. Yuk, mulai kebaikanmu hari ini! ✨"
        )
    elif intent == "ask_cancel_monthly":
        return (
            "Halo Kak! Terima kasih banyak ya sudah pernah menjadi pahlawan kebaikan secara rutin bersama kami. 🥺❤️\n\n"
            "Kalau Kakak sedang ada keperluan lain dan ingin menghentikan donasi rutin (autodebet), tentu saja bisa kapan pun tanpa syarat yang ribet.\n\n"
            "Caranya:\n"
            "1️⃣ Masuk ke akun DonasiCare.\n"
            "2️⃣ Buka menu **Donasi Rutin Saya**.\n"
            "3️⃣ Pilih program yang aktif, lalu klik **Berhenti Autodebet**.\n\n"
            "Sistem kami akan langsung menyetop pemotongan di bulan berikutnya. Kami tunggu Kakak kembali menyebar kebaikan di lain waktu ya! 🫶"
        )
    elif intent == "ask_payment_issue":
        return (
            "Aduh, mohon maaf banget ya Kak kalau ada kendala di sistem pembayaran kami! Jangan khawatir, dana Kakak pasti aman kok. 🛠️\n\n"
            "Biasanya, jika status donasi masih 'Pending', sistem bank atau e-wallet sedang membutuhkan waktu sedikit lebih lama (maksimal 1x24 jam) untuk proses sinkronisasi.\n\n"
            "Biar kami bantu cek lebih cepat, Kakak bisa langsung klik tombol **Hubungi Kami** dan infokan Nomor Invoice atau screenshot bukti transfernya. Tim CS kami akan langsung mengurusnya sampai statusnya sukses! 🚀"
        )
    elif intent == "ask_change_profile":
        return (
            "Siap, Kak! Untuk urusan ganti foto profil, nama, atau alamat email, gampang banget kok! 📝\n\n"
            "Kakak tinggal masuk ke aplikasi/web DonasiCare, lalu:\n"
            "1️⃣ Pergi ke menu **Profil** di pojok kanan atas.\n"
            "2️⃣ Klik icon pensil atau tombol **Edit Profil**.\n"
            "3️⃣ Ubah data yang Kakak inginkan dan klik **Simpan**.\n\n"
            "Voila! Profil Kakak otomatis ter-update. Kalau mau ganti nomor HP yang terhubung ke e-Wallet, pastikan nomor barunya aktif ya! 😉"
        )
    elif intent == "ask_annual_report":
        return (
            "Wah, saya senang sekali Kakak peduli dengan transparansi! 📊✨\n\n"
            "Bagi kami, laporan penyaluran dana itu wajib hukumnya. Kakak bisa mengunduh **Laporan Keuangan & Penyaluran Tahunan** DonasiCare secara bebas.\n\n"
            "Caranya:\n"
            "Silakan kunjungi halaman utama kami, scroll ke bagian paling bawah (footer), dan klik menu **Laporan Transparansi**. Di sana Kakak bisa unduh dokumen PDF lengkap beserta dokumentasi lapangannya.\n\n"
            "Setiap rupiah yang dititipkan, pasti kami pertanggungjawabkan! 🤝"
        )
    elif intent == "ask_event_invitation":
        return (
            "Halo Kak! Wah, suatu kehormatan luar biasa bagi kami bisa diundang ke acara Kakak. 🎉\n\n"
            "Tim DonasiCare dengan senang hati terbuka untuk hadir sebagai narasumber, kolaborator, atau sekadar *sharing session* seputar gerakan sosial dan kerelawanan.\n\n"
            "Agar tim kami bisa menyesuaikan jadwal, Kakak bisa mengirimkan *Term of Reference* (ToR) atau undangan resminya ke email kami di **event@donasicare.org**. Nanti tim representatif kami akan membalas secepatnya ya! 🗓️"
        )
    elif intent == "ask_data_privacy":
        return (
            "Pertanyaan yang sangat *mindful*, Kak! Di era digital ini privasi memang nomor satu. 🔒\n\n"
            "DonasiCare menerapkan standar keamanan enkripsi *End-to-End* dan kepatuhan penuh terhadap UU Pelindungan Data Pribadi (PDP). Artinya:\n"
            "✅ Data pribadi Kakak tidak akan pernah dijual ke pihak ketiga.\n"
            "✅ Nomor HP dan Email murni hanya digunakan untuk laporan donasi.\n"
            "✅ Sistem pembayaran kami terintegrasi langsung dengan gerbang pembayaran (Payment Gateway) berlisensi Bank Indonesia.\n\n"
            "Jadi, identitas Kakak tersimpan sangat rapat dan aman di brankas digital kami! 🛡️"
        )
    elif intent == "ask_emergency_help":
        return (
            "Ya ampun, Kak! Saya ikut prihatin mendengarnya. 🥺\n\n"
            "Jika ini adalah situasi **darurat medis atau bencana alam** yang membutuhkan penanganan sangat segera, Kakak harus langsung menghubungi layanan darurat pemerintah seperti 119 (Ambulans) atau 112 (Panggilan Darurat).\n\n"
            "Namun, untuk permohonan bantuan dana *pasca-darurat*, Kakak atau perwakilan keluarga bisa mengirimkan pesan darurat ke WhatsApp Hotline khusus kami di **0811-9999-SOS** dengan menyertakan foto kondisi dan lokasi. Tim lapangan kami akan melakukan peninjauan cepat (Fast Response) dalam 24 jam! 🚑"
        )
    elif intent == "ask_collab_media":
        return (
            "Halo rekan media! Wah, senang sekali rasanya mendapat sapaan dari teman-teman pers. 📰✨\n\n"
            "Kami selalu terbuka untuk wawancara, liputan eksklusif, maupun kebutuhan *press release* seputar kegiatan sosial kemanusiaan DonasiCare.\n\n"
            "Silakan langsung hubungi tim Public Relations kami melalui:\n"
            "📧 Email: **pr@donasicare.org**\n"
            "📱 WhatsApp Humas: **0812-Media-Care**\n\n"
            "Mari bersama-sama kita sebarluaskan virus kebaikan ke seluruh penjuru negeri! 🇮🇩🎤"
        )
    elif intent == "ask_general_donation_guide":
        return (
            "Halo Kak! Tentu, saya akan bantu jelaskan secara lengkap tentang sistem donasi di platform DonasiCare. 🌟\n\n"
            "**DonasiCare** adalah *platform crowdfunding* digital yang memfasilitasi niat baik ribuan orang untuk membantu saudara kita yang sedang kesulitan. "
            "Sistem kami dirancang agar transparan, cepat, dan 100% aman.\n\n"
            "**1. Siapa saja yang dibantu?**\n"
            "Kami memiliki banyak kampanye aktif di berbagai bidang, seperti:\n"
            "• 📚 Pendidikan (Beasiswa dan fasilitas sekolah)\n"
            "• 🏥 Kesehatan (Bantuan biaya pengobatan kritis)\n"
            "• 🆘 Bencana Alam (Tanggap darurat logistik & evakuasi)\n"
            "• 🌿 Lingkungan (Program penghijauan & kelestarian alam)\n\n"
            "**2. Bagaimana Cara Berdonasi?**\n"
            "Caranya sangat praktis:\n"
            "- Pilih kampanye yang menggerakkan hati Kakak.\n"
            "- Masukkan nominal donasi (Bisa mulai dari Rp10.000 menggunakan E-Wallet).\n"
            "- Pilih metode pembayaran (GoPay, DANA, OVO, QRIS, BCA, Mandiri, dll).\n"
            "- Kakak juga bisa memilih opsi *Anonim (Hamba Allah)* jika tidak ingin nama ditampilkan.\n\n"
            "**3. Keuntungan Berdonasi di Sini?**\n"
            "• **Transparansi:** Setiap program wajib memberikan *Update Laporan* berkala berupa foto dan rincian penyaluran dana.\n"
            "• **E-Sertifikat:** Setiap donasi berhasil, Kakak akan mendapatkan e-Sertifikat penghargaan.\n"
            "• **Potongan Pajak:** Bukti donasi dari kampanye tertentu bisa digunakan sebagai pengurang PPh di SPT Tahunan.\n"
            "• **Bebas Potongan Tersembunyi:** Kami tidak menerapkan biaya admin terselubung.\n\n"
            "Apakah ada informasi spesifik yang ingin Kakak tanyakan lagi? 😊"
        )
    elif intent == "ask_donation_behalf":
        return (
            "Bisa banget, Kak! Menyedekahkan harta atas nama orang tua atau keluarga yang sudah meninggal dunia (Almarhum/Almarhumah) adalah amal jariyah yang sangat mulia. 🕊️❤️\n\n"
            "Cara melakukannya di platform kami:\n"
            "1. Saat mengisi form donasi, pada kolom **Nama Lengkap**, Kakak bisa menuliskan: *'Fulan bin Fulan (Alm)'* atau *'Hamba Allah untuk Ibunda tercinta'*.\n"
            "2. Kakak juga bisa menuliskan doa khusus di kolom **Pesan / Doa**, agar setiap orang yang membaca halaman kampanye tersebut ikut mengaminkan doa Kakak.\n\n"
            "InsyaAllah, pahalanya akan langsung mengalir kepada beliau. Aamiin. 🤲"
        )
    elif intent == "ask_donation_asset":
        return (
            "Wah, niat Kakak sungguh luar biasa! ✨ Untuk saat ini, melalui aplikasi/website DonasiCare, kami hanya memfasilitasi donasi dalam bentuk dana tunai atau transfer saldo.\n\n"
            "Namun, jika Kakak ingin mendonasikan atau mewakafkan aset bernilai tinggi (seperti emas batangan, surat berharga, tanah, kendaraan, atau properti), "
            "kami memiliki divisi khusus **Wakaf & Aset Produktif** yang siap membantu.\n\n"
            "Tim legal kami akan mendampingi proses balik nama, akad syariah, dan penyerahan aset tersebut agar sah secara hukum dan agama. "
            "Silakan hubungi konsultan wakaf kami melalui email ke: **wakaf@donasicare.org**. 🙏"
        )
    elif intent == "ask_verification_process":
        return (
            "Ini adalah pertanyaan yang kritis dan sangat kami hargai, Kak! Keamanan dana donatur adalah prioritas tertinggi DonasiCare. 🛡️\n\n"
            "Untuk mencegah kampanye fiktif atau penipuan, tim **Trust & Safety** kami melakukan verifikasi ketat:\n"
            "1. **Verifikasi Identitas:** Setiap penggalang dana wajib mengunggah KTP, Swafoto dengan KTP, dan Nomor Rekening atas nama yang sama.\n"
            "2. **Verifikasi Medis/Lapangan:** Jika kampanyenya adalah bantuan medis, penggalang dana wajib melampirkan rekam medis resmi, surat rujukan rumah sakit, dan estimasi biaya bermaterai.\n"
            "3. **Survey Langsung:** Untuk pencairan dana di atas limit tertentu, relawan lapangan kami akan melakukan *video call* atau *survey* langsung ke lokasi penerima manfaat.\n\n"
            "Kami pastikan hanya kampanye yang valid dan mendesak yang bisa tayang di *platform* kami! 🔎"
        )
    elif intent == "ask_riba_free":
        return (
            "Alhamdulillah, pertanyaan yang sangat baik, Kak! 🕌\n\n"
            "DonasiCare sangat berkomitmen untuk menjaga kehalalan aliran dana:\n"
            "1. **Rekening Penampungan Syariah:** Dana donasi, infak, dan zakat dipisahkan ke dalam rekening Bank Syariah yang terbebas dari sistem bunga (riba).\n"
            "2. **Mitra Payment Gateway:** Biaya transaksi (*payment gateway fee*) yang ditarik murni merupakan biaya layanan teknologi (ujrah), bukan bunga.\n"
            "3. **Akad yang Jelas:** Setiap pengguna yang berdonasi akan menyetujui *Syarat & Ketentuan* yang didasarkan pada akad *Tabarru'* (tolong-menolong dalam kebaikan).\n\n"
            "Jadi, Kakak bisa berdonasi, berzakat, atau berinfak dengan hati yang tenang dan berkah. ✨"
        )

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
            "Setiap penggalang dana and program juga telah melewati proses verifikasi identitas yang ketat untuk mencegah penipuan. 🔒\n\n"
            "Donasi Kakak dijamin 100% aman. Ada program yang ingin Kakak dukung hari ini? 😊"
        )



    elif intent == "ask_impact_simulation":
        text_clean = text.lower().replace(".", "").replace(",", "")
        matches = re.findall(r"(?:rp)?\s*(\d+)\s*(k|ribu|rb|juta|jt)?", text_clean)
        nom = 0
        if matches:
            for num_str, suffix in matches:
                val = int(num_str)
                if suffix in ["k", "ribu", "rb"]:
                    val *= 1000
                elif suffix in ["juta", "jt"]:
                    val *= 1000000
                elif val < 10000 and "rp" not in text.lower():
                    val *= 1000
                
                if val > nom:
                    nom = val
                
        if nom > 0:
            buku = max(1, nom // 5000)
            pensil = max(1, nom // 2000)
            makan = max(1, nom // 20000)
            air = max(1, nom // 5000)
            obat = max(1, nom // 50000)
            pohon = max(1, nom // 15000)
            
            return (
                f"Luar biasa! 🌟 Dengan donasi sebesar **Rp {nom:,}**, Kakak bisa membawa perubahan besar di berbagai sektor.\n\n"
                f"Berikut adalah estimasi rincian manfaat yang bisa disalurkan dari donasi Kakak:\n\n"
                f"📚 **Pendidikan:**\n"
                f"Menyumbangkan sekitar **{buku} buku tulis** baru atau **{pensil} buah alat tulis/pensil** "
                f"yang akan sangat membantu anak-anak di pelosok agar tetap bisa sekolah.\n\n"
                f"🆘 **Bencana Alam:**\n"
                f"Dapat dikonversi menjadi **{makan} paket makanan siap saji** yang bergizi "
                f"dan **{air} liter air bersih** untuk para pengungsi korban bencana alam.\n\n"
                f"🏥 **Kesehatan:**\n"
                f"Menyediakan **{obat} paket obat-obatan dasar & vitamin** "
                f"bagi pasien tidak mampu yang kesulitan mendapat akses medis.\n\n"
                f"🌿 **Lingkungan:**\n"
                f"Berkontribusi menanam **{pohon} bibit pohon produktif / mangrove** "
                f"yang akan menghijaukan kembali lahan kritis dan mencegah longsor.\n\n"
                f"Kakak bebas memilih ke mana dana ini akan difokuskan. Ingin menyalurkannya sekarang? 😊"
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
        
    elif intent == "choose_volunteer":
        return (
            "Wah, pilihan yang bagus! 🎉\n\n"
            "Untuk melanjutkan proses pendaftaran sebagai relawan, silakan ketik data diri Kakak dengan format berikut:\n\n"
            "**Nama Lengkap - Usia - Nomor HP - Pilihan Relawan**\n"
            "(Contoh: Budi Santoso - 25 - 08123456789 - Relawan Distribusi Pangan)"
        )
        
    elif intent == "fill_volunteer_info":
        return (
            "Terima kasih atas semangat kepedulian Kakak! ❤️ Data Kakak sudah kami catat dengan baik di sistem kami.\n\n"
            "Tim koordinator relawan kami akan segera menghubungi Kakak melalui nomor HP yang diberikan dalam waktu maksimal 2x24 jam untuk proses orientasi dan briefing.\n\n"
            "Mari bersama-sama kita wujudkan senyum bagi mereka yang membutuhkan! Jika ada pertanyaan lain, jangan ragu untuk bertanya ya."
        )
        
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

    # 6. Smart Knowledge Base Retrieval (RAG Simulation)
    campaigns = get_all_campaigns()
    prompt_lower = text.lower()
    
    HUMANIZED_STORIES = {
        1: (
            "👩‍🏫 **Kondisi di Lapangan:**\n"
            "Saat ini ada ratusan anak cerdas di pelosok yang terancam putus sekolah. "
            "Tim kami (Kak Nisa & Kak Budi) mendampingi mereka setiap minggu, memastikan seragam, SPP, dan alat tulis terpenuhi. "
            "Bantuan Kakak adalah tiket masa depan mereka untuk terus bermimpi."
        ),
        2: (
            "🆘 **Update Evakuasi Bencana:**\n"
            "Sekitar 400 keluarga masih bertahan di posko pengungsian dengan kondisi kedinginan. "
            "Tim relawan yang dikomandoi Pak Ridwan sedang bekerja siang-malam memasak di dapur umum dan menyalurkan pakaian kering serta obat-obatan. "
            "Mereka sangat membutuhkan uluran tangan kita secepatnya!"
        ),
        3: (
            "🌳 **Gerakan Penyelamatan Lahan:**\n"
            "Kondisi hulu sungai semakin rawan longsor. Bersama Mang Udin (tokoh masyarakat) dan 50 relawan lokal, "
            "kami sedang menanam pohon produktif yang kelak selain menahan longsor, buahnya bisa dijual untuk menghidupi ekonomi desa. "
            "Ini adalah tabungan amal jariyah yang terus mengalir."
        ),
        4: (
            "🏡 **Kisah Panti Asuhan:**\n"
            "Panti Asuhan ini menjadi rumah bagi 45 anak yatim piatu. Mereka diasuh dengan penuh kasih sayang oleh Bunda Rina dibantu 3 pengasuh sukarela yang menemani mereka belajar dan bermain. "
            "Saat ini, mereka sedang kesulitan memenuhi kebutuhan sembako bulanan dan atap asrama yang bocor. Bantuan Kakak akan membuat mereka merasa tidak sendirian di dunia ini. ❤️"
        )
    }
    
    knowledge_base = []
    
    # 6.1. Semua Kampanye
    for c in campaigns:
        progress = min(int((c['dana_terkumpul'] / c['target_dana']) * 100), 100) if c['target_dana'] > 0 else 0
        story = HUMANIZED_STORIES.get(c['id'], c['deskripsi'])
        
        knowledge_base.append({
            "keywords": f"{c['judul'].lower()} {c['deskripsi'].lower()} {c['kategori'].lower()} kampanye donasi program {c.get('lokasi', '').lower()} {story.lower()}",
            "response": f"📌 **{c['judul']}** ({c['kategori']})\n\n{story}\n\n📍 Lokasi: {c.get('lokasi', 'Indonesia')}\n💰 Terkumpul: {format_rupiah(c['dana_terkumpul'])} dari {format_rupiah(c['target_dana'])} ({progress}%)\n\n💡 _Jika hati Kakak tergerak, klik 'Donasi Sekarang' di menu sebelah kiri ya!_"
        })
        
    # 6.2. Statistik Website
    total_dana = get_total_donasi()
    total_donatur = get_donation_count()
    total_kampanye = get_campaign_count()
    knowledge_base.append({
        "keywords": "statistik data website jumlah donatur orang pengguna total dana uang terkumpul rupiah program kampanye berjalan",
        "response": f"📊 **Statistik DonasiCare Saat Ini:**\n\n💰 Total Dana Terkumpul: **{format_rupiah(total_dana)}**\n👥 Donatur Aktif: **{total_donatur:,} Orang**\n🎯 Program Berjalan: **{total_kampanye} Kampanye**\n\nTerima kasih kepada seluruh orang baik yang telah berkontribusi!"
    })
    
    # 6.3. Relawan / Volunteer
    knowledge_base.append({
        "keywords": "relawan volunteer gabung daftar bantu tenaga sukarelawan tugas pekerjaan lapangan",
        "response": "🙌 **Pusat Relawan (Volunteer Center)**\n\nKami memiliki berbagai misi kerelawanan, seperti:\n1. **Relawan Distribusi Pangan** (Membagikan sembako ke panti asuhan)\n2. **Guru Relawan Pelosok** (Mengajar anak-anak di daerah terpencil)\n3. **Relawan Medis Darurat** (Tenaga kesehatan untuk bencana)\n\nAnda bisa mendaftar dengan menuju ke menu **Volunteer Center** di bilah navigasi!"
    })
    
    # 6.4. Tentang Kami & Impact Tracker
    knowledge_base.append({
        "keywords": "tentang kami visi misi profil donasicare yayasan organisasi siapa alamat",
        "response": "🏢 **Tentang DonasiCare**\n\nDonasiCare adalah platform urun dana (crowdfunding) yang transparan dan terpercaya. Visi kami adalah menghubungkan kebaikan ke seluruh penjuru negeri.\nKami memastikan 100% dana tersalurkan tepat sasaran tanpa potongan tersembunyi. Anda bisa mengecek transparansi di menu **Tentang Kami**."
    })
    knowledge_base.append({
        "keywords": "impact tracker peta bantuan jejak dampak penyaluran laporan lokasi bukti",
        "response": "🗺️ **Impact Tracker & Peta Bantuan**\n\nKami memiliki fitur pelacak dampak langsung di website kami. Anda dapat melihat Peta Bantuan Interaktif yang menunjukkan di mana saja donasi telah disalurkan beserta foto laporannya. Silakan buka menu **Peta Bantuan** atau **Impact Tracker**!"
    })
    
    # Simple Scoring
    words = [w for w in prompt_lower.split() if len(w) > 3]
    if "semua" in prompt_lower or "semuanya" in prompt_lower or "semua data" in prompt_lower:
        words.extend(["kampanye", "statistik", "relawan", "tentang", "impact"])

    best_matches = []
    
    for kb in knowledge_base:
        score = sum(2 if w in kb["keywords"].split() else (1 if w in kb["keywords"] else 0) for w in words)
        if score > 0:
            best_matches.append((score, kb["response"]))
            
    if best_matches:
        best_matches.sort(key=lambda x: x[0], reverse=True)
        top_score = best_matches[0][0]
        # Jika keywordnya global spt "semua", tampilkan top 4
        limit = 4 if "semua" in prompt_lower else 2
        answers = [ans for sc, ans in best_matches if top_score - sc <= 2][:limit]
        
        reply = "🔍 Berdasarkan seluruh data di DonasiCare, ini yang bisa saya sampaikan:\n\n"
        reply += "\n\n---\n\n".join(answers)
        return reply

    # 7. Final Fallback (Jika benar-benar tidak ada keywords)
    time_greeting = _get_time_greeting()
    fallback_responses = [
        f"Hmm... {time_greeting.lower()}, maaf ya, saya kurang paham maksud Anda. 🤔\n\n"
        "Tapi tenang saja! Sekarang saya memiliki akses ke **SELURUH DATA** di website ini. Anda bebas bertanya tentang:\n"
        "• Data statistik total donasi & donatur\n"
        "• Info lengkap seluruh program kampanye\n"
        "• Cara donasi atau pembayaran\n"
        "• Cara menjadi relawan (volunteer)\n"
        "• Profil dan transparansi DonasiCare (Impact Tracker)\n\n"
        "Coba tanyakan satu per satu dengan kata kunci di atas!",
    ]
    return fallback_responses[0]

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