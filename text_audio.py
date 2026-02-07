import sys
import os
import re
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from gtts import gTTS

# --- ADD THIS IF IT CRASHES ON WINDOWS ---
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def clean_ocr_text(text):
    text = re.sub(r'\s+', ' ', text)
    # Keeping basic punctuation so the audio sounds natural
    text = re.sub(r'[^a-zA-Z0-9.,!? ]', '', text)
    return text.strip()

def run_full_flow(image_path, speed_mode="Normal"):
    try:
        # Check if file exists before processing
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at: {image_path}")

        # 1. OCR PROCESSING
        img = Image.open(image_path)
        img = img.convert('L')
        img = ImageEnhance.Contrast(img).enhance(2)
        img = img.filter(ImageFilter.SHARPEN)
        
        raw_text = pytesseract.image_to_string(img)
        
        # 2. TEXT CLEANING
        cleaned_text = clean_ocr_text(raw_text)
        
        if not cleaned_text:
            cleaned_text = "The OCR could not detect any readable text."

        # 3. AUDIO GENERATION
        is_slow = True if speed_mode.lower() == "slow" else False
        
        # Use absolute path for audio to avoid permission issues
        audio_output_path = os.path.abspath(image_path + ".mp3")
        
        tts = gTTS(text=cleaned_text, slow=is_slow)
        tts.save(audio_output_path)

        # 4. FINAL OUTPUT (Node.js reads this)
        # Use a unique separator that won't appear in text
        print(f"{cleaned_text}|{audio_output_path}")
        sys.stdout.flush() # Ensure Node.js gets the data immediately

    except Exception as e:
        sys.stderr.write(f"PYTHON_ERROR: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
        # Default to Normal if speed is missing
        speed = sys.argv[2] if len(sys.argv) > 2 else "Normal"
        run_full_flow(img_path, speed)
    else:
        sys.stderr.write("Usage: python text_audio.py <image_path> <speed>\n")
        sys.exit(1)