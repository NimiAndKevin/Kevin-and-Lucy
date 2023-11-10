from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(898, 596)
        Dialog.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                            "border: 1px solid white;\n")
        
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(659, 433, 241, 161))
        self.pushButton.setStyleSheet("background-color: rgb(0, 0, 0;\n"
                                      "font: italic 20pt \"Noto Sans\";\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_window)
        self.pushButton.setIcon(QtGui.QIcon("C:\\Users\\surface\\Downloads\\Quit.png"))
        self.pushButton.setText("")  # Clear the button text
        self.pushButton.setIconSize(QtCore.QSize(200, 200))


        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 430, 471, 161))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setScaledContents(True)  # Enable scaling while maintaining aspect ratio

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(469, 423, 191, 171))
        self.pushButton_2.setStyleSheet("font: 20pt \"Segoe UI\";\n"
                                        "color: rgb(255, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.start_animation)
        self.pushButton_2.setIcon(QtGui.QIcon("C:\\Users\\surface\\Downloads\\Start.png"))
        self.pushButton_2.setText("")  # Clear the button text
        self.pushButton_2.setIconSize(QtCore.QSize(200, 200))

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 501, 431))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_2.setScaledContents(True)

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(500, 0, 401, 271))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_3.setScaledContents(True)

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(500, 270, 401, 171))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_4.setScaledContents(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "KEVIN"))
        self.pushButton.setText(_translate("Dialog", ""))
        self.pushButton_2.setText(_translate("Dialog", ""))

    def start_animation(self):
        self.movie1 = QtGui.QMovie("../00545cb7179c504433d4c8f5e845f286.gif")
        self.label.setMovie(self.movie1)
        self.movie1.start()

        self.movie2 = QtGui.QMovie("../../Downloads/MImN.gif")
        self.label_2.setMovie(self.movie2)
        self.movie2.start()

        self.movie3 = QtGui.QMovie("../../Downloads/Jarvis_Gui (1).gif")
        self.label_3.setMovie(self.movie3)
        self.movie3.start()

        self.movie4 = QtGui.QMovie("../../Downloads/Earth_Template.gif")
        self.label_4.setMovie(self.movie4)
        self.movie4.start()

    def close_window(self):
        QtWidgets.qApp.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    app_icon = QtGui.QIcon("C:\\Users\\surface\Downloads\\7gQj (1).gif")
    app.setWindowIcon(app_icon)
    Dialog.show()
    sys.exit(app.exec_())