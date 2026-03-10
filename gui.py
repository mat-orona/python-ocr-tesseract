import tkinter as tk

# Importa herramientas para abrir archivos y mostrar mensajes
from tkinter import filedialog, messagebox

# Importa la función OCR desde el archivo function.py
from function import ocr_recognition
from PIL import Image, ImageTk


IDIOMAS = {
    "Español": "spa",
    "Inglés": "eng",
    "Portugués": "por",
    "Francés": "fra"
}

# Función principal que inicia la interfaz gráfica
def ini_gui():
    def cargar_imagen(ruta):
        global img_actual, img_tk

        img_actual = Image.open(ruta)
        img_actual.thumbnail((600, 600))
        img_tk = ImageTk.PhotoImage(img_actual)

        img_label.configure(image=img_tk)
        img_label.image = img_tk
        # Función para seleccionar una imagen desde el explorador de archivos
        
    def seleccionar_imagen():
        # Abre un cuadro de diálogo para seleccionar archivos
        archivo = filedialog.askopenfilename(
            title="Seleccionar imagen",
            # Solo admite
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
                ("Todos los archivos", "*.*")
            ]
        )

        # Si el usuario selecciona un archivo, se guarda la ruta
        if archivo:
            ruta_var.set(archivo)

    # Función que ejecuta el OCR sobre la imagen seleccionada
    def ejecutar_ocr():
        # Obtiene la ruta del archivo ingresada
        ruta = ruta_var.get().strip()
        # Verifica que se haya seleccionado un archivo
        if not ruta:
            messagebox.showwarning("Falta archivo", "Seleccioná archivo primero.")
            return

        # Obtiene el idioma seleccionado (por defecto español)

        lang_var = tk.StringVar(value="Español")
        lang = IDIOMAS[lang_var.get()]
        try:
            # Ejecuta la función OCR
            texto, csv_data = ocr_recognition(ruta, lang)

        except Exception as e:
            # Muestra un mensaje de error si falla el OCR
            messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{e}")
            return
        
        # Limpia el área de texto
        resultado.delete("1.0", tk.END)

        # Inserta el texto reconocido en la interfaz
        resultado.insert(tk.END, texto)
        
        # csv
        csv_text.delete("1.0", tk.END)
        for fila in csv_data:
            csv_text.insert(tk.END, ",".join(fila))
        # cargar img
        cargar_imagen(ruta)
        
   
            
    # Crea la ventana principal
    ventana = tk.Tk()

    # Título de la ventana
    ventana.title("OCR Simple")

    # Tamaño mínimo de la ventana
    ventana.minsize(700, 450)

    # Configura la columna principal para que se expanda
    ventana.columnconfigure(0, weight=1)

    # Configura la fila del resultado para que se expanda
    ventana.rowconfigure(1, weight=1)


    # ===== FRAME SUPERIOR (CONTROLES) =====

    # Crea un frame para los controles superiores
    top = tk.Frame(ventana, padx=12, pady=12)

    # Ubica el frame en la ventana
    top.grid(row=0, column=0, sticky="ew")

    # Permite que la columna central se expanda
    top.columnconfigure(1, weight=1)

    # Etiqueta para el campo de archivo
    tk.Label(top, text="Archivo:").grid(row=0, column=0, sticky="w", padx=(0, 8))

    # Variable para almacenar la ruta del archivo
    ruta_var = tk.StringVar()

    # Campo de texto para mostrar la ruta del archivo
    tk.Entry(top, textvariable=ruta_var).grid(row=0, column=1, sticky="ew", padx=(0, 8))

    # Botón para buscar la imagen
    tk.Button(top, text="Buscar…", command=seleccionar_imagen).grid(row=0, column=2)

    # Etiqueta para el idioma
    tk.Label(top, text="Idioma:").grid(row=1, column=0, sticky="w", pady=(10, 0))

    lang_var = tk.StringVar(value="Español")

    menu_idioma = tk.OptionMenu(
        top,
        lang_var,
        *IDIOMAS.keys()
    )
    menu_idioma.grid(row=1, column=1, sticky="w")

    # Botón para ejecutar el OCR
    tk.Button(top, text="Procesar OCR", command=ejecutar_ocr).grid(row=1, column=2, pady=(10, 0))


    # ===== FRAME CENTRAL (RESULTADO OCR) =====

    # Frame para mostrar el texto reconocido
    mid = tk.Frame(ventana, padx=12)

    # Ubica el frame y agrega padding inferior
    mid.grid(row=1, column=0, sticky="nsew", pady=(0, 12))

    # Permite que el contenido se expanda
    mid.columnconfigure(0, weight=1)
    mid.rowconfigure(0, weight=1)

    # Área de texto donde se muestra el resultado OCR
    resultado = tk.Text(mid, wrap="word")

    # Ubica el área de texto
    resultado.grid(row=0, column=0, sticky="nsew")

    # Barra de desplazamiento vertical
    scroll = tk.Scrollbar(mid, command=resultado.yview)

    # Ubica la barra de desplazamiento
    scroll.grid(row=0, column=1, sticky="ns")

    # Conecta el scroll con el área de texto
    resultado.configure(yscrollcommand=scroll.set)
    
    # ===== FRAME CSV =====
    csv_frame = tk.Frame(ventana, padx=12)
    csv_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 12))

    csv_frame.columnconfigure(0, weight=1)
    csv_frame.rowconfigure(0, weight=1)

    csv_text = tk.Text(csv_frame, wrap="word")
    csv_text.grid(row=0, column=0, sticky="nsew")

    scroll_y = tk.Scrollbar(csv_frame, orient="vertical", command=csv_text.yview)
    scroll_y.grid(row=0, column=1, sticky="ns")

    csv_text.configure(yscrollcommand=scroll_y.set)
    # ===== FRAME/CANVA de imagen =====
    img_frame = tk.Frame(ventana, padx=12)
    img_frame.grid(row=1, column=2, sticky="nsew")

    img_actual = Image.open("default.png")
    img_actual.thumbnail((600, 600))
    img_tk = ImageTk.PhotoImage(img_actual)

    img_label = tk.Label(img_frame, image=img_tk)
    img_label.image = img_tk
    img_label.pack(expand=True)
    
    ventana.columnconfigure(2, weight=1)
    ventana.rowconfigure(1, weight=1)
    # Ícono de barra de tareas (más confiable)
    icono_png = tk.PhotoImage(file="icon.png")
    ventana.iconphoto(True, icono_png)

    # Inicia el bucle principal de la interfaz
    ventana.mainloop()
