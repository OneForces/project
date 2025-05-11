
from PyQt5 import QtCore, QtWidgets

class Ui_SelectServiceWidget(object):
    def setupUi(self, Form):
        Form.setObjectName("SelectServiceWidget")
        Form.resize(400, 300)

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)

        self.label = QtWidgets.QLabel(Form)
        self.label.setText("Выберите службу:")
        self.verticalLayout.addWidget(self.label)

        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.addItems(["Отдел проектирования", "Служба контроля", "Технологический отдел"])
        self.verticalLayout.addWidget(self.comboBox)

        self.sendButton = QtWidgets.QPushButton(Form)
        self.sendButton.setText("Отправить")
        self.verticalLayout.addWidget(self.sendButton)


