from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from function import *

class OCRRect(QGraphicsRectItem):
    def __init__(self, x, y, w, h, name):
        super().__init__(x, y, w, h)

        self.name = name
        self.output = ""

        pen = QPen(QColor("blue"))
        pen.setWidth(2)
        self.setPen(pen)

        self.setFlags(
            QGraphicsRectItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsRectItem.GraphicsItemFlag.ItemIsSelectable 
        )

    

class ImageView(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent
        
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform
        )

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

    def load_image(self, path):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            QMessageBox.critical(self, "Error", f"No se pudo cargar la imagen:\n{path}")
            return
        
        self.scene.clear()
        self.pixmap_item = self.scene.addPixmap(pixmap)  
        self.pixmap_item.setPos(0, 0)                    
        self.setSceneRect(self.pixmap_item.boundingRect())
        
    def wheelEvent(self, event):
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)
        
    def get_fields(self):
        fields = {}

        for item in self.scene.items():
            if isinstance(item, OCRRect):
                r = item.sceneBoundingRect()

                fields[item.name] = (
                    int(r.x()),
                    int(r.y()),
                    int(r.width()),
                    int(r.height())
                )
        return fields

    def keyPressEvent(self, event):
        selected = self.scene.selectedItems()
        if not selected:
            return

        rect = selected[0]  # OCRRect seleccionado
        r = rect.rect()

        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Down:
                rect.setRect(r.x(), r.y(), r.width(), r.height() + 2)

            elif event.key() == Qt.Key.Key_Up:
                rect.setRect(r.x(), r.y(), r.width(), max(2, r.height() - 2))

            elif event.key() == Qt.Key.Key_Right:
                rect.setRect(r.x(), r.y(), r.width() + 2, r.height())

            elif event.key() == Qt.Key.Key_Left:
                rect.setRect(r.x(), r.y(), max(2, r.width() - 2), r.height())

            rect.update()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        selected = self.scene.selectedItems()
        if selected:
            rect = selected[0]
            self.parent_window.on_rect_selected(rect)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resultados_globales = []
        self.setWindowTitle("OCR Viewer")
        self.setWindowIcon(QIcon("assets/icon.ico"))
        # Visor central
        self.view = ImageView(self)
        
        self.setCentralWidget(self.view)

        self.view.load_image("assets/default.jpg")

        # --- Barra DERECHA para ajustar campos ---
        toolbar = QToolBar()
        toolbar.setMovable(True)

        dock_toolbar = QDockWidget("Ajustes de campos", self)
        dock_toolbar.setWidget(toolbar)

        dock_toolbar.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock_toolbar)

        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 9999)
        self.width_spin.setPrefix("W: ")

        self.height_spin = QSpinBox()
        self.height_spin.setRange(0, 9999)
        self.height_spin.setPrefix("H: ")

        toolbar.addWidget(self.width_spin)
        toolbar.addWidget(self.height_spin)
        
        self.color_btn = QPushButton("Color")
        self.color_btn.clicked.connect(self.change_rect_color)
        toolbar.addWidget(self.color_btn)


        # Conectar cambios
        self.width_spin.valueChanged.connect(self.update_rect_size)
        self.height_spin.valueChanged.connect(self.update_rect_size)

        self.selected_rect = None      
        # --- Barra IZQUIERDA para ajustar campos ---
        dock = QDockWidget("Menu", self)

        dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea |
            Qt.DockWidgetArea.TopDockWidgetArea |
            Qt.DockWidgetArea.BottomDockWidgetArea
        )

        dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )

        dock_widget = QWidget()
        layout = QVBoxLayout()
        row = QHBoxLayout()

       #BOTONES 
        btn_save_profile = QPushButton("Guardar perfil")
        btn_save_profile.clicked.connect(self.save_profile)
        row.addWidget(btn_save_profile)
        
        btn_load_profile = QPushButton("Cargar perfil")
        btn_load_profile.clicked.connect(self.load_profile)
        row.addWidget(btn_load_profile)

        btn_load_multiple = QPushButton("Cargar múltiples")
        btn_load_multiple.clicked.connect(self.load_multiple_images)
        layout.addWidget(btn_load_multiple)

        
        
        btn_load = QPushButton("Cargar imagen")
        btn_load.clicked.connect(self.load_image_dialog)
        layout.addWidget(btn_load)
        
        btn_add = QPushButton("Agregar campo")
        btn_add.clicked.connect(self.add_field)
        layout.addWidget(btn_add)
        
        btn_ocr = QPushButton("Preview OCR")
        btn_ocr.clicked.connect(self.run_ocr)
        layout.addWidget(btn_ocr)
        
        btn_concatenate = QPushButton("Añadir")
        btn_concatenate.clicked.connect(self.concatenate)
        layout.addWidget(btn_concatenate)
        
        

        
        self.fields_list = QListWidget()
        
        self.fields_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.fields_list.customContextMenuRequested.connect(self.show_fields_menu)

        self.fields_list.keyPressEvent = self.delete_field_key
        self.fields_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.fields_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.fields_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.fields_list.itemDoubleClicked.connect(self.rename_field)
        self.fields_list.setMinimumHeight(150)

        layout.addWidget(self.fields_list)
        self.fields_list.currentItemChanged.connect(self.on_list_item_selected)
        dock_widget.setLayout(layout)
        dock.setWidget(dock_widget)
        layout.addLayout(row)
        
        
        
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        self.current_image_path = "assets/default.jpg"
        self.view.load_image(self.current_image_path)
        
                
        # --- PANEL OUTPUT ---
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()

        self.output_tabs = QTabWidget()
        self.output_tabs.setMinimumHeight(355)

        # --- Pestaña: Resultados globales ---
        self.tab_global = QTextEdit()
        self.tab_global.setReadOnly(True)
        self.output_tabs.addTab(self.tab_global, "Global")

        # --- Pestaña: CSV ---
        self.tab_csv = QTextEdit()
        self.tab_csv.setReadOnly(True)
        self.output_tabs.addTab(self.tab_csv, "CSV")

        # --- Pestaña: JSON ---
        self.tab_json = QTextEdit()
        self.tab_json.setReadOnly(True)
        self.output_tabs.addTab(self.tab_json, "JSON")

        # --- Pestaña: SQL ---
        self.tab_sql = QTextEdit()
        self.tab_sql.setReadOnly(True)
        self.output_tabs.addTab(self.tab_sql, "SQL")

        # --- Pestaña: XML ---
        self.tab_xml = QTextEdit()
        self.tab_xml.setReadOnly(True)
        self.output_tabs.addTab(self.tab_xml, "XML")

        output_layout.addWidget(self.output_tabs)
        output_group.setLayout(output_layout)

        layout.addWidget(output_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

    def load_image_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp *.pdf )"
        )

        if not file_path:
            QMessageBox.warning(self, "Error", "No se seleccionó ninguna imagen.")
            return

        self.view.scene.clear()
        self.fields_list.clear()
        self.field_counter = 0
        
        # Cargar nueva imagen
        self.current_image_path = file_path
        self.view.load_image(file_path)
        
    def run_ocr(self):
        fields = self.view.get_fields()

        if not fields:
            QMessageBox.warning(self, "OCR", "No hay campos.")
            return

        results = ocr_by_fields(self.current_image_path, fields)

        if isinstance(results, list):
            results = results[0]["campos"]


        preview_text = ""

        for i in range(self.fields_list.count()):
            item = self.fields_list.item(i)
            rect = item.rect

            if rect is None:
                continue

            rect.output = results.get(rect.name, "")
            item.setText(f"{rect.name} → {rect.output}")

            preview_text += f"{rect.name}: {rect.output}\n"

    def concatenate(self):

        lista_final = []

        for i in range(self.fields_list.count()):
            item = self.fields_list.item(i)
            rect = item.rect

            if rect is None:
                continue
            
            lista_final.append({
                "nombreDelCampo": rect.name,
                "resultado": rect.output,
                "documento": self.current_image_path
            })

        self.resultados_globales.extend(lista_final)
        self.update_global_preview()
        self.update_output_tabs()

    def update_global_preview(self):
            text = ""

            for campo in self.resultados_globales:

                text += f"{campo['nombreDelCampo']}: {campo['resultado']}\n"
                text += f"Doc: {campo['documento']}\n"
                text += "-" + "\n"

    def add_field(self):
        count = self.fields_list.count() + 1
        name = f"Campo {count}"
        
        # Crear rectángulo
        rect = OCRRect(50, 50, 150, 30, name)
        self.view.scene.addItem(rect)
        rect.is_field_rect = True

  

        # Crear item de lista
        item = QListWidgetItem(name)
        self.fields_list.addItem(item)

        #  VINCULACIÓN CLAVE
        rect.list_item = item
        item.rect = rect

        # Seleccionar automáticamente
        rect.setSelected(True)
        self.on_rect_selected(rect)
        
    def on_rect_selected(self, rect):
        # Si el rect no tiene item, no hacemos nada
        if not hasattr(rect, "list_item"):
            return

        item = rect.list_item

        # Si el item ya fue borrado, no hacemos nada
        if item is None:
            return

        # Si el item ya no está en la lista, no hacemos nada
        if self.fields_list.row(item) == -1:
            return

        # Si todo está bien, seleccionamos
        row = self.fields_list.row(item)
        self.fields_list.setCurrentRow(row)

    def on_list_item_selected(self, item):
        if not item:
            return

        rect = item.rect
        self.selected_rect = rect

        # Seleccionar el rectángulo en la escena
        self.view.scene.clearSelection()
        rect.setSelected(True)

        # Actualizar spinboxes
        self.on_rect_selected(rect)

    def update_rect_size(self):
        if not self.selected_rect:
            return

        rect = self.selected_rect
        r = rect.rect()

        w = self.width_spin.value()
        h = self.height_spin.value()

        rect.setRect(r.x(), r.y(), w, h)
        rect.update()

    def change_rect_color(self):
        if not self.selected_rect:
            return

        color = QColorDialog.getColor()

        if color.isValid():
            pen = self.selected_rect.pen()
            pen.setColor(color)
            self.selected_rect.setPen(pen)
            self.selected_rect.update()
    # --- TABs Output(transformador) ---
    def update_output_tabs(self):
        # --- TAB 1: Resultados globales ---
        text = ""
        for campo in self.resultados_globales:
            text += f"Documento: {campo['documento']}\n"
            text += f"{campo['nombreDelCampo']}: {campo['resultado']}\n"
            text += "-" * 40 + "\n"
        self.tab_global.setPlainText(text)

        # --- TAB 2: CSV ---
        csv_text = "documento,campos,resultado\n"
        for campo in self.resultados_globales:
            csv_text += f"{campo['documento']},{campo['nombreDelCampo']},{campo['resultado']}\n"
        self.tab_csv.setPlainText(csv_text)

        # --- TAB 3: JSON ---
        import json
        json_text = json.dumps(self.resultados_globales, indent=4, ensure_ascii=False)
        self.tab_json.setPlainText(json_text)
        
        # --- TAB SQL ---
        sql_text = ""
        for campo in self.resultados_globales:
            sql_text += (
                "INSERT INTO resultados (documento, nombreDelCampo, resultado) "
                f"VALUES ('{campo['documento']}', '{campo['nombreDelCampo']}', '{campo['resultado']}');\n"
            )
        self.tab_sql.setPlainText(sql_text)

        # --- TAB XML ---
        xml_text = "<resultados>\n"
        for campo in self.resultados_globales:
            xml_text += f"  <campo>\n"
            xml_text += f"    <documento>{campo['documento']}</documento>\n"
            xml_text += f"    <nombre>{campo['nombreDelCampo']}</nombre>\n"
            xml_text += f"    <resultado>{campo['resultado']}</resultado>\n"
            xml_text += f"  </campo>\n"
        xml_text += "</resultados>"
        self.tab_xml.setPlainText(xml_text)
    
    def rename_field(self, item):
        nuevo = QInputDialog.getText(self, "Renombrar campo", "Nuevo nombre:")[0]
        if nuevo:
            item.setText(nuevo)
            item.rect.name = nuevo

    def delete_field(self, item):
        rect = item.rect

        # borrar rectángulo
        if rect:
            self.view.scene.removeItem(rect)

        # borrar item de la lista
        row = self.fields_list.row(item)
        self.fields_list.takeItem(row)

    def delete_field_key(self, event):
        if event.key() == Qt.Key.Key_Delete:
            item = self.fields_list.currentItem()
            if item:
                rect = item.rect
                self.view.scene.removeItem(rect)
                self.fields_list.takeItem(self.fields_list.row(item))

    def show_fields_menu(self, position):
        item = self.fields_list.itemAt(position)
        if not item:
            return

        menu = QMenu()

        rename_action = QAction("Renombrar", self)
        delete_action = QAction("Eliminar", self)

        rename_action.triggered.connect(lambda: self.rename_field(item))
        delete_action.triggered.connect(lambda: self.delete_field(item))

        menu.addAction(rename_action)
        menu.addAction(delete_action)

        menu.exec(self.fields_list.mapToGlobal(position))

    def create_field_from_profile(self, name, x, y, w, h):
        rect = OCRRect(0, 0, w, h, name)
        rect.is_field_rect = True

        rect.setPos(x, y)

        self.view.scene.addItem(rect)

        item = QListWidgetItem(name)
        self.fields_list.addItem(item)

        rect.list_item = item
        item.rect = rect

        return rect

    def save_profile(self):
        perfil = []

        for i in range(self.fields_list.count()):
            item = self.fields_list.item(i)
            rect = item.rect

            r = rect.sceneBoundingRect()

            perfil.append({
                "name": rect.name,
                "x": r.x(),
                "y": r.y(),
                "width": r.width(),
                "height": r.height()
            })

        import json
        from PyQt6.QtWidgets import QFileDialog

        path, _ = QFileDialog.getSaveFileName(self, "Guardar perfil", "", "JSON (*.json)")
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            json.dump(perfil, f, indent=4, ensure_ascii=False)

    def load_profile(self):
        from PyQt6.QtWidgets import QFileDialog
        import json

        path, _ = QFileDialog.getOpenFileName(self, "Cargar perfil", "", "JSON (*.json)")
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            perfil = json.load(f)

        # limpiar lista y escena
        self.fields_list.clear()
        for item in list(self.view.scene.items()):
            if hasattr(item, "is_field_rect"):
                self.view.scene.removeItem(item)

        # reconstruir campos
        for campo in perfil:
            self.create_field_from_profile(
                campo["name"],
                campo["x"],
                campo["y"],
                campo["width"],
                campo["height"]
            )
        self.loaded_profile = perfil

    def load_image(self, path):
        for item in list(self.view.scene.items()):
            if not hasattr(item, "is_field_rect"):
                self.view.scene.removeItem(item)


        # Cargar imagen
        pixmap = QPixmap(path)
        self.view.scene.addPixmap(pixmap)

        # Guardar ruta actual
        self.current_image_path = path
        self.current_image = QImage(path)
        
        # Ajustar vista
        self.view.fitInView(self.view.scene.itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def process_multiple_images(self, paths):
        for i, path in enumerate(paths, start=1):
            self.load_image(path)
            self.run_ocr()
            self.concatenate()

            self.progress_bar.setValue(i)
            QApplication.processEvents()  # mantiene viva la UI

        self.progress_bar.setVisible(False)
        QApplication.processEvents()  # mantiene viva la UI
        self.progress_bar.setVisible(False)
        
    def load_multiple_images(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar imágenes",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.tif *.tiff)"
        )

        if not paths:
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(paths))
        self.progress_bar.setValue(0)

        self.process_multiple_images(paths)