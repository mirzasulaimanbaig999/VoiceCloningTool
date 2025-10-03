import streamlit as st
import openai
from pathlib import Path

st.title("🎙️ VoiceCloningTool (OpenAI TTS)")

# Load key from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Upload sample voice (saved but not used by OpenAI yet)
voice_file = st.file_uploader("📂 Upload your voice sample (MP3/WAV)", type=["mp3", "wav"])

# Enter text
text = st.text_area("✍️ Enter text you want spoken")

if st.button("🎤 Generate Audio"):
    if not text.strip():
        st.error("Please enter some text.")
    else:
        out_file = Path("output.mp3")

        # Generate narration using OpenAI TTS
        with openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="sage",   # alloy, verse, sage, shimmer
            input=text
        ) as response:
            response.stream_to_file(out_file)

        # Play & download
        st.audio(str(out_file))
        with open(out_file, "rb") as f:
            st.download_button("⬇️ Download Audio", f, file_name="output.mp3")
