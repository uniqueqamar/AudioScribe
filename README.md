# AudioScribe 🎙️

Convert photos of handwritten notes into spoken audio — instantly.

---

## How it works

1. Upload a photo of your handwritten notes
2. Tesseract OCR extracts the text
3. gTTS converts it to an MP3
4. Listen directly in the browser

---

## Setup

### Prerequisites

| Tool | Install |
|------|---------|
| Node.js ≥ 18 | https://nodejs.org |
| Python ≥ 3.8 | https://python.org |
| Tesseract OCR | See below |

#### Install Tesseract

- **Windows:** https://github.com/UB-Mannheim/tesseract/wiki  
  Default path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- **macOS:** `brew install tesseract`
- **Linux:** `sudo apt install tesseract-ocr`

#### Install Python dependencies

```bash
pip install pillow pytesseract gtts
```

### Install Node dependencies

```bash
npm install
```

---

## Run

```bash
node server.js
```

Then open **http://localhost:3000** in your browser.

---

