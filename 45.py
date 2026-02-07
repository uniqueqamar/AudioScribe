import streamlit as st
from gtts import gTTS
import re
import os

st.title("AudioScribe 🎧")
st.write("Convert your notes into audio for hands-free learning")

# Text input (this will later be replaced by OCR output)
text = st.text_area(
    "Text to speak",
    "This is a test of the AudioScribe audio system."
)

# Speed control
speed = st.selectbox(
    "Choose reading speed",
    ["Normal", "Slow"]
)

# Convert button
if st.button("Convert to Audio"):
    if text.strip() == "":
        st.warning("Please enter some text first.")
    else:
        # Clean the text
        clean_text = re.sub(r'\s+', ' ', text).strip()

        # Speed handling (gTTS supports slow=True/False)
        slow_mode = True if speed == "Slow" else False

        # Convert text to audio
        tts = gTTS(clean_text, slow=slow_mode)
        tts.save("audio.mp3")

        st.success("🎧 Audio ready!")
        audio_file = open("audio.mp3", "rb")
        st.audio(audio_file, format="audio/mp3")

# Repeat button (plays last generated audio)
if os.path.exists("audio.mp3"):
    if st.button("🔁 Repeat Audio"):
        audio_file = open("audio.mp3", "rb")
        st.audio(audio_file, format="audio/mp3")
