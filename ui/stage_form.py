from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StageForm(object):
    def setupUi(self, StageForm):
        StageForm.setObjectName("StageForm")
        StageForm.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(StageForm)
        self.verticalLayout.setObjectName("verticalLayout")

        self.stageTitleLabel = QtWidgets.QLabel(StageForm)
        self.stageTitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.stageTitleLabel.setStyleSheet("font-size: 16pt; font-weight: bold;")
        self.stageTitleLabel.setObjectName("stageTitleLabel")
        self.verticalLayout.addWidget(self.stageTitleLabel)

        self.deadlineLabel = QtWidgets.QLabel(StageForm)
        self.deadlineLabel.setObjectName("deadlineLabel")
        self.verticalLayout.addWidget(self.deadlineLabel)

        self.tableWidget = QtWidgets.QTableWidget(StageForm)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["Фамилия", "Имя", "Должность"])
        self.verticalLayout.addWidget(self.tableWidget)

        self.attachedFilesLabel = QtWidgets.QLabel(StageForm)
        self.attachedFilesLabel.setObjectName("attachedFilesLabel")
        self.verticalLayout.addWidget(self.attachedFilesLabel)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.sendButton = QtWidgets.QPushButton(StageForm)
        self.sendButton.setObjectName("sendButton")
        self.buttonLayout.addWidget(self.sendButton)

        self.attachButton = QtWidgets.QPushButton(StageForm)
        self.attachButton.setObjectName("attachButton")
        self.buttonLayout.addWidget(self.attachButton)

        self.verticalLayout.addLayout(self.buttonLayout)

        self.retranslateUi(StageForm)
        QtCore.QMetaObject.connectSlotsByName(StageForm)

    def retranslateUi(self, StageForm):
        _translate = QtCore.QCoreApplication.translate
        StageForm.setWindowTitle(_translate("StageForm", "Этап"))
        self.stageTitleLabel.setText(_translate("StageForm", "Название этапа"))
        self.deadlineLabel.setText(_translate("StageForm", "Срок: не установлен"))
        self.attachedFilesLabel.setText(_translate("StageForm", "Файлы не выбраны"))
        self.sendButton.setText(_translate("StageForm", "Отправить"))
        self.attachButton.setText(_translate("StageForm", "Прикрепить файл"))
