# DonasiCare - Platform Donasi Terpercaya 💚

DonasiCare adalah sebuah aplikasi berbasis web yang dibangun menggunakan **Streamlit**. Aplikasi ini memfasilitasi program donasi dengan berbagai fitur seperti:
- **Menu Utama**: Informasi program donasi, AI Assistant, dan donasi langsung.
- **Informasi**: Transparansi dana, program relawan, dan tentang kami.
- **AI Assistant**: Chatbot donasi, rekomendasi minat, edukasi sosial, dan generator kampanye berbasis AI.

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

Ikuti langkah-langkah di bawah ini untuk menjalankan project ini di komputer Anda:

### 1. Clone Repository (Jika dari GitHub)
Buka terminal/Command Prompt Anda, kemudian jalankan:
```bash
git clone https://github.com/username-anda/DonasiCare.git
cd DonasiCare
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)
Untuk mengisolasi dependensi, buat dan aktifkan virtual environment:
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependensi
Aplikasi ini membutuhkan beberapa library Python (terutama `streamlit`). Jalankan perintah berikut untuk menginstall semuanya:
```bash
pip install -r requirements.txt
```
*(Jika file `requirements.txt` belum tersedia, Anda cukup menjalankan `pip install streamlit`)*

### 4. Jalankan Aplikasi
Setelah dependensi terinstall, jalankan aplikasi Streamlit dengan perintah:
```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser default Anda melalui alamat `http://localhost:8501`.

## 📁 Struktur Folder
```text
DonasiCare/
├── app.py                 # File utama untuk menjalankan aplikasi
├── pages/                 # Halaman-halaman fitur aplikasi (Home, AI Assistant, dll)
├── utils/                 # Kumpulan fungsi bantuan (database, helpers, dll)
├── assets/                # Aset gambar atau file statis lainnya
├── database/              # Penyimpanan database (misal SQLite)
├── requirements.txt       # Daftar package Python yang dibutuhkan
└── README.md              # Dokumentasi ini
```

## 🛠️ Teknologi yang Digunakan
- **Python 3.x**
- **Streamlit** (Frontend & Routing)
- **SQLite** (Database default - untuk riwayat chatbot/kampanye)
