import streamlit as st
from pathlib import Path
import subprocess

st.title("🎙️ VoiceCloningTool")

# Create folders
uploads_path = Path("uploads")
output_path = Path("output")
uploads_path.mkdir(exist_ok=True)
output_path.mkdir(exist_ok=True)

# Step 1: Upload sample voice
voice_file = st.file_uploader("📂 Upload your voice sample (min 5 mins, MP3/WAV)", type=["mp3", "wav"])

# Step 2: Enter text
text = st.text_area("✍️ Enter text you want spoken in your cloned voice")

# Step 3: Generate audio
if st.button("🎤 Generate Cloned Audio"):
    if not voice_file:
        st.error("Please upload a voice sample first.")
    elif not text.strip():
        st.error("Please enter some text.")
    else:
        # Save uploaded file
        file_path = uploads_path / "voice_sample.mp3"
        with open(file_path, "wb") as f:
            f.write(voice_file.read())

        # Output file path
        out_file = output_path / "output.wav"

        # Run Coqui TTS command
        subprocess.run([
            "tts", 
            "--model_name", "tts_models/multilingual/multi-dataset/your_tts",
            "--speaker_wav", str(file_path),
            "--text", text,
            "--out_path", str(out_file)
        ])

        # Play & download result
        audio_bytes = open(out_file, "rb").read()
        st.audio(audio_bytes, format="audio/wav")
        st.download_button("⬇️ Download Cloned Audio", audio_bytes, file_name="cloned_voice.wav")
