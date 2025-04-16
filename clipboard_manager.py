# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QObject, pyqtSignal

# class ClipboardManager(QObject):
#     new_clipboard_item = pyqtSignal(str)

#     def __init__(self):
#         super().__init__()
#         self.clipboard = QApplication.clipboard()
#         self.last_text = ""
#         self.clipboard.dataChanged.connect(self.on_clipboard_change)

#     def on_clipboard_change(self):
#         # Check if the clipboard contains text
#         if self.clipboard.mimeData().hasText():
#             text = self.clipboard.text()
#             if text != self.last_text:
#                 self.last_text = text
#                 self.new_clipboard_item.emit(text)
