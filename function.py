import pytesseract
from PIL import Image


def exe():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_recognition(filename, lang="spa"):
    img = Image.open(filename)
    text = pytesseract.image_to_string(img, lang=lang)
    return text, print("=== TEXTO DETECTADO ===")
