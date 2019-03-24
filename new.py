# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GA.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import next as nxt

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):

    def GA(self):
        dataset_val= self.lv_dataset.currentItem().text()
        population_val= self.lv_population.currentItem().text()
        generation_val=  self.lv_generation.currentItem().text()

        print dataset_val, population_val, generation_val                   # current selection


        self.send=nxt.Ui_NextWindow()  
        self.send.get_values(dataset_val,population_val,generation_val)

        self.window=QtGui.QMainWindow()
        self.ui=nxt.Ui_NextWindow()
        self.ui.setupUi(self.window)
        self.window.show()
        MainWindow.hide()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setFixedSize(428, 342)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.Submit = QtGui.QPushButton(self.centralwidget)
        self.Submit.setGeometry(QtCore.QRect(160, 240, 111, 27))
        self.Submit.setObjectName(_fromUtf8("Submit"))
        self.dataset = QtGui.QLabel(self.centralwidget)
        self.dataset.setGeometry(QtCore.QRect(10, 30, 121, 21))
        self.dataset.setObjectName(_fromUtf8("dataset"))
        self.population = QtGui.QLabel(self.centralwidget)
        self.population.setGeometry(QtCore.QRect(160, 30, 101, 20))
        self.population.setObjectName(_fromUtf8("population"))
        self.generation = QtGui.QLabel(self.centralwidget)
        self.generation.setGeometry(QtCore.QRect(290, 30, 161, 20))
        self.generation.setObjectName(_fromUtf8("generation"))
        self.lv_dataset = QtGui.QListWidget(self.centralwidget)
        self.lv_dataset.setGeometry(QtCore.QRect(20, 60, 111, 131))
        self.lv_dataset.setObjectName(_fromUtf8("lv_dataset"))
        self.lv_dataset.addItems(["iris.csv", "nuclear.csv"])
        self.lv_population = QtGui.QListWidget(self.centralwidget)
        self.lv_population.setGeometry(QtCore.QRect(160, 60, 101, 131))
        self.lv_population.setObjectName(_fromUtf8("lv_population"))
        self.lv_population.addItems(["5","10","15","20"])
        self.lv_generation = QtGui.QListWidget(self.centralwidget)
        self.lv_generation.setGeometry(QtCore.QRect(300, 60, 101, 131))
        self.lv_generation.setObjectName(_fromUtf8("lv_generation"))
        self.lv_generation.addItems(["1","2","3","4","5","6","7","8","9","10"])
        MainWindow.setCentralWidget(self.centralwidget)


        self.Submit.clicked.connect(self.GA)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.Submit.setText(_translate("MainWindow", "Submit Values", None))
        self.dataset.setText(_translate("MainWindow", "Dataset Selection", None))
        self.population.setText(_translate("MainWindow", "Population No", None))
        self.generation.setText(_translate("MainWindow", " No. of Generations", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

