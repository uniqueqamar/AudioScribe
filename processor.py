import sys
import os
import re
from gtts import gTTS

# 1. Integration of your cleaning logic
def clean_ocr_text(text):
    # Removes extra spaces, newlines, and weird symbols
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,!? ]', '', text)
    text = re.sub(r'\s+([.,!?])', r'\1', text)
    return text.strip()

def process_file(file_path):
    try:
        # 2. OCR STEP (Placeholder)
        # In the future, you will put your Pytesseract code here.
        # For now, we use a sample text to ensure the "Audio" part works.
        raw_text = "Analysis complete. This audio was generated from your uploaded notes using Scriptify's neural voice engine."

        # 3. CLEANING STEP
        cleaned_text = clean_ocr_text(raw_text)

        # 4. AUDIO GENERATION STEP
        # We save the MP3 in the same 'uploads' folder as the image
        audio_filename = file_path + ".mp3"
        tts = gTTS(text=cleaned_text, lang='en', slow=False)
        tts.save(audio_filename)

        # 5. THE CRITICAL OUTPUT
        # Node.js is listening for this exact print format
        print(f"{cleaned_text}|{audio_filename}")

    except Exception as e:
        # If something fails, send the error to stderr so Node.js sees it
        sys.stderr.write(str(e))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        sys.stderr.write("No file path provided to Python script.")
        sys.exit(1)