from PyQt5 import QtWidgets
import sys

from ui.main_window import MainWindow
from core import app  # ← единый app
from core import db   # ← единый db

if __name__ == "__main__":
    qt_app = QtWidgets.QApplication(sys.argv)

    with app.app_context():
        main_window = MainWindow(user_role="Инженер")
        main_window.show()

    sys.exit(qt_app.exec_())
