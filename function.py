import pytesseract
from PIL import Image
from image_processing import preprocess_image

def exe():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_recognition(filename, lang="spa+eng"):
    img = Image.open(filename)
    img_proc = preprocess_image(img)
    
    bbox_data = pytesseract.image_to_data(
    img_proc,
    lang=lang,
    config="--oem 3 --psm 6",
    output_type=pytesseract.Output.DICT)
    
    text_data = pytesseract.image_to_string(img, lang=lang)
    filas = text_data.splitlines()
    csv_data = [fila.split() for fila in filas]
    
    info_data = pytesseract.image_to_data(img, lang=lang)
    
    #bbox_data = pytesseract.image_to_data(img,output_type=pytesseract.Output.DICT)
    
    print("=== TEXTO DETECTADO ===")
    return text_data,csv_data,info_data,bbox_data
