import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QInputDialog, QMenu, QDialog, QLabel  # 👈 add QDialog here
)

from PyQt5.QtCore import Qt
from transform_preview import TransformPreviewDialog
from preview_transform_dialog import PreviewTransformDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QHBoxLayout

from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


class SearchWindow(QWidget):
    def __init__(self, history, on_item_selected):
        super().__init__()
        self.setWindowTitle("KlipFusion Search Clipboard History")
        # self.setGeometry(500, 300, 500, 400)
        self.resize(600, 600)  # width, height


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
                padding: 2px;
            }

            QListWidget::item:selected {
                background-color: #3e8e41;
                color: white;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 4px;
            }

            QPushButton:hover {
                background-color: #5a5a5a;
            }

            QPushButton:pressed {
                background-color: #2e7031;
            }

        """)


    def handle_transform(self, transformed):
        dialog = TransformPreviewDialog("", transformed, self)
        if dialog.exec_() == QDialog.Accepted:
            final = dialog.get_transformed_text()
            if self.on_item_selected:
                self.on_item_selected(final)
            self.close()

    def handle_edit(self, original):
        edited, ok = QInputDialog.getMultiLineText(self, "Edit Text", "Modify the text:", original)
        if ok and edited.strip():
            if self.on_item_selected:
                self.on_item_selected(edited.strip())
            self.close()


    def update_list(self):
        self.list_widget.clear()
        for item in self.history:
            content_type = item.get("type", "text")
            icon_map = {
                "text": "📝", "image": "🖼️", "video": "🎥", "audio": "🎵",
                "file": "📁", "link": "🔗", "code": "💻",
                "email": "📧", "phone": "📞",
            }
            icon = icon_map.get(content_type, "📋")
            text = item.get("text", "")
            snippet = text[:60]
            timestamp = item.get("timestamp") or "Unknown time"

            # Main widget
            item_widget = QWidget()
            main_layout = QVBoxLayout(item_widget)
            main_layout.setContentsMargins(10, 6, 10, 6)

            layout = QVBoxLayout(item_widget)
            layout.setContentsMargins(80, 8, 10, 12)  # 💡 Add bottom margin for spacing
            layout.setSpacing(4)  # 💡 Space between label and timestamp/buttons

            # Text + Timestamp stacked vertically
            label_layout = QVBoxLayout()
            label_layout.setSpacing(2)

            text_label = QLabel(f"{icon} {snippet}" + ("..." if len(text) > 60 else ""))
            text_label.setStyleSheet("font-weight: bold;")

            timestamp_label = QLabel(f"{content_type.upper()} • {timestamp}")
            timestamp_label.setStyleSheet("color: #888; font-size: 11px;")

            label_layout.addWidget(text_label)
            label_layout.addWidget(timestamp_label)

            # Button layout (inline left-aligned)
            button_layout = QHBoxLayout()
            button_layout.setSpacing(18)
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_layout.setAlignment(Qt.AlignLeft)

            # Add buttons
            def add_btn(icon_path, tooltip, handler, text, color="#3a3a3a"):
                btn = QPushButton()
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(20, 20))  # ✅ Correct
            # Adjust icon size as needed
                btn.setToolTip(tooltip)
                btn.setFixedSize(32, 28)
                btn.clicked.connect(lambda _, t=text: handler(t))
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        border: .5px solid white;
                        border-radius: 4px;
                    }}
                    QPushButton:hover {{
                        background-color: #5a5a5a;
                    }}
                """)
                button_layout.addWidget(btn)

            add_btn("icons/pen.png", "Edit & Paste", self.handle_edit, text, "#4285F4")
            add_btn("icons/uppercase-interface-button.png", "UPPERCASE", lambda t: self.handle_transform(t.upper()), text, "#34A853")
            add_btn("icons/lowercase-interface-symbol.png", "lowercase", lambda t: self.handle_transform(t.lower()), text, "#34A853")
            add_btn("icons/strip.png", "Strip", lambda t: self.handle_transform(t.strip()), text, "#FBBC05")
            add_btn("icons/clean.png", "Clean", lambda t: self.handle_transform(re.sub(r'\s+', ' ', t).strip()), text, "#EA4335")


            # Add all to main layout
            main_layout.addLayout(label_layout)
            main_layout.addLayout(button_layout)

            # Final wrap
            list_item = QListWidgetItem()
            size = item_widget.sizeHint()
            list_item.setSizeHint(QSize(size.width(), size.height() + 12))  # ⬅️ Add vertical space

            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)

            # Style the item widget like a card
            item_widget.setStyleSheet("""
                background-color: #2e2e2e;
                border-radius: 8px;
                border: 1px solid #444;
            """)

            # Create a QListWidgetItem
            list_item = QListWidgetItem()

            # Add vertical spacing between list items by increasing the item height
            size = item_widget.sizeHint()
            list_item.setSizeHint(QSize(size.width(), size.height() + 2))  # 👈 this creates vertical space

            # Add item to list and set its widget
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, item_widget)





        
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
        if original is None:
            # Fallback to text content if no data was set
            original = selected_item.text()
        original = original or ""


        menu = QMenu()
        menu = QMenu()

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
            transformed = (original or "").upper()

        elif action == lower_action:
            transformed = original.lower()
        elif action == strip_action:
            transformed = original.strip()
        elif action == clean_action:
            transformed = re.sub(r'\s+', ' ', original).strip()
    

        if action != edit_action:
            dialog = TransformPreviewDialog(original, transformed, self)
            if dialog.exec_() != QDialog.Accepted:
                return
            transformed = dialog.get_transformed_text()
            

        if self.on_item_selected and transformed:
            self.on_item_selected(transformed)
        self.close()



    
        
