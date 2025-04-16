import os
import json
import re
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
from search_window import SearchWindow
from datetime import datetime

HISTORY_FILE = "clipboard_history.json"
MAX_HISTORY = 30

def detect_content_type(text):
    if re.match(r'https?://\S+', text):
        return "url"
    elif re.match(r'\S+@\S+\.\S+', text):
        return "email"
    elif re.match(r'^\+?[0-9\s\-\(\)]+$', text):
        return "phone"
    elif re.search(r'\b(def|class|function|import|var|let|const)\b', text):
        return "code"
    elif os.path.exists(text):
        return "file_path"
    else:
        return "text"

class ClipboardTray(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.setIcon(QIcon.fromTheme("edit-paste"))
        self.setToolTip("Smart Clipboard Manager")

        self.clipboard = QApplication.clipboard()
        copied_text = self.clipboard.text()

        self.menu = QMenu()
        self.setContextMenu(self.menu)

        self.history = self.load_history()
        self.search_window = None
        self.activated.connect(self.on_tray_icon_clicked)

        if copied_text.strip():
            self.history.insert(0, {
                "text": copied_text,
                "type": detect_content_type(copied_text),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        self.clipboard.dataChanged.connect(self.on_clipboard_change)
        self.update_menu()
        self.show()

    def on_clipboard_change(self):
        text = self.clipboard.text()
        if text and (not self.history or text != self.history[0]["text"]):
            content_type = detect_content_type(text)
            self.history.insert(0, {
                "text": text,
                "type": content_type,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.history = self.history[:MAX_HISTORY]
            self.save_history()
            self.update_menu()

    def update_menu(self):
        self.menu.clear()
        for item in self.history[:10]:
            label = f"[{item['type']}] {item['text'][:40]}" + ("..." if len(item["text"]) > 40 else "")
            action = QAction(label, self)
            action.triggered.connect(lambda checked, text=item["text"]: self.clipboard.setText(text))
            self.menu.addAction(action)

        self.menu.addSeparator()

        search_action = QAction("Search History", self)
        search_action.triggered.connect(self.open_search_window)
        self.menu.addAction(search_action)

        clear_action = QAction("Clear History", self)
        clear_action.triggered.connect(self.clear_history)
        self.menu.addAction(clear_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        self.menu.addAction(quit_action)

    def open_search_window(self):
        if self.search_window is None or not self.search_window.isVisible():
            self.search_window = SearchWindow(self.history, self.clipboard.setText)
            self.search_window.show()
            self.search_window.activateWindow()

    def clear_history(self):
        self.history = []
        self.save_history()
        self.update_menu()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                raw_history = json.load(f)
                upgraded = []
                for item in raw_history:
                    if isinstance(item, str):
                        upgraded.append({
                            "text": item,
                            "type": detect_content_type(item),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    elif isinstance(item, dict) and "text" in item and "type" in item:
                        if "timestamp" not in item:
                            item["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        upgraded.append(item)
                return upgraded
        return []

    def save_history(self):
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.history, f, indent=2)

    def on_tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # left click
            self.open_search_window()
