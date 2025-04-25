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
from PyQt5.QtWidgets import QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
import os
from PyQt5.QtGui import QPixmap


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
                border-radius: 1px;
                padding: 4px;
            }

            QPushButton:hover {
                background-color: #5a5a5a;
            }

            QPushButton:pressed {
                background-color: #2e7031;
            }
            QScrollBar:vertical {
                border: none;
                background: #2a2a2a;
                width: 10px;
                margin: 4px 0 4px 0;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background: #5a5a5a;
                min-height: 30px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background: #777;
            }

            QScrollBar::handle:vertical:pressed {
                background: #888;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
                background: none;
                border: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            QScrollBar:horizontal {
                border: none;
                background: #2a2a2a;
                height: 10px;
                margin: 0 4px 0 4px;
                border-radius: 5px;
            }

            QScrollBar::handle:horizontal {
                background: #5a5a5a;
                min-width: 30px;
                border-radius: 5px;
            }

            QScrollBar::handle:horizontal:hover {
                background: #777;
            }

            QScrollBar::handle:horizontal:pressed {
                background: #888;
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0;
                background: none;
                border: none;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
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


    def update_list(self, items=None):
        self.list_widget.clear()
        items = items or self.history

        for item in items:
            content_type = item.get("type", "text")
            text = item.get("text", "")
            timestamp = item.get("timestamp") or "Unknown time"

            # ⬇️ Create the item widget and main layout FIRST
            item_widget = QWidget()
            main_layout = QVBoxLayout()
            main_layout.setContentsMargins(12, 20, 12, 8)
            main_layout.setSpacing(6)

            # Prepare snippet for text display
            snippet = text[:60]

            # Check if content is an image
            if content_type == "image" and os.path.exists(text):
                print(f"Loading image from: {text}")  # Debugging line

                image_label = QLabel()
                pixmap = QPixmap(text)
                
                # Check if the image was successfully loaded
                if pixmap.isNull():
                    print(f"Failed to load image from: {text}")
                    image_label.setText("Failed to load image")  # Show an error text if image fails to load
                else:
                    pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    image_label.setPixmap(pixmap)
                
                main_layout.addWidget(image_label)
                snippet = ""  # We don't show text for images
            else:
                text_label = QLabel(snippet + ("..." if len(text) > 60 else ""))
                text_label.setStyleSheet("font-weight: regular;")
                main_layout.addWidget(text_label)

            # ⬇️ Add timestamp label
            timestamp_label = QLabel(f"{content_type.upper()} • {timestamp}")
            timestamp_label.setStyleSheet("color: #888; font-size: 10px;")
            main_layout.addWidget(timestamp_label)

            # ⬇️ Add transformation buttons
            button_layout = QHBoxLayout()
            button_layout.setSpacing(12)
            button_layout.setAlignment(Qt.AlignLeft)
            buttons = []

            def add_btn(icon_path, tooltip, handler, text, color="#3a3a3a"):
                btn = QPushButton()
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(16, 16))
                btn.setToolTip(tooltip)
                btn.setFixedSize(32, 28)
                btn.clicked.connect(lambda _, t=text: handler(t))

                effect = QGraphicsOpacityEffect()
                effect.setOpacity(0.0)
                btn.setGraphicsEffect(effect)
                btn.setEnabled(False)

                fade_anim = QPropertyAnimation(effect, b"opacity")
                fade_anim.setDuration(300)
                fade_anim.setStartValue(0.0)
                fade_anim.setEndValue(1.0)
                fade_anim.setEasingCurve(QEasingCurve.OutQuad)

                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        border-radius: 2px;
                        padding: 4px;
                        border: 1px solid green;
                    }}
                    QPushButton:hover {{
                        background-color: #5a5a5a;
                    }}
                """)

                btn._fade_anim = fade_anim

                def animate_in():
                    btn.setEnabled(True)
                    fade_anim.setDirection(QPropertyAnimation.Forward)
                    fade_anim.start()

                def animate_out():
                    fade_anim.setDirection(QPropertyAnimation.Backward)
                    fade_anim.start()
                    btn.setEnabled(False)

                btn.animate_in = animate_in
                btn.animate_out = animate_out

                button_layout.addWidget(btn)
                buttons.append((btn, effect))

            # Add buttons after defining the function
            add_btn("icons/pen.png", "Edit & Paste", self.handle_edit, text)
            add_btn("icons/uppercase-interface-button.png", "UPPERCASE", lambda t: self.handle_transform(t.upper()), text)
            add_btn("icons/lowercase-interface-symbol.png", "lowercase", lambda t: self.handle_transform(t.lower()), text)
            add_btn("icons/strip.png", "Strip", lambda t: self.handle_transform(t.strip()), text)
            add_btn("icons/clean.png", "Clean", lambda t: self.handle_transform(re.sub(r'\s+', ' ', t).strip()), text)

            main_layout.addLayout(button_layout)
            item_widget.setLayout(main_layout)
            item_widget.setStyleSheet("QWidget { background-color: transparent; }")

            def enterEvent(event, btns=buttons):
                for btn, _ in btns:
                    btn.animate_in()
                QWidget.enterEvent(item_widget, event)

            def leaveEvent(event, btns=buttons):
                for btn, _ in btns:
                    btn.animate_out()
                QWidget.leaveEvent(item_widget, event)

            item_widget.enterEvent = enterEvent
            item_widget.leaveEvent = leaveEvent

            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 18, 18)
            container_layout.addWidget(item_widget)

            list_item = QListWidgetItem()
            list_item.setSizeHint(container.sizeHint())
            list_item.setData(Qt.UserRole, text)
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, container)


            
    def filter_history(self, text):
        filtered = [
            item for item in self.history
            if text.lower() in item.get("text", "").lower()
        ]
        self.update_list(filtered)


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



    
        
