# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_help.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.setWindowModality(QtCore.Qt.ApplicationModal)
        Help.resize(600, 800)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Help.setWindowIcon(icon)
        Help.setStyleSheet("QWidget#Help{background-color: #FFFFFF; }")
        self.gridLayout = QtWidgets.QGridLayout(Help)
        self.gridLayout.setContentsMargins(0, -1, 0, 0)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.title = QtWidgets.QLabel(Help)
        self.title.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet("QLabel{border: 1px solid #8f8f91; border-radius: 5px}")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.gridLayout.addWidget(self.title, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(6, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 3, 1)
        spacerItem1 = QtWidgets.QSpacerItem(6, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.search_widget = QtWidgets.QWidget(Help)
        self.search_widget.setStyleSheet("QWidget#search_widget{border-right: 1px solid #B2B2B2;}")
        self.search_widget.setObjectName("search_widget")
        self.layer_recherche = QtWidgets.QHBoxLayout(self.search_widget)
        self.layer_recherche.setContentsMargins(0, 0, 0, 0)
        self.layer_recherche.setSpacing(0)
        self.layer_recherche.setObjectName("layer_recherche")
        self.search_bar = QtWidgets.QLineEdit(self.search_widget)
        self.search_bar.setMinimumSize(QtCore.QSize(300, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.search_bar.setFont(font)
        self.search_bar.setStyleSheet("QLineEdit{border: 1px solid #8f8f91; border-top-left-radius: 5px; border-bottom-left-radius: 5px; padding-left: 5px; }")
        self.search_bar.setObjectName("search_bar")
        self.layer_recherche.addWidget(self.search_bar)
        self.search_clear_bt = QtWidgets.QPushButton(self.search_widget)
        self.search_clear_bt.setMinimumSize(QtCore.QSize(40, 30))
        self.search_clear_bt.setMaximumSize(QtCore.QSize(40, 30))
        self.search_clear_bt.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-left-width: 0px; border-bottom-right-radius: 5px; border-top-right-radius: 5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.search_clear_bt.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/search_clear.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_clear_bt.setIcon(icon1)
        self.search_clear_bt.setIconSize(QtCore.QSize(20, 20))
        self.search_clear_bt.setFlat(True)
        self.search_clear_bt.setObjectName("search_clear_bt")
        self.layer_recherche.addWidget(self.search_clear_bt)
        self.gridLayout.addWidget(self.search_widget, 1, 1, 1, 1)
        self.fond = QtWidgets.QWidget(Help)
        self.fond.setMinimumSize(QtCore.QSize(0, 38))
        self.fond.setMaximumSize(QtCore.QSize(16777215, 38))
        self.fond.setStyleSheet("QWidget#fond{background: #DBE4EE}")
        self.fond.setObjectName("fond")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.fond)
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.quit = QtWidgets.QPushButton(self.fond)
        self.quit.setMinimumSize(QtCore.QSize(120, 24))
        self.quit.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.quit.setFont(font)
        self.quit.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.quit.setObjectName("quit")
        self.horizontalLayout.addWidget(self.quit)
        spacerItem3 = QtWidgets.QSpacerItem(6, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout.addWidget(self.fond, 3, 0, 1, 3)
        self.help_tree = QtWidgets.QTreeView(Help)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.help_tree.setFont(font)
        self.help_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.help_tree.setStyleSheet("QTreeView::item { height: 30px; }")
        self.help_tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.help_tree.setIconSize(QtCore.QSize(20, 20))
        self.help_tree.setAnimated(True)
        self.help_tree.setHeaderHidden(True)
        self.help_tree.setObjectName("help_tree")
        self.gridLayout.addWidget(self.help_tree, 2, 1, 1, 1)

        self.retranslateUi(Help)
        QtCore.QMetaObject.connectSlotsByName(Help)
        Help.setTabOrder(self.search_bar, self.search_clear_bt)
        Help.setTabOrder(self.search_clear_bt, self.help_tree)
        Help.setTabOrder(self.help_tree, self.quit)

    def retranslateUi(self, Help):
        _translate = QtCore.QCoreApplication.translate
        Help.setWindowTitle(_translate("Help", "Aide"))
        self.title.setText(_translate("Help", "Aide et Support"))
        self.search_bar.setToolTip(_translate("Help", "Rechercher"))
        self.search_bar.setPlaceholderText(_translate("Help", "Rechercher"))
        self.search_clear_bt.setToolTip(_translate("Help", "Supprimer la recherche"))
        self.quit.setText(_translate("Help", " Quitter"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Help = QtWidgets.QWidget()
    ui = Ui_Help()
    ui.setupUi(Help)
    Help.show()
    sys.exit(app.exec_())
