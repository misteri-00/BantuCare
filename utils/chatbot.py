import re
import time
import random
import datetime
from utils.database import get_connection
from utils.campaign import get_all_campaigns, get_total_donasi, get_campaign_count, get_campaigns_by_category
from utils.helpers import format_rupiah, get_donation_count

# ═══════════════════════════════════════════════════════════════════════
# DonasiCare – Smart Chatbot Engine (Pure Python, No External API)
# Features: Intent classification, sentiment detection, context memory,
#           randomized natural responses, campaign data integration
# ═══════════════════════════════════════════════════════════════════════


# ── Intent Patterns ───────────────────────────────────────────────────
# Setiap intent memiliki beberapa pola regex untuk menangkap variasi ucapan
INTENT_PATTERNS = {
    "greeting": [
        r"\b(halo|hai|hi|hey|selamat|assalamualaikum|pagi|siang|sore|malam|helo)\b",
    ],
    "farewell": [
        r"\b(bye|dadah|sampai jumpa|terima kasih|makasih|thanks|selamat tinggal)\b",
    ],
    "ask_total_donation": [
        r"(total|berapa|jumlah).*(donasi|dana|uang|terkumpul|sumbangan)",
        r"(dana|donasi|uang).*(terkumpul|masuk|diterima|total)",
        r"sudah (berapa|terkumpul)",
    ],
    "ask_program_count": [
        r"(berapa|jumlah|ada).*(program|kampanye|kegiatan|proyek)",
        r"(program|kampanye).*(berapa|aktif|jumlah|banyak)",
    ],
    "ask_donor_count": [
        r"(berapa|jumlah|ada).*(donatur|penyumbang|orang|donor)",
        r"(donatur|penyumbang|donor).*(berapa|jumlah|banyak)",
    ],
    "search_education": [
        r"\b(pendidikan|sekolah|beasiswa|belajar|buku|anak|pelajar|murid|siswa)\b",
    ],
    "search_health": [
        r"\b(kesehatan|medis|sakit|obat|rumah sakit|klinik|dokter|gizi|nutrisi)\b",
    ],
    "search_disaster": [
        r"\b(bencana|banjir|gempa|longsor|tsunami|kebakaran|erupsi|badai|topan)\b",
    ],
    "search_environment": [
        r"\b(lingkungan|hutan|mangrove|reboisasi|sampah|polusi|laut|pantai|alam)\b",
    ],
    "ask_how_to_donate": [
        r"(cara|gimana|bagaimana|langkah|step|panduan).*(donasi|bayar|sumbang|transfer|bantu)",
        r"(donasi|bayar|sumbang).*(cara|gimana|bagaimana)",
        r"metode.*(pembayaran|bayar|donasi)",
        r"(bisa|mau|ingin|pengen).*(donasi|sumbang|bantu|bayar|berdonasi|menyumbang)",
        r"\b(berdonasi|menyumbang)\b",
    ],
    "ask_payment_method": [
        r"(metode|jenis|apa saja).*(bayar|pembayaran|transfer)",
        r"\b(gopay|ovo|dana|qris|bca|mandiri|bni|bri)\b",
        r"(bayar|transfer).*(apa|pakai|lewat|via|melalui)",
    ],
    "ask_transparency": [
        r"(transparan|laporan|bukti|audit|akuntabel|jujur)",
        r"(dana|uang|donasi).*(digunakan|disalurkan|dipakai|kemana|ke mana)",
        r"(kemana|ke mana).*(uang|dana|donasi)",
    ],
    "ask_security": [
        r"(aman|keamanan|terpercaya|penipuan|bodong|percaya)",
    ],
    "ask_impact_simulation": [
        r"(jika|kalau|misal|seandainya).*(donasi|berdonasi|menyumbang|sumbang).*(rp|Rp)?\s*(\d+|\d{1,3}(?:\.\d{3})+)",
        r"(dampak|manfaat|bantuan|apa).*(donasi|berdonasi|menyumbang|sumbang).*(rp|Rp)?\s*(\d+|\d{1,3}(?:\.\d{3})+)",
    ],
    "ask_volunteer": [
        r"\b(volunteer|relawan|sukarelawan|gabung|daftar|bergabung)\b",
        r"(jadi|mau|ingin|pengen).*(relawan|volunteer)",
    ],
    "ask_about": [
        r"(apa itu|tentang|mengenai|jelaskan).*(donasicare|platform|organisasi|yayasan)",
        r"(siapa|apa).*(donasicare|kalian|kamu|anda)",
    ],
    "ask_recommendation": [
        r"(rekomendasi|rekomen|saran|sarankan|suggest)",
        r"(program|kampanye).*(terbaik|populer|unggulan|favorit|bagus)",
        r"(mau|ingin|pengen).*(donasi|bantu|sumbang).*(apa|mana|kemana)",
    ],
    "positive_sentiment": [
        r"\b(bagus|keren|mantap|hebat|luar biasa|amazing|wow|good|great|suka|senang)\b",
    ],
    "negative_sentiment": [
        r"\b(jelek|buruk|mengecewakan|kecewa|tidak suka|benci|marah|kesal)\b",
    ],
}


def classify_intent(text: str) -> str:
    """Klasifikasikan intent dari teks pengguna menggunakan regex pattern matching."""
    text_lower = text.lower().strip()
    
    # Cek setiap intent pattern
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
    
    # Kembalikan intent dengan skor tertinggi
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


# ── Response Templates (Humanist, Empathetic, Persuasive) ──────────────────

GREETING_RESPONSES = [
    "Halo, Kak! 👋 Senang sekali bisa mengobrol dengan Anda. Saya CareBot, siap membantu menjawab pertanyaan seputar program kebaikan di DonasiCare. Ada yang bisa saya bantu hari ini? 😊",
    "Hai! Selamat datang di DonasiCare. 🌿 Saya di sini untuk menemani Anda mencari cara terbaik berbagi kebaikan. Ada program spesifik yang ingin Kakak tanyakan?",
]

