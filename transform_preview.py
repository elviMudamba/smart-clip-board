from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton


class TransformPreviewDialog(QDialog):
    def __init__(self, original, transformed, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview Transformation")
        self.setMinimumSize(700, 400)

        layout = QVBoxLayout()

        side_by_side = QHBoxLayout()

        # Original Text
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Original"))
        self.original_text = QTextEdit(original)
        self.original_text.setReadOnly(True)
        left_layout.addWidget(self.original_text)

        # Transformed Text (Editable)
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Transformed"))
        self.transformed_text = QTextEdit(transformed)
        right_layout.addWidget(self.transformed_text)

        side_by_side.addLayout(left_layout)
        side_by_side.addLayout(right_layout)

        layout.addLayout(side_by_side)

        # Buttons
        button_layout = QHBoxLayout()
        apply_btn = QPushButton("✅ Paste")
        cancel_btn = QPushButton("❌ Cancel")
        button_layout.addStretch()
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        apply_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        # Style
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: white;
                font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            }
            QTextEdit {
                background-color: #2e2e2e;
                color: white;
                border: 1px solid #444;
                padding: 6px;
                border-radius: 6px;
            }
            QPushButton {
                padding: 6px 12px;
                background-color: #3e8e41;
                border: none;
                border-radius: 6px;
                color: white;
            }
            QPushButton:hover {
                background-color: #4ea652;
            }
        """)

    def get_transformed_text(self):
        return self.transformed_text.toPlainText().strip()
