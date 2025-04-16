import sys
from PyQt5.QtWidgets import QApplication
from tray_ui import ClipboardTray

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    tray = ClipboardTray()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
