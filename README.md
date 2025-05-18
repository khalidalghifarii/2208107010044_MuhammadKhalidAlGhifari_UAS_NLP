# 🤖 Indonesian Voice Chatbot AI – STT, Gemini LLM, TTS Integration

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistem Chatbot Suara Berbahasa Indonesia**

*Proyek Ujian Akhir Semester - Pemrosesan Bahasa Alami*  
*Jurusan Informatika - Universitas Syiah Kuala*

</div>

## 📝 Deskripsi Proyek

Proyek ini merupakan implementasi sistem asisten virtual berbasis suara yang memungkinkan pengguna berkomunikasi secara langsung melalui interface berbasis web. Sistem ini menggabungkan teknologi Speech-to-Text (STT), Large Language Model (LLM), dan Text-to-Speech (TTS) untuk menghasilkan pengalaman interaksi yang natural dalam Bahasa Indonesia.  Sistem akan mengenali suara pengguna, mengubahnya menjadi teks (Speech-to-Text), memprosesnya menggunakan model bahasa besar (Gemini API), lalu mengubah hasil jawabannya kembali menjadi suara (Text-to-Speech).

## ⭐ Kemampuan Sistem

- 🎤 Menangkap dan memproses input suara pengguna melalui antarmuka web
- 🔍 Mengkonversi input suara menjadi teks dengan Whisper.cpp
- 💡 Memproses pertanyaan dan menghasilkan respon cerdas dengan Gemini API
- 🔊 Menghasilkan respons suara yang natural dalam Bahasa Indonesia menggunakan Coqui TTS
- 📱 Interface pengguna yang modern dan responsif dengan Gradio
- 💾 Menyimpan riwayat percakapan untuk pengalaman yang berkesinambungan

## 🧰 Teknologi Pendukung

Sistem ini mengintegrasikan berbagai teknologi modern:

- **Pengenalan Suara:** [Whisper.cpp](https://github.com/ggml-org/whisper.cpp) - Implementasi efisien dari model Whisper OpenAI
- **Pemrosesan Bahasa:** [Gemini API](https://ai.google.dev/) - LLM canggih dari Google untuk pemahaman konteks
- **Sintesis Suara:** [Indonesian TTS](https://github.com/Wikidepia/indonesian-tts) - Model Coqui TTS yang dioptimalkan untuk Bahasa Indonesia
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) - Framework Python modern untuk API
- **Frontend:** [Gradio](https://www.gradio.app/) - Library untuk interface web interaktif

## 📲 Cara Penggunaan

1. Akses aplikasi web Gradio
2. Tekan tombol mikrofon untuk merekam pertanyaan dalam Bahasa Indonesia
3. Tunggu beberapa saat untuk pemrosesan
4. Dengarkan respons audio dari asisten virtual

## 📋 Persyaratan Sistem

- Python 3.9+
- Pip (Package Installer for Python)
- Git
- CMake (untuk kompilasi Whisper.cpp)
- C++ Compiler (GCC atau Visual Studio Build Tools)
- API Key Google Gemini

## ⚙️ Petunjuk Instalasi

> **Catatan:** Repository ini tidak termasuk folder `whisper.cpp`, `coqui_utils`, dan file `.env` karena ukurannya yang besar dan alasan keamanan. Komponen-komponen ini perlu dikonfigurasi secara terpisah.

### 1. Clone Repository

```bash
git clone https://github.com/khalidalghifarii/2208107010044_MuhammadKhalidAlGhifari_UAS_NLP.git
cd 2208107010044_MuhammadKhalidAlGhifari_UAS_NLP
```

### 2. Persiapan Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Untuk Linux/macOS
# atau
venv\Scripts\activate  # Untuk Windows
```

### 3. Instalasi Dependensi

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Whisper.cpp

```bash
git clone https://github.com/ggml-org/whisper.cpp.git
cd whisper.cpp

# Kompilasi
make

# Download model (rekomendasi: large-v3-turbo)
bash ./models/download-ggml-model.sh large-v3-turbo

# Kembali ke direktori proyek
cd ..
```

### 5. Konfigurasi Coqui TTS

```bash
# Buat direktori untuk model TTS
mkdir -p coqui_utils

# Download model TTS Indonesia 
# Dari https://github.com/Wikidepia/indonesian-tts/releases
```

Setelah download, ekstrak dan pindahkan file-file berikut ke folder `coqui_utils`:
- `checkpoint_1260000-inference.pth`
- `config.json`
- `speakers.pth`
- File model lainnya yang diperlukan

### 6. Setup API Gemini

1. Dapatkan API key dari [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Buat file `.env` di direktori utama:

```
GEMINI_API_KEY=your_api_key_here
```

## 🏗️ Struktur Direktori

```
📂 Repository/
├── 📂 app/
│   ├── 📂 coqui_utils/            # Model TTS (perlu dikonfigurasi)
│   ├── 📂 whisper.cpp/            # Library STT (perlu dikonfigurasi)
│   ├── 📄 chat_history.json       # Penyimpanan riwayat chat
│   ├── 📄 llm.py                  # Integrasi dengan Gemini API
│   ├── 📄 main.py                 # Endpoint utama FastAPI
│   ├── 📄 stt.py                  # Modul Speech-to-Text
│   └── 📄 tts.py                  # Modul Text-to-Speech
├── 📂 gradio_app/
│   └── 📄 app.py                  # Antarmuka pengguna dengan Gradio
├── 📄 .env                        # Konfigurasi API keys (perlu dibuat)
├── 📄 .gitignore                  # Pengecualian file untuk git
├── 📄 README.md                   # Dokumentasi proyek
└── 📄 requirements.txt            # Daftar dependensi
```

## 👨‍💻 Pengembang

**Mahasiswa:**
- Muhammad Khalid Al Ghifari

## 🎬 Demo Aplikasi

Tonton demonstrasi aplikasi di link berikut:
[YouTube – Voice Chatbot Demo](https://youtu.be/7pH8LCto-P4)

## 🔗 Postingan LinkedIn

[Selengkapnya tentang proyek ini di LinkedIn](https://www.linkedin.com/posts/muhammad-khalid-al-ghifari-048a7b27a_github-khalidalghifarii2208107010044muhammadkhalidalghifariuasnlp-activity-7329848822656913408-nKe3?utm_source=share&utm_medium=member_desktop&rcm=ACoAAEQlWXgBuRRIAxc0LnbxaW_3JSGwk49YdKM) 


## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).



