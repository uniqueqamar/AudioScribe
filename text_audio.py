import streamlit as st
from gtts import gTTS
import re

st.set_page_config(page_title="AudioScribe", layout="centered")

st.title("AudioScribe 🎧")
st.write("Listen to your notes with flexible controls")

# ---------- Session state ----------
if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "index" not in st.session_state:
    st.session_state.index = 0

# ---------- Input ----------
text = st.text_area(
    "Enter text (this will come from OCR later)",
    placeholder="Paste your notes here..."
)

speed = st.selectbox(
    "Speech speed",
    ["Slow", "Normal", "Fast"]
)

# ---------- Helpers ----------
def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def split_into_chunks(text, size):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

def chunk_size_for_speed(speed):
    if speed == "Slow":
        return 8
    elif speed == "Normal":
        return 15
    else:  # Fast
        return 30

def play_audio(text_chunk, speed):
    tts = gTTS(text_chunk, slow=(speed == "Slow"))
    tts.save("audio.mp3")
    st.audio("audio.mp3")

# ---------- Convert ----------
if st.button("▶ Convert & Play"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        cleaned = clean_text(text)
        size = chunk_size_for_speed(speed)

        st.session_state.chunks = split_into_chunks(cleaned, size)
        st.session_state.index = 0

        play_audio(st.session_state.chunks[0], speed)

# ---------- Controls ----------
if st.session_state.chunks:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⏪ Rewind 5s"):
            if st.session_state.index > 0:
                st.session_state.index -= 1
                play_audio(
                    st.session_state.chunks[st.session_state.index],
                    speed
                )

    with col2:
        if st.button("⏩ Forward 5s"):
            if st.session_state.index < len(st.session_state.chunks) - 1:
                st.session_state.index += 1
                play_audio(
                    st.session_state.chunks[st.session_state.index],
                    speed
                )

    st.info(
        f"Playing section {st.session_state.index + 1} of {len(st.session_state.chunks)}"
    )
