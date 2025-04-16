from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
)
from PyQt5.QtCore import Qt
import markdown


class PreviewTransformDialog(QDialog):
    def __init__(self, original_text, transform_fn, callback):
        super().__init__()
        self.setWindowTitle("🛠 Preview & Transform")
        self.setMinimumSize(800, 500)

        self.original_text = original_text
        self.transform_fn = transform_fn
        self.callback = callback

        self.editor = QTextEdit()
        self.editor.setText(original_text)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)

        # Layout setup
        main_layout = QVBoxLayout()
        split_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        split_layout.addWidget(self.editor)
        split_layout.addWidget(self.preview)

        self.apply_btn = QPushButton("✅ Apply")
        self.cancel_btn = QPushButton("❌ Cancel")
        self.revert_btn = QPushButton("🔄 Revert")
        self.transform_btn = QPushButton("🧪 Apply Transformation")

        self.apply_btn.clicked.connect(self.apply)
        self.cancel_btn.clicked.connect(self.reject)
        self.revert_btn.clicked.connect(self.revert)
        self.transform_btn.clicked.connect(self.update_preview)

        button_layout.addStretch()
        button_layout.addWidget(self.revert_btn)
        button_layout.addWidget(self.transform_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.apply_btn)

        main_layout.addLayout(split_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.update_preview()

        self.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 13px;
                background-color: #1e1e1e;
                color: #eeeeee;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton {
                padding: 8px 14px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 6px;
            }
        """)

    def update_preview(self):
        edited = self.editor.toPlainText()
        transformed = self.transform_fn(edited)
        rendered_html = markdown.markdown(transformed)
        self.preview.setHtml(rendered_html)

    def revert(self):
        self.editor.setText(self.original_text)
        self.update_preview()

    def apply(self):
        final_text = self.transform_fn(self.editor.toPlainText())
        self.callback(final_text)
        self.accept()
