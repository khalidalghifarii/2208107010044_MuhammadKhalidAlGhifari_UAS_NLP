import os
import google.generativeai as genai
from google.generativeai import GenerationConfig
from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini-1.5-pro"  

# TODO: Ambil API key dari file .env
# Gunakan os.getenv("NAMA_ENV_VARIABLE") untuk mengambil API Key dari file .env.
# Pastikan di file .env terdapat baris: GEMINI_API_KEY=your_api_key
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_HISTORY_FILE = os.path.join(BASE_DIR, "chat_history.json")

# Prompt sistem yang digunakan untuk membimbing gaya respons LLM
system_instruction = """
You are a responsive, intelligent, and fluent virtual assistant who communicates in Indonesian.
Your task is to provide clear, concise, and informative answers in response to user queries or statements spoken through voice.

Your answers must:
- Be written in polite and easily understandable Indonesian.
- Be short and to the point (maximum 2–3 sentences).
- Avoid repeating the user's question; respond directly with the answer.

Example tone:
User: Cuaca hari ini gimana?
Assistant: Hari ini cuacanya cerah di sebagian besar wilayah, dengan suhu sekitar 30 derajat.

User: Kamu tahu siapa presiden Indonesia?
Assistant: Presiden Indonesia saat ini adalah Joko Widodo.

If you're unsure about an answer, be honest and say that you don't know.
"""

# TODO: Inisialisasi klien Gemini dan konfigurasi prompt
# Gunakan genai.Client(api_key=...) untuk membuat klien.
# Gunakan types.GenerateContentConfig(system_instruction=...) untuk membuat konfigurasi awal.
# Jika ingin melihat contoh implementasi, baca dokumentasi resmi Gemini:
# https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started.ipynb

# Konfigurasi API dan Model
genai.configure(api_key=GOOGLE_API_KEY)

# Membuat konfigurasi generasi
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 200,
}

# Inisialisasi model
model = genai.GenerativeModel(
    model_name=MODEL,
    generation_config=generation_config
)

# Inisialisasi chat session
chat = model.start_chat(history=[])

# Fungsi untuk menyimpan/memuat riwayat chat
def save_chat_history(current_chat):
    # Simplified version - just to maintain functionality
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write(str(current_chat))

def load_chat_history():
    # Simplified to avoid compatibility issues
    return model.start_chat(history=[])

# Kirim prompt ke LLM dan kembalikan respons teks
def generate_response(prompt: str) -> str:
    try:
        # Menggunakan model langsung untuk mendapatkan respons
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "Maaf, saya tidak dapat menghasilkan respons untuk pertanyaan tersebut."
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return f"[ERROR] {str(e)}"