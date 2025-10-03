import streamlit as st
import openai
from pathlib import Path

# ---- Password protection (just like VoiceAI) ----
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 VoiceCloningTool Login")
    password = st.text_input("Enter Password", type="password")
    if st.button("Login"):
        if password == st.secrets["APP_PASSWORD"]:
            st.session_state.authenticated = True
            st.success("✅ Access granted")
            st.rerun()
        else:
            st.error("❌ Incorrect password")
    st.stop()

# ---- Main App (only visible after login) ----
st.title("🎙️ VoiceCloningTool (OpenAI TTS)")

# Load OpenAI Key from Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Upload voice sample (stored, but not used yet)
voice_file = st.file_uploader("📂 Upload your voice sample (MP3/WAV)", type=["mp3", "wav"])

# Enter text
text = st.text_area("✍️ Enter text you want spoken")

# Generate Audio
if st.button("🎤 Generate Audio"):
    if not text.strip():
        st.error("Please enter some text.")
    else:
        out_file = Path("output.mp3")

        # Generate audio using OpenAI TTS
        with openai.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="sage",   # options: alloy, verse, sage, shimmer
            input=text
        ) as response:
            response.stream_to_file(out_file)

        # Show result
        st.audio(str(out_file))
        with open(out_file, "rb") as f:
            st.download_button("⬇️ Download Audio", f, file_name="output.mp3")
