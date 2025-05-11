from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from core import app  # подтягиваем активированный app

if __name__ == "__main__":
    import sys
    qt_app = QApplication(sys.argv)

    window = MainWindow(user_role="Инженер")
    window.show()

    sys.exit(qt_app.exec_())
