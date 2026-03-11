# OCR en Python con Tesseract

Herramienta de reconocimiento óptico de caracteres (OCR) desarrollada en Python utilizando Tesseract, con interfaz gráfica y base para procesamiento y estructuración de documentos.

El proyecto está pensado como una base extensible para:
- digitalización de documentos
- extracción de texto
- análisis visual del OCR
- futura clasificación y extracción de datos (Data Entry)

---

## Funcionalidades actuales

- OCR sobre imágenes usando Tesseract
- Interfaz gráfica con Tkinter
- Visualización de bounding boxes (detecciones OCR)
- Soporte para múltiples idiomas (Español, Inglés, Portugués, Francés)
- Preprocesamiento de imágenes (base)
- Código modular y extensible
- Exportación de texto y datos OCR

---

## En desarrollo / Próximos pasos

- Clasificación de documentos (facturas, recibos, etc.)
- Extracción estructurada de datos (CUIT, totales, fechas)
- Presets de preprocesamiento según tipo de documento
- Exportación a formatos estructurados (TXT / CSV / JSON)
- Modo Data Entry asistido

---

## Requisitos

- Python 3
- Tesseract OCR
- pytesseract
- Pillow
- Tkinter (incluido en Python)

---

## Requisitos de entrada

- Imágenes claras y legibles
- Buen contraste entre texto y fondo
- Preferentemente documentos escaneados
- Resolución adecuada (idealmente 300 DPI)

---

## Uso

```bash
python main.py