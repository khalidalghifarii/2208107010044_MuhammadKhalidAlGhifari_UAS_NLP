import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import tempfile
import uuid

# Import komponen backend
from app.stt import transcribe_speech_to_text
from app.llm import generate_response
from app.tts import transcribe_text_to_speech

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="Voice Chatbot API")

@app.get("/")
async def root():
    return {"message": "Voice Chatbot API is running!"}

@app.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    """
    Endpoint utama untuk menerima audio, menjalankan pipeline STT -> LLM -> TTS,
    dan mengembalikan audio respons.
    """
    # Simpan file audio yang dikirimkan
    audio_content = await file.read()
    
    # Langkah 1: Speech-to-Text (STT)
    print("[INFO] Proses transkripsi suara ke teks...")
    transcription = transcribe_speech_to_text(audio_content, file_ext=".wav")
    print(f"[INFO] Hasil transkripsi: {transcription}")
    
    # Langkah 2: Large Language Model (LLM)
    print("[INFO] Mengirim teks ke LLM...")
    llm_response = generate_response(transcription)
    print(f"[INFO] Respons LLM: {llm_response}")
    
    # Langkah 3: Text-to-Speech (TTS)
    print("[INFO] Mengkonversi respons ke suara...")
    tts_output_path = transcribe_text_to_speech(llm_response)
    print(f"[INFO] File audio respons: {tts_output_path}")
    
    # Mengembalikan file audio hasil TTS
    return FileResponse(
        path=tts_output_path,
        media_type="audio/wav",
        filename="response.wav"
    )