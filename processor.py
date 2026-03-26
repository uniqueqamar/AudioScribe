import sys
import os
import re
import platform
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from gtts import gTTS

# ── Auto-detect Tesseract path ───────────────────────────────
if platform.system() == "Windows":
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    # If not found, pytesseract will try PATH — user may have it there
else:
    # On macOS/Linux tesseract is usually on PATH already; no override needed
    pass


def process_notes(image_path, speed_mode="Normal"):
    try:
        # 1. Validate image exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        # 2. OCR Pre-processing
        img = Image.open(image_path)
        img = img.convert("L")                          # grayscale
        img = ImageEnhance.Contrast(img).enhance(2)     # boost contrast
        img = img.filter(ImageFilter.SHARPEN)            # sharpen

        # 3. Extract text
        raw_text = pytesseract.image_to_string(img)

        # 4. Clean text
        clean_text = re.sub(r"\s+", " ", raw_text).strip()
        if not clean_text:
            clean_text = "No text could be detected in the image."

        # 5. Speed setting
        is_slow = speed_mode.lower() == "slow"

        # 6. Generate audio
        audio_path = image_path + ".mp3"
        tts = gTTS(text=clean_text, slow=is_slow)
        tts.save(audio_path)

        # 7. Output: text|audio_path  (Node.js reads this)
        print(f"{clean_text}|{audio_path}")

    except Exception as e:
        sys.stderr.write(f"Error: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python processor.py <image_path> [Normal|Slow]\n")
        sys.exit(1)

    img_arg = sys.argv[1]
    speed_arg = sys.argv[2] if len(sys.argv) > 2 else "Normal"
    process_notes(img_arg, speed_arg)
