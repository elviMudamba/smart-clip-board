from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QDialog, QSizePolicy
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class PreviewTransformDialog(QDialog):
    def __init__(self, original_text, transform_fn, callback):
        super().__init__()
        self.setWindowTitle("Preview & Transform")
        self.setMinimumSize(600, 400)

        self.original_text = original_text or ""
        self.transformed_text = transform_fn(self.original_text)
        self.callback = callback

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header labels
        header_layout = QHBoxLayout()
        original_label = QLabel("📝 Original")
        transformed_label = QLabel("✨ Transformed")

        for label in (original_label, transformed_label):
            label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            label.setStyleSheet("color: #cccccc;")
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        header_layout.addWidget(original_label)
        header_layout.addWidget(transformed_label)
        layout.addLayout(header_layout)

        # Text areas
        split_layout = QHBoxLayout()

        self.original_edit = QTextEdit()
        self.original_edit.setReadOnly(True)
        self.original_edit.setPlainText(self.original_text)

        self.transformed_edit = QTextEdit()
        self.transformed_edit.setPlainText(self.transformed_text)

        for editor in (self.original_edit, self.transformed_edit):
            editor.setStyleSheet("""
                QTextEdit {
                    background-color: #1e1e1e;
                    color: #f0f0f0;
                    border: 1px solid #444;
                    border-radius: 10px;
                    padding: 10px;
                    font-family: 'Fira Code', 'Consolas', monospace;
                    font-size: 14px;
                }
            """)
            editor.setMinimumWidth(280)

        split_layout.addWidget(self.original_edit)
        split_layout.addWidget(self.transformed_edit)

        layout.addLayout(split_layout)

        # Apply Button
        apply_button = QPushButton("✅ Apply")
        apply_button.setFixedSize(120, 36)
        apply_button.clicked.connect(self.apply)
        apply_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout.addWidget(apply_button, alignment=Qt.AlignRight)

        # Optional window styling
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
        """)

    def apply(self):
        final_text = self.transformed_edit.toPlainText()
        if self.callback:
            self.callback(final_text)
        self.accept()

    def get_transformed_text(self):
        return self.transformed_edit.toPlainText()
