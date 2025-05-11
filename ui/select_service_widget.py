from PyQt5 import QtWidgets
from ui.select_service_widget_ui import Ui_SelectServiceWidget


class SelectServiceWidget(QtWidgets.QWidget, Ui_SelectServiceWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