FAREWELL_RESPONSES = [
    "Sama-sama! Terima kasih banyak sudah berkunjung dan peduli pada sesama, Kak! ❤️ Semoga hari Anda penuh berkah. Jangan ragu untuk kembali jika ada yang ingin ditanyakan lagi ya. 👋",
    "Terima kasih kembali atas kepedulian Anda. 🙏 Sekecil apapun kebaikan kita, pasti sangat berarti bagi mereka yang membutuhkan. Sampai jumpa lagi! ✨",
]

TRANSPARENCY_RESPONSES = [
    "DonasiCare berkomitmen 100% transparan! 📊\n\n"
    "• Setiap donasi tercatat di sistem kami secara real-time\n"
    "• Laporan penggunaan dana bisa dilihat di halaman **Transparansi**\n"
    "• Kami memastikan dana sampai ke penerima manfaat yang tepat\n"
    "• Audit dilakukan secara berkala untuk menjaga akuntabilitas\n\n"
    "Anda bisa mengecek dashboard transparansi kami kapan saja!",
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
    """Dapatkan sapaan berdasarkan waktu saat ini."""
    hour = datetime.datetime.now().hour
    if hour < 11:
        return "Selamat pagi"
    elif hour < 15:
        return "Selamat siang"
    elif hour < 18:
        return "Selamat sore"
    return "Selamat malam"


def _build_donation_guide() -> str:
    """Bangun panduan donasi yang informatif."""
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
    """Bangun informasi metode pembayaran."""
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
    """Bangun respons rekomendasi kampanye dari database."""
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
    """Bangun respons rekomendasi umum (top 3 program)."""
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


def generate_smart_response(prompt: str, chat_history: list = None) -> str:
    """
    Mesin respons utama chatbot DonasiCare.
    Mengklasifikasi intent, mempertimbangkan konteks, dan menghasilkan jawaban dinamis.
    """
    intent = classify_intent(prompt)
    mood = detect_mood(prompt)
    
    # Jika mood negatif terdeteksi, prioritaskan empati
    if mood == "negative" and intent == "unknown":
        intent = "negative_sentiment"
    elif mood == "positive" and intent == "unknown":
        intent = "positive_sentiment"
        
    # Variasi kata pengantar natural
    fillers_info = ["Tentu saja! ", "Baiklah, ", "Siap! ", "Oh, tentu bisa. ", "Ini dia detailnya: ", "Mari saya jelaskan. "]
    fillers_search = ["Hmm, sebentar ya saya carikan... 🤔\n\n", "Beri saya waktu sejenak untuk mengecek... 🔍\n\n", "Wah, niat yang sangat mulia! Ini beberapa daftarnya:\n\n"]
    
    # ── Build response berdasarkan intent ──
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
    
    elif intent == "search_education":
        return random.choice(fillers_search) + _build_campaign_response("Pendidikan", "📚 Berikut program **pendidikan** yang sedang membutuhkan bantuan:")
    
    elif intent == "search_health":
        return random.choice(fillers_search) + _build_campaign_response("Kesehatan", "🏥 Berikut program **kesehatan** yang sedang berjalan:")
    
    elif intent == "search_disaster":
        return random.choice(fillers_search) + _build_campaign_response("Bencana Alam", "🆘 Berikut program **bantuan bencana** darurat:")
    
    elif intent == "search_environment":
        return random.choice(fillers_search) + _build_campaign_response("Lingkungan", "🌿 Berikut program **lingkungan** yang bisa didukung:")
    
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
        # Ekstrak nominal dari teks
        matches = re.findall(r"(?:rp|Rp)?\s*(\d{1,3}(?:\.\d{3})*|\d+)", prompt.lower())
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
    
    # ── Fallback: coba cari keyword di nama kampanye ──
    campaigns = get_all_campaigns()
    prompt_lower = prompt.lower()
    matched = [c for c in campaigns if any(word in c['judul'].lower() for word in prompt_lower.split() if len(word) > 3)]
    
    if matched:
        response = random.choice(["Sepertinya saya menemukan sesuatu yang pas dengan pencarian Anda:\n\n", "Coba lihat beberapa program ini, mungkin sesuai dengan maksud Anda:\n\n"])
        for c in matched[:2]:
            progress = min(int((c['dana_terkumpul'] / c['target_dana']) * 100), 100) if c['target_dana'] > 0 else 0
            response += f"📌 **{c['judul']}** ({c['kategori']})\n"
            response += f"   Terkumpul: {format_rupiah(c['dana_terkumpul'])} dari {format_rupiah(c['target_dana'])} ({progress}%)\n\n"
        response += "Untuk informasi lebih lengkap, Anda bisa cek di halaman **Program Donasi** ya."
        return response
    
    # ── Final fallback ──
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


def stream_text(text: str, delay_min: float = 0.01, delay_max: float = 0.04):
    """Generator untuk efek mengetik (typing effect) di Streamlit dengan jeda acak agar natural."""
    for word in text.split(" "):
        yield word + " "
        # Berikan jeda lebih lama layaknya orang sedang berpikir/berhenti di tanda baca
        if word.endswith(".") or word.endswith("!") or word.endswith("?") or word.endswith("\n"):
            time.sleep(random.uniform(delay_min * 8, delay_max * 8))
        elif word.endswith(",") or word.endswith(":"):
            time.sleep(random.uniform(delay_min * 4, delay_max * 4))
        else:
            time.sleep(random.uniform(delay_min, delay_max))


# ── Database helpers ──────────────────────────────────────────────────

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