from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        MainWindow.setCentralWidget(self.centralwidget)

        # Навигационная панель (добавляется из main_window.py)
        self.stack = QtWidgets.QStackedWidget()
        self.verticalLayout.addWidget(self.stack)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.menuActions.setObjectName("menuActions")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionDevelopment = QtWidgets.QAction(MainWindow)
        self.actionDevelopment.setObjectName("actionDevelopment")
        self.actionNotifications = QtWidgets.QAction(MainWindow)
        self.actionNotifications.setObjectName("actionNotifications")
        self.actionHistory = QtWidgets.QAction(MainWindow)
        self.actionHistory.setObjectName("actionHistory")
        self.actionLetters = QtWidgets.QAction(MainWindow)
        self.actionLetters.setObjectName("actionLetters")
        self.actionProducts = QtWidgets.QAction(MainWindow)
        self.actionProducts.setObjectName("actionProducts")

        self.menuActions.addAction(self.actionDevelopment)
        self.menuActions.addAction(self.actionNotifications)
        self.menuActions.addAction(self.actionHistory)
        self.menuActions.addAction(self.actionLetters)
        self.menuActions.addAction(self.actionProducts)
        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Главное окно"))
        self.menuActions.setTitle(_translate("MainWindow", "Действия"))
        self.actionDevelopment.setText(_translate("MainWindow", "Разработка"))
        self.actionNotifications.setText(_translate("MainWindow", "Уведомления"))
        self.actionHistory.setText(_translate("MainWindow", "История"))
        self.actionLetters.setText(_translate("MainWindow", "Письма"))
        self.actionProducts.setText(_translate("MainWindow", "Изделия"))
