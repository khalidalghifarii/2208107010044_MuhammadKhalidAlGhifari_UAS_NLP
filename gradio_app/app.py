import os
import tempfile
import requests
import gradio as gr
import scipy.io.wavfile
from datetime import datetime

# Tema kustom dengan warna yang lebih modern
custom_theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
    neutral_hue="slate",
    radius_size=gr.themes.sizes.radius_md,
    text_size=gr.themes.sizes.text_md,
).set(
    button_primary_background_fill="*primary_500",
    button_primary_background_fill_hover="*primary_600",
    button_primary_text_color="white",
    button_primary_border_color="*primary_500",
    button_secondary_background_fill="*neutral_100",
    block_label_background_fill="*neutral_50",
    block_title_text_color="*primary_500",
)

# Log percakapan
conversation_history = []

def voice_chat(audio, history):
    if audio is None:
        return None, history
    
    sr, audio_data = audio
    current_time = datetime.now().strftime("%H:%M:%S")

    # Tambahkan indikator loading ke history
    history.append({"role": "user", "content": "🎤 Audio terkirim", "time": current_time})
    
    # Simpan sebagai .wav
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        scipy.io.wavfile.write(tmpfile.name, sr, audio_data)
        audio_path = tmpfile.name

    # Kirim ke endpoint FastAPI
    try:
        with open(audio_path, "rb") as f:
            files = {"file": ("voice.wav", f, "audio/wav")}
            response = requests.post("http://localhost:8000/voice-chat", files=files)

        if response.status_code == 200:
            # Simpan file respons audio dari chatbot
            output_audio_path = os.path.join(tempfile.gettempdir(), "tts_output.wav")
            with open(output_audio_path, "wb") as f:
                f.write(response.content)
            
            # Update riwayat percakapan
            current_time = datetime.now().strftime("%H:%M:%S")
            history.append({"role": "assistant", "content": "🔊 Audio respons tersedia", "time": current_time})
            
            return output_audio_path, history
        else:
            # Update riwayat jika terjadi error
            current_time = datetime.now().strftime("%H:%M:%S")
            history.append({"role": "system", "content": f"❌ Error: Server mengembalikan status {response.status_code}", "time": current_time})
            return None, history
    except Exception as e:
        # Tangani error koneksi
        current_time = datetime.now().strftime("%H:%M:%S")
        history.append({"role": "system", "content": f"❌ Error: {str(e)}", "time": current_time})
        return None, history
    finally:
        # Hapus file temporary
        if os.path.exists(audio_path):
            os.unlink(audio_path)

# Fungsi untuk render riwayat percakapan
def format_history(history):
    html = ""
    for msg in history:
        role = msg["role"]
        content = msg["content"]
        time = msg["time"]
        
        if role == "user":
            html += f"""
            <div style="display: flex; margin-bottom: 10px;">
                <div style="background-color: #e0e7ff; border-radius: 12px; padding: 10px; margin-right: auto; max-width: 80%;">
                    <div style="font-weight: bold; color: #4338ca;">You</div>
                    <div>{content}</div>
                    <div style="font-size: 0.8em; text-align: right; color: #6b7280;">{time}</div>
                </div>
            </div>
            """
        elif role == "assistant":
            html += f"""
            <div style="display: flex; margin-bottom: 10px;">
                <div style="background-color: #dbeafe; border-radius: 12px; padding: 10px; margin-left: auto; max-width: 80%;">
                    <div style="font-weight: bold; color: #1e40af;">Assistant</div>
                    <div>{content}</div>
                    <div style="font-size: 0.8em; text-align: right; color: #6b7280;">{time}</div>
                </div>
            </div>
            """
        else:  # system messages
            html += f"""
            <div style="display: flex; margin-bottom: 10px; justify-content: center;">
                <div style="background-color: #fee2e2; border-radius: 12px; padding: 8px 15px; max-width: 80%; text-align: center;">
                    <div style="color: #991b1b;">{content}</div>
                    <div style="font-size: 0.8em; color: #6b7280;">{time}</div>
                </div>
            </div>
            """
    
    return html

# Fungsi untuk reset percakapan
def reset_conversation():
    return None, []

# Fungsi untuk memperbarui status recording
def update_recording_status(recording):
    if recording:
        return "🔴 Recording..."
    else:
        return "⚪ Tap to record"

# UI Gradio dengan desain yang lebih modern
with gr.Blocks(theme=custom_theme, css="""
    .container {
        max-width: 800px;
        margin: 0 auto;
    }
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    .footer {
        text-align: center;
        margin-top: 30px;
        color: #6b7280;
        font-size: 0.9em;
    }
    .chat-container {
        min-height: 300px;
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 20px;
        padding: 15px;
        border-radius: 10px;
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
    }
    #recording-status {
        font-size: 0.9em;
        text-align: center;
        margin-top: 5px;
        font-weight: 500;
    }
""") as demo:
    with gr.Column(elem_classes="container"):
        # Header
        with gr.Column(elem_classes="header"):
            gr.Markdown("# 🎙️ Voice Chatbot AI")
            gr.Markdown("Berbicara langsung ke mikrofon dan dapatkan jawaban suara dari asisten AI")
        
        # Chat container
        chat_display = gr.HTML(elem_classes="chat-container")
        
        # Audio input dan output
        with gr.Row():
            with gr.Column(scale=1):
                audio_input = gr.Audio(
                    sources="microphone", 
                    type="numpy", 
                    label="Rekam Suara",
                    elem_id="audio-input",
                    interactive=True
                )
                recording_status = gr.Markdown("⚪ Tap to record", elem_id="recording-status")
                
            with gr.Column(scale=1):
                audio_output = gr.Audio(
                    type="filepath", 
                    label="Respons Asisten",
                    elem_id="audio-output",
                    interactive=False
                )
        
        # Tombol aksi
        with gr.Row():
            submit_btn = gr.Button("💬 Kirim Pesan", variant="primary", scale=2)
            reset_btn = gr.Button("🔄 Reset Percakapan", scale=1)
        
        # State untuk menyimpan riwayat percakapan
        history_state = gr.State([])
        
        # Footer
        with gr.Row(elem_classes="footer"):
            gr.Markdown("Chatbot Suara menggunakan Whisper, Gemini AI, dan Indonesian TTS")

    # Event handlers
    submit_btn.click(
        fn=voice_chat,
        inputs=[audio_input, history_state],
        outputs=[audio_output, history_state]
    ).then(
        fn=format_history,
        inputs=[history_state],
        outputs=[chat_display]
    )
    
    reset_btn.click(
        fn=reset_conversation,
        inputs=[],
        outputs=[audio_output, history_state]
    ).then(
        fn=format_history,
        inputs=[history_state],
        outputs=[chat_display]
    )
    
    # Update status saat recording
    audio_input.start_recording(
        fn=lambda: update_recording_status(True),
        outputs=[recording_status]
    )
    
    audio_input.stop_recording(
        fn=lambda: update_recording_status(False),
        outputs=[recording_status]
    )
    
    # Initialize empty chat
    demo.load(
        fn=format_history,
        inputs=[history_state],
        outputs=[chat_display]
    )

# Jalankan aplikasi
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)