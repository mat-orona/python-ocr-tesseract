# OCR en Python con Tesseract

Herramienta de reconocimiento óptico de caracteres (OCR) desarrollada en Python utilizando Tesseract, con interfaz gráfica y enfoque en extracción estructurada de datos.

El proyecto está pensado como una base extensible para:
- digitalización de documentos
- extracción de texto
- análisis visual del OCR
- futura clasificación y estructuración de datos (Data Entry asistido)

---

## Funcionalidades actuales

- OCR sobre imágenes usando Tesseract
- Interfaz gráfica con Tkinter
- Visualización de bounding boxes del OCR
- Delimitación manual de zonas de reconocimiento por campo
- Extracción de texto por campos definidos (formularios)
- Soporte para múltiples idiomas:
  - Español
  - Inglés
  - Portugués
  - Francés
- Arquitectura modular y extensible
- Base para exportación estructurada (CSV / JSON)
---
## Estado actual

Actualmente el sistema permite:

cargar una imagen

visualizar detecciones OCR

delimitar zonas específicas de lectura

extraer texto estructurado por campo

generar representaciones CSV en memoria (string)

## Requisitos
Python 3

Tesseract OCR

pytesseract

Pillow

Tkinter (incluido en Python)
---
## Arquitectura del proyecto

- `gui.py`  
  Interfaz gráfica y control del flujo de trabajo.

- `function.py`  
  Lógica de OCR general y OCR por campos.

- `fields_map/`  
  Definición de formularios y zonas de reconocimiento por tipo de documento.
  Cada formulario define sus propios campos y coordenadas.

Ejemplo:
```python
FIELDS = {
    "apellido": (x, y, width, height),
    "nombre": (x, y, width, height),
    "dni": (x, y, width, height)
}
