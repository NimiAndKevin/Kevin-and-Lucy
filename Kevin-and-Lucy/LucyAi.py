from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                            "border : 1px solid white;\n"
                            "")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(240, 80, 421, 421))
        self.label.setText("")
        
        # Create a QMovie and set it to the QLabel for animation
        self.movie = QtGui.QMovie("../../Downloads/fxVE.gif")
        self.label.setMovie(self.movie)
        self.movie.start()  # Start the animation
        
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "LUCY"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    app_icon = QtGui.QIcon("C:\\Users\\surface\\Desktop\\icon-5887113_1280.webp")
    app.setWindowIcon(app_icon)
    Dialog.show()
    sys.exit(app.exec_())