import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QInputDialog, QMenu, QDialog  # 👈 add QDialog here
)

from PyQt5.QtCore import Qt
from transform_preview import TransformPreviewDialog
from preview_transform_dialog import PreviewTransformDialog



class SearchWindow(QWidget):
    def __init__(self, history, on_item_selected):
        super().__init__()
        self.setWindowTitle("Search Clipboard History")
        self.setGeometry(500, 300, 500, 400)

        self.history = history
        self.on_item_selected = on_item_selected

        layout = QVBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search...")
        self.search_box.textChanged.connect(self.filter_history)

        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.item_clicked)
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(self.search_box)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        self.update_list()

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', 'Ubuntu', sans-serif;
                font-size: 14px;
            }

            QLineEdit {
                padding: 8px;
                border: 1px solid #444;
                border-radius: 6px;
                background-color: #2e2e2e;
                color: white;
            }

            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #444;
                border-radius: 6px;
            }

            QListWidget::item {
                padding: 8px;
            }

            QListWidget::item:selected {
                background-color: #3e8e41;
                color: white;
            }
        """)

    def update_list(self):
        self.list_widget.clear()
        for item in self.history:
            content_type = item.get("type", "text")
            text = item.get("text", "")
            snippet = text[:60]
            display_text = f"[{content_type.upper()}] {snippet}" + ("..." if len(text) > 60 else "")
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.UserRole, text)
            self.list_widget.addItem(list_item)

    def filter_history(self, text):
        self.list_widget.clear()
        for item in self.history:
            full_text = item.get("text", "")
            if text.lower() in full_text.lower():
                content_type = item.get("type", "text")
                snippet = full_text[:60]
                display_text = f"[{content_type.upper()}] {snippet}" + ("..." if len(full_text) > 60 else "")
                list_item = QListWidgetItem(display_text)
                list_item.setData(Qt.UserRole, full_text)
                self.list_widget.addItem(list_item)

    def item_clicked(self, item):
        if self.on_item_selected:
            self.on_item_selected(item.data(Qt.UserRole))
        self.close()

    def show_context_menu(self, position):
        selected_item = self.list_widget.itemAt(position)
        if not selected_item:
            return

        original = selected_item.data(Qt.UserRole)

        menu = QMenu()
        fancy_action = menu.addAction("🪄 Fancy Preview")

        edit_action = menu.addAction("✏️ Edit & Paste")
        upper_action = menu.addAction("🔠 UPPERCASE")
        lower_action = menu.addAction("🔡 lowercase")
        strip_action = menu.addAction("🧹 Strip whitespace")
        clean_action = menu.addAction("🚿 Remove formatting")

        action = menu.exec_(self.list_widget.viewport().mapToGlobal(position))

        if not action:
            return

        transformed = original

        if action == edit_action:
            edited, ok = QInputDialog.getMultiLineText(self, "Edit Text", "Modify the text:", original)
            if ok and edited.strip():
                transformed = edited.strip()
            else:
                return
        elif action == upper_action:
            transformed = original.upper()
        elif action == lower_action:
            transformed = original.lower()
        elif action == strip_action:
            transformed = original.strip()
        elif action == clean_action:
            transformed = re.sub(r'\s+', ' ', original).strip()
        elif action == fancy_action:
            self.open_preview_dialog(original)

        if action != edit_action:
            dialog = TransformPreviewDialog(original, transformed, self)
            if dialog.exec_() != QDialog.Accepted:
                return
            transformed = dialog.get_transformed_text()
            

        if self.on_item_selected and transformed:
            self.on_item_selected(transformed)
        self.close()

        

        

    def open_preview_dialog(self, original_text):
        dialog = PreviewTransformDialog(original_text, lambda text: text, self.on_item_selected)

        dialog.exec_()
    
        
