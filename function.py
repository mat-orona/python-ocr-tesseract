import pytesseract
from PIL import Image
from fields_map.ini_form import FORMULARIOS
import csv
import io
def exe():
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#nuevo motor de OCR con Fields o cuadros preseleccionados para distintos formularios
def ocr_by_fields(filename, fields, lang="spa"):
    img = Image.open(filename)
    results = {}

    for field_name, (x, y, w, h) in fields.items():
        region = img.crop((x, y, x + w, y + h))

        text = pytesseract.image_to_string(
            region,
            lang=lang,
            config="--psm 7 --oem 3"
        ).strip()

        results[field_name] = text

    return results

def forms_to_csv_string(forms_data):
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["campo", "valor"])
    for campo, valor in forms_data.items():
        writer.writerow([campo, valor])

    return output.getvalue()
