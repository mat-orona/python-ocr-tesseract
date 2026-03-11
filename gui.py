import tkinter as tk

# Importa herramientas para abrir archivos y mostrar mensajes
from tkinter import filedialog, messagebox

# Importa la función OCR desde el archivo function.py
from function import ocr_recognition
from PIL import Image, ImageTk , ImageDraw


IDIOMAS = {
    "Español": "spa",
    "Inglés": "eng",
    "Portugués": "por",
    "Francés": "fra"
}
info_data = None
bbox_data = None
img_original = None
img_actual = None
bbox_data = None
# Función principal que inicia la interfaz gráfica
def ini_gui():

    def cargar_imagen(ruta):
        global img_actual, img_original, img_tk

        img_original = Image.open(ruta)  
        img_actual = img_original.copy()  

        img_actual.thumbnail((600, 600))
        img_tk = ImageTk.PhotoImage(img_actual)

        img_label.configure(image=img_tk)
        img_label.image = img_tk
        
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
        global info_data,bbox_data
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
            text_data, csv_data , info_data , bbox_data = ocr_recognition(ruta, lang)

        except Exception as e:
            # Muestra un mensaje de error si falla el OCR
            messagebox.showerror("Error", f"No se pudo procesar el archivo:\n{e}")
            return
        
        # Limpia el área de texto
        res_text_data.delete("1.0", tk.END)

        # Inserta el texto reconocido en la interfaz
        res_text_data.insert(tk.END, text_data)
        
        # csv
        res_text_csv_data.delete("1.0", tk.END)
        for fila in csv_data:
            res_text_csv_data.insert(tk.END, ",".join(fila))
        # cargar img
        cargar_imagen(ruta)
        
    def info_data_v(info_data):
        if info_data is None:
            messagebox.showwarning(
                "Sin datos",
                "Primero tenés que ejecutar el OCR."
            )
            return
        ventana_info_data = tk.Toplevel()
        ventana_info_data.title("Info OCR")
        ventana_info_data.geometry("1000x600")

        ventana_info_data.columnconfigure(0, weight=1)
        ventana_info_data.rowconfigure(0, weight=1)

        info_data_frame = tk.Frame(ventana_info_data, padx=12, pady=12)
        info_data_frame.grid(row=0, column=0, sticky="nsew")

        info_data_frame.columnconfigure(0, weight=1)
        info_data_frame.rowconfigure(0, weight=1)

        res_text_info_data = tk.Text(info_data_frame, wrap="word")
        res_text_info_data.grid(row=0, column=0, sticky="nsew")

        scroll = tk.Scrollbar(info_data_frame, command=res_text_info_data.yview)
        scroll.grid(row=0, column=1, sticky="ns")

        res_text_info_data.configure(yscrollcommand=scroll.set)

        res_text_info_data.insert(tk.END, info_data)
  
    def dibujar_bounding_boxes(img, data):
        if data is None:
            return img  # no hay OCR todavía
        draw = ImageDraw.Draw(img)
        n = len(data["text"])
        for i in range(n):
            if data["text"][i].strip() and int(data["conf"][i]) > 0:
                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]

                draw.rectangle(
                    [(x, y), (x + w, y + h)],
                    outline="red",
                    width=2
                )
        return img       
    def mostrar_bounding_boxes():
        global img_actual, img_tk

        if bbox_data is None:
            messagebox.showwarning("OCR", "Primero ejecutá el OCR")
            return

        img_actual = dibujar_bounding_boxes(img_original.copy(), bbox_data)
        img_actual.thumbnail((600, 600))

        img_tk = ImageTk.PhotoImage(img_actual)
        img_label.configure(image=img_tk)
        img_label.image = img_tk
            
        
        
    #===== GUI =====
    # Crea la ventana principal
    ventana = tk.Tk()

    # Título de la ventana
    ventana.title("OCR Simple")

    # Tamaño mínimo de la ventana
    ventana.geometry("1080x800")
    ventana.minsize(1080, 800)
    ventana.columnconfigure(0, weight=3)
    ventana.columnconfigure(1, weight=2)

    ventana.rowconfigure(0, weight=0)
    ventana.rowconfigure(1, weight=2)
    ventana.rowconfigure(2, weight=1)
    # ===== FRAME SUPERIOR (CONTROLES) =====
    # Crea un frame para los controles superiores
    top = tk.Frame(ventana, padx=12, pady=12)

    # Ubica el frame en la ventana
    top.grid(row=0, column=0, columnspan=1, sticky="ew")

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
    
    
    tk.Button(top,text="Ver info OCR",command=lambda: info_data_v(info_data)).grid(row=2, column=2, pady=10)

    
    tk.Button(top,text="Ver detecciones",command=mostrar_bounding_boxes).grid(row=2, column=1, pady=10)
    

    # ===== FRAME CENTRAL (RESULTADO OCR) =====

    # Frame para mostrar el texto reconocido
    mid = tk.Frame(ventana, padx=12)

    # Ubica el frame y agrega padding inferior
    mid.grid(row=1, column=0, sticky="nsew")

    # Permite que el contenido se expanda
    mid.columnconfigure(0, weight=1)
    mid.rowconfigure(0, weight=1)

    # Área de texto donde se muestra el resultado OCR
    res_text_data = tk.Text(mid, wrap="word")

    # Ubica el área de texto
    res_text_data.grid(row=0, column=0, sticky="nsew")

    # Barra de desplazamiento vertical
    scroll = tk.Scrollbar(mid, command=res_text_data.yview)

    # Ubica la barra de desplazamiento
    scroll.grid(row=0, column=1, sticky="ns")

    # Conecta el scroll con el área de texto
    res_text_data.configure(yscrollcommand=scroll.set)
    
    # ===== FRAME CSV =====
    csv_frame = tk.Frame(ventana, padx=12)
    csv_frame.grid(row=2, column=0, columnspan=1, sticky="nsew")
    csv_frame.columnconfigure(0, weight=1)
    csv_frame.rowconfigure(0, weight=1)

    res_text_csv_data = tk.Text(csv_frame, wrap="word")
    res_text_csv_data.grid(row=0, column=0, sticky="nsew")

    scroll_y = tk.Scrollbar(csv_frame, orient="vertical", command=res_text_csv_data.yview)
    scroll_y.grid(row=0, column=1, sticky="ns")

    res_text_csv_data.configure(yscrollcommand=scroll_y.set)
    # ===== FRAME/CANVA de imagen =====
    img_frame = tk.Frame(ventana, padx=12)
    img_frame.grid(row=1, column=1, sticky="nsew")

    img_actual = Image.open("default.png")
    img_actual.thumbnail((600, 600))
    img_tk = ImageTk.PhotoImage(img_actual)

    img_label = tk.Label(img_frame, image=img_tk)
    img_label.image = img_tk
    img_label.pack(expand=True)


    # Ícono de barra de tareas
    icono_png = tk.PhotoImage(file="icon.png")
    ventana.iconphoto(True, icono_png)

    # Inicia el bucle principal de la interfaz
    ventana.mainloop()
