# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_autocompletion.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Autocompletion(object):
    def setupUi(self, Autocompletion):
        Autocompletion.setObjectName("Autocompletion")
        Autocompletion.setWindowModality(QtCore.Qt.WindowModal)
        Autocompletion.resize(399, 300)
        Autocompletion.setWindowTitle("Form")
        Autocompletion.setStyleSheet("QWidget#Autocompletion {background:#FFFFFF}")
        self.gridLayout = QtWidgets.QGridLayout(Autocompletion)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.liste = QtWidgets.QTableView(Autocompletion)
        self.liste.setFocusPolicy(QtCore.Qt.NoFocus)
        self.liste.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.liste.setAlternatingRowColors(True)
        self.liste.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.liste.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.liste.setObjectName("liste")
        self.liste.horizontalHeader().setVisible(False)
        self.liste.horizontalHeader().setStretchLastSection(True)
        self.liste.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.liste, 0, 0, 1, 1)

        self.retranslateUi(Autocompletion)
        QtCore.QMetaObject.connectSlotsByName(Autocompletion)

    def retranslateUi(self, Autocompletion):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Autocompletion = QtWidgets.QWidget()
    ui = Ui_Autocompletion()
    ui.setupUi(Autocompletion)
    Autocompletion.show()
    sys.exit(app.exec_())
