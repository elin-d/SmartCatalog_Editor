# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_catalog_update.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CatalogUpdate(object):
    def setupUi(self, CatalogUpdate):
        CatalogUpdate.setObjectName("CatalogUpdate")
        CatalogUpdate.setWindowModality(QtCore.Qt.ApplicationModal)
        CatalogUpdate.resize(400, 400)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CatalogUpdate.setWindowIcon(icon)
        CatalogUpdate.setStyleSheet("QWidget#CatalogUpdate {background:#FFFFFF}")
        self.gridLayout = QtWidgets.QGridLayout(CatalogUpdate)
        self.gridLayout.setContentsMargins(0, 6, 0, 0)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.update_search = QtWidgets.QLineEdit(CatalogUpdate)
        self.update_search.setMinimumSize(QtCore.QSize(0, 30))
        self.update_search.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.update_search.setFont(font)
        self.update_search.setStyleSheet("QLineEdit{padding-left: 5px; border: 1px solid #8f8f91; border-right-width: 0px; border-top-left-radius:5px; border-bottom-left-radius: 5px; }")
        self.update_search.setClearButtonEnabled(True)
        self.update_search.setObjectName("update_search")
        self.horizontalLayout.addWidget(self.update_search)
        self.update_select = QtWidgets.QPushButton(CatalogUpdate)
        self.update_select.setMinimumSize(QtCore.QSize(30, 30))
        self.update_select.setMaximumSize(QtCore.QSize(30, 30))
        self.update_select.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-right-width: 0px; padding-right: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/select_all.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.update_select.setIcon(icon1)
        self.update_select.setIconSize(QtCore.QSize(20, 20))
        self.update_select.setObjectName("update_select")
        self.horizontalLayout.addWidget(self.update_select)
        self.update_none = QtWidgets.QPushButton(CatalogUpdate)
        self.update_none.setMinimumSize(QtCore.QSize(30, 30))
        self.update_none.setMaximumSize(QtCore.QSize(30, 30))
        self.update_none.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-top-right-radius:5px ; border-bottom-right-radius:5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/none.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.update_none.setIcon(icon2)
        self.update_none.setIconSize(QtCore.QSize(20, 20))
        self.update_none.setObjectName("update_none")
        self.horizontalLayout.addWidget(self.update_none)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.projects_table = QtWidgets.QTableView(CatalogUpdate)
        self.projects_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.projects_table.setAlternatingRowColors(True)
        self.projects_table.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.projects_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.projects_table.setSortingEnabled(True)
        self.projects_table.setObjectName("projects_table")
        self.projects_table.horizontalHeader().setStretchLastSection(True)
        self.projects_table.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.projects_table, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.fond = QtWidgets.QWidget(CatalogUpdate)
        self.fond.setMinimumSize(QtCore.QSize(0, 38))
        self.fond.setMaximumSize(QtCore.QSize(16777215, 38))
        self.fond.setStyleSheet("QWidget#fond{background: #DBE4EE}")
        self.fond.setObjectName("fond")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.fond)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.update_launch = QtWidgets.QPushButton(self.fond)
        self.update_launch.setMinimumSize(QtCore.QSize(120, 24))
        self.update_launch.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.update_launch.setFont(font)
        self.update_launch.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.update_launch.setShortcut("Ctrl+S")
        self.update_launch.setObjectName("update_launch")
        self.horizontalLayout_3.addWidget(self.update_launch)
        self.update_quit = QtWidgets.QPushButton(self.fond)
        self.update_quit.setMinimumSize(QtCore.QSize(120, 24))
        self.update_quit.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.update_quit.setFont(font)
        self.update_quit.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.update_quit.setShortcut("Esc")
        self.update_quit.setObjectName("update_quit")
        self.horizontalLayout_3.addWidget(self.update_quit)
        spacerItem3 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.gridLayout.addWidget(self.fond, 2, 0, 1, 3)

        self.retranslateUi(CatalogUpdate)
        QtCore.QMetaObject.connectSlotsByName(CatalogUpdate)
        CatalogUpdate.setTabOrder(self.update_search, self.update_select)
        CatalogUpdate.setTabOrder(self.update_select, self.update_none)
        CatalogUpdate.setTabOrder(self.update_none, self.projects_table)
        CatalogUpdate.setTabOrder(self.projects_table, self.update_launch)
        CatalogUpdate.setTabOrder(self.update_launch, self.update_quit)

    def retranslateUi(self, CatalogUpdate):
        _translate = QtCore.QCoreApplication.translate
        CatalogUpdate.setWindowTitle(_translate("CatalogUpdate", "Mettre à jour les catalogues"))
        self.update_search.setPlaceholderText(_translate("CatalogUpdate", "Rechercher"))
        self.update_launch.setText(_translate("CatalogUpdate", "Mettre à jour"))
        self.update_quit.setText(_translate("CatalogUpdate", "Annuler"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CatalogUpdate = QtWidgets.QWidget()
    ui = Ui_CatalogUpdate()
    ui.setupUi(CatalogUpdate)
    CatalogUpdate.show()
    sys.exit(app.exec_())
