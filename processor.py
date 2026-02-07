import sys
import os
import re
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from gtts import gTTS
# Import your cleaning logic if it's in a separate file
# from clean_text import clean_ocr_text

def process_notes(image_path, speed_mode="Normal"):
    try:
        # 1. OCR Preprocessing
        img = Image.open(image_path)
        img = img.convert('L')
        img = ImageEnhance.Contrast(img).enhance(2)
        img = img.filter(ImageFilter.SHARPEN)
        
        # 2. Extract Text
        raw_text = pytesseract.image_to_string(img)

        # 3. Clean Text (Using logic from clean_audio.py/clean_text.py)
        # This removes extra whitespace and newlines for smoother audio
        clean_text = re.sub(r'\s+', ' ', raw_text).strip()
        
        if not clean_text:
            clean_text = "No text detected in the image."

        # 4. Handle Speed (Logic from clean_audio.py)
        is_slow = True if speed_mode == "Slow" else False

        # 5. Generate Audio
        audio_path = image_path + ".mp3"
        tts = gTTS(text=clean_text, slow=is_slow)
        tts.save(audio_path)

        # 6. Success Output (This is what Node.js reads)
        print(f"{clean_text}|{audio_path}")

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Check for both image path and speed arguments
    if len(sys.argv) > 1:
        img_arg = sys.argv[1]
        speed_arg = sys.argv[2] if len(sys.argv) > 2 else "Normal"
        process_notes(img_arg, speed_arg)
    else:
        sys.exit(1)