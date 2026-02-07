import re

def clean_ocr_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,!? ]', '', text)
    text = re.sub(r'\s+([.,!?])', r'\1', text)
    return text.strip()


from clean_text import clean_ocr_text

sample = "This   is\n a test @@@ with   weird ### symbols!"
print(clean_ocr_text(sample))
