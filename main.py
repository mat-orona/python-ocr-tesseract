#OCR (Reconocimiento Óptico de Caracteres)
from function import *
from gui import *
import sys
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
#----------------------------------------------------MAIN
if __name__ == "__main__":
    exe()
    main()



