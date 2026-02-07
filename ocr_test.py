from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

# If Tesseract is not in PATH, uncomment and set the path
# pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"

image_path = "/Users/Fatima/python_project/handwriting copy.jpg"
img = Image.open(image_path)

# ---- Preprocessing ----
# 1. Convert to grayscale
img = img.convert('L')

# 2. Increase contrast
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)

# 3. Apply sharpening filter
img = img.filter(ImageFilter.SHARPEN)

# ---- OCR ----
text = pytesseract.image_to_string(img)

print("---- Extracted Text ----")
print(text)

# ---- Save text to file ----
with open("/Users/Fatima/python_project/handwriting_text.txt", "w") as f:
    f.write(text)
