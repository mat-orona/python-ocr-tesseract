import tkinter as tk
from tkinter import filedialog
from function import ocr_recognition

def ini_gui():
    def selec_image():
        archivo = filedialog.askopenfilename()
        if archivo:
            texto = ocr_recognition(archivo)
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END, texto)

    ventana = tk.Tk()
    ventana.title("OCR Simple")

    boton = tk.Button(ventana, text="Seleccionar imagen", command=selec_image)
    boton.pack()

    resultado = tk.Text(ventana, height=30, width=60)
    resultado.pack()

    ventana.mainloop()
