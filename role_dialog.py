from PyQt5 import QtWidgets

class RoleDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор роли")
        self.setFixedSize(300, 100)

        layout = QtWidgets.QVBoxLayout(self)

        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(["Главный конструктор", "Инженер", "Проектировщик"])
        layout.addWidget(QtWidgets.QLabel("Выберите роль:"))
        layout.addWidget(self.combo)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def get_role(self):
        return self.combo.currentText()
