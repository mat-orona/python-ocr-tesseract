#OCR (Reconocimiento Óptico de Caracteres)

import pytesseract
from function import *
from gui import *
from PIL import Image
#----------------------------------------------------MAIN
if __name__ == "__main__":
    #OCR tesseract.exe para que lo ejecute
    exe()
    ini_gui()
    #OCR (Reconocimiento Óptico de Caracteres) ~ para usar la funcion
    text = ocr_recognition("prueba.png","spa")


#print(text)
