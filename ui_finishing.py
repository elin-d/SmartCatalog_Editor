# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_finishing.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Finishing(object):
    def setupUi(self, Finishing):
        Finishing.setObjectName("Finishing")
        Finishing.setWindowModality(QtCore.Qt.ApplicationModal)
        Finishing.resize(337, 315)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/asc.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Finishing.setWindowIcon(icon)
        Finishing.setStyleSheet("QWidget#Finishing{background-color: #FFFFFF}")
        self.gridLayout = QtWidgets.QGridLayout(Finishing)
        self.gridLayout.setContentsMargins(0, 6, 0, 0)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setObjectName("gridLayout")
        self.finishing_layer = QtWidgets.QVBoxLayout()
        self.finishing_layer.setObjectName("finishing_layer")
        self.finishing_title = QtWidgets.QLabel(Finishing)
        self.finishing_title.setMinimumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.finishing_title.setFont(font)
        self.finishing_title.setObjectName("finishing_title")
        self.finishing_layer.addWidget(self.finishing_title)
        self.finishing_layer_1 = QtWidgets.QHBoxLayout()
        self.finishing_layer_1.setSpacing(0)
        self.finishing_layer_1.setObjectName("finishing_layer_1")
        self.finishing = QtWidgets.QComboBox(Finishing)
        self.finishing.setMinimumSize(QtCore.QSize(0, 30))
        self.finishing.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.finishing.setFont(font)
        self.finishing.setStyleSheet("QComboBox { border: 1px solid #8f8f91; border-right-width: 0px; padding-right: 1px; border-top-left-radius:5px; border-bottom-left-radius:5px; padding-left: 5px; }\n"
"QComboBox::drop-down{width: 27px; padding-left: 1px; background-color: #FFFFFF; }\n"
"QComboBox::drop-down:hover{border-left: 1px solid #8f8f91; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QComboBox::drop-down:pressed{border-left: 1px solid #8f8f91; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QComboBox::down-arrow {image: url(:/Images/spin_down.svg); width: 12px; height: 12px; }\n"
"QComboBox QAbstractItemView{background-color:#FFFFFF; }\n"
"QFontComboBox QAbstractItemView::item:hover {background: #BAD0E7; }")
        self.finishing.setIconSize(QtCore.QSize(20, 20))
        self.finishing.setObjectName("finishing")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/room_floor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.finishing.addItem(icon1, "")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/room_baseboard.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.finishing.addItem(icon2, "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Images/room_wall.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.finishing.addItem(icon3, "")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Images/room_ceilling.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.finishing.addItem(icon4, "")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Images/room_other.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.finishing.addItem(icon5, "")
        self.finishing_layer_1.addWidget(self.finishing)
        self.help = QtWidgets.QPushButton(Finishing)
        self.help.setMinimumSize(QtCore.QSize(30, 30))
        self.help.setMaximumSize(QtCore.QSize(30, 30))
        self.help.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-top-right-radius:5px ; border-bottom-right-radius:5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.help.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Images/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help.setIcon(icon6)
        self.help.setIconSize(QtCore.QSize(20, 20))
        self.help.setObjectName("help")
        self.finishing_layer_1.addWidget(self.help)
        self.finishing_layer.addLayout(self.finishing_layer_1)
        self.gridLayout.addLayout(self.finishing_layer, 0, 1, 1, 1)
        self.attribute_layer = QtWidgets.QVBoxLayout()
        self.attribute_layer.setObjectName("attribute_layer")
        self.attribute_title = QtWidgets.QLabel(Finishing)
        self.attribute_title.setMinimumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.attribute_title.setFont(font)
        self.attribute_title.setObjectName("attribute_title")
        self.attribute_layer.addWidget(self.attribute_title)
        self.attribute_layer_1 = QtWidgets.QHBoxLayout()
        self.attribute_layer_1.setSpacing(0)
        self.attribute_layer_1.setObjectName("attribute_layer_1")
        self.attribute = QtWidgets.QComboBox(Finishing)
        self.attribute.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.attribute.setFont(font)
        self.attribute.setStyleSheet("QComboBox { border: 1px solid #8f8f91; border-right-width: 0px; padding-right: 1px; border-top-left-radius:5px; border-bottom-left-radius:5px; padding-left: 5px; }\n"
"QComboBox::drop-down{width: 27px; padding-left: 1px; background-color: #FFFFFF; }\n"
"QComboBox::drop-down:hover{border-left: 1px solid #8f8f91; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QComboBox::drop-down:pressed{border-left: 1px solid #8f8f91; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QComboBox::down-arrow {image: url(:/Images/spin_down.svg); width: 12px; height: 12px; }\n"
"QComboBox QAbstractItemView{background-color:#FFFFFF; }\n"
"QFontComboBox QAbstractItemView::item:hover {background: #BAD0E7; }")
        self.attribute.setIconSize(QtCore.QSize(20, 20))
        self.attribute.setObjectName("attribute")
        self.attribute_layer_1.addWidget(self.attribute)
        self.attribute_add = QtWidgets.QPushButton(Finishing)
        self.attribute_add.setMinimumSize(QtCore.QSize(30, 30))
        self.attribute_add.setMaximumSize(QtCore.QSize(30, 30))
        self.attribute_add.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-top-right-radius:5px ; border-bottom-right-radius:5px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.attribute_add.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Images/attribute_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.attribute_add.setIcon(icon7)
        self.attribute_add.setIconSize(QtCore.QSize(20, 20))
        self.attribute_add.setObjectName("attribute_add")
        self.attribute_layer_1.addWidget(self.attribute_add)
        self.attribute_layer.addLayout(self.attribute_layer_1)
        self.gridLayout.addLayout(self.attribute_layer, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.layer_layer = QtWidgets.QGridLayout()
        self.layer_layer.setSpacing(3)
        self.layer_layer.setObjectName("layer_layer")
        self.layer_02 = QtWidgets.QPushButton(Finishing)
        self.layer_02.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_02.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_02.setFont(font)
        self.layer_02.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_02.setText("2")
        self.layer_02.setCheckable(True)
        self.layer_02.setObjectName("layer_02")
        self.layer_layer.addWidget(self.layer_02, 1, 1, 1, 1)
        self.layer_upper = QtWidgets.QPushButton(Finishing)
        self.layer_upper.setMinimumSize(QtCore.QSize(0, 24))
        self.layer_upper.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_upper.setFont(font)
        self.layer_upper.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_upper.setCheckable(True)
        self.layer_upper.setChecked(True)
        self.layer_upper.setObjectName("layer_upper")
        self.layer_layer.addWidget(self.layer_upper, 1, 6, 1, 1)
        self.layer_06 = QtWidgets.QPushButton(Finishing)
        self.layer_06.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_06.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_06.setFont(font)
        self.layer_06.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_06.setText("6")
        self.layer_06.setCheckable(True)
        self.layer_06.setObjectName("layer_06")
        self.layer_layer.addWidget(self.layer_06, 2, 0, 1, 1)
        self.layer_title = QtWidgets.QLabel(Finishing)
        self.layer_title.setMinimumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.layer_title.setFont(font)
        self.layer_title.setObjectName("layer_title")
        self.layer_layer.addWidget(self.layer_title, 0, 0, 1, 7)
        self.layer_01 = QtWidgets.QPushButton(Finishing)
        self.layer_01.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_01.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_01.setFont(font)
        self.layer_01.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_01.setText("1")
        self.layer_01.setCheckable(True)
        self.layer_01.setObjectName("layer_01")
        self.layer_layer.addWidget(self.layer_01, 1, 0, 1, 1)
        self.layer_05 = QtWidgets.QPushButton(Finishing)
        self.layer_05.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_05.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_05.setFont(font)
        self.layer_05.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_05.setText("5")
        self.layer_05.setCheckable(True)
        self.layer_05.setObjectName("layer_05")
        self.layer_layer.addWidget(self.layer_05, 1, 4, 1, 1)
        self.layer_04 = QtWidgets.QPushButton(Finishing)
        self.layer_04.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_04.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_04.setFont(font)
        self.layer_04.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_04.setText("4")
        self.layer_04.setCheckable(True)
        self.layer_04.setObjectName("layer_04")
        self.layer_layer.addWidget(self.layer_04, 1, 3, 1, 1)
        self.layer_10 = QtWidgets.QPushButton(Finishing)
        self.layer_10.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_10.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_10.setFont(font)
        self.layer_10.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_10.setText("10")
        self.layer_10.setCheckable(True)
        self.layer_10.setObjectName("layer_10")
        self.layer_layer.addWidget(self.layer_10, 2, 4, 1, 1)
        self.layer_07 = QtWidgets.QPushButton(Finishing)
        self.layer_07.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_07.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_07.setFont(font)
        self.layer_07.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_07.setText("7")
        self.layer_07.setCheckable(True)
        self.layer_07.setObjectName("layer_07")
        self.layer_layer.addWidget(self.layer_07, 2, 1, 1, 1)
        self.layer_08 = QtWidgets.QPushButton(Finishing)
        self.layer_08.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_08.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_08.setFont(font)
        self.layer_08.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_08.setText("8")
        self.layer_08.setCheckable(True)
        self.layer_08.setObjectName("layer_08")
        self.layer_layer.addWidget(self.layer_08, 2, 2, 1, 1)
        self.layer_09 = QtWidgets.QPushButton(Finishing)
        self.layer_09.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_09.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_09.setFont(font)
        self.layer_09.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_09.setText("9")
        self.layer_09.setCheckable(True)
        self.layer_09.setObjectName("layer_09")
        self.layer_layer.addWidget(self.layer_09, 2, 3, 1, 1)
        self.layer_all = QtWidgets.QPushButton(Finishing)
        self.layer_all.setMinimumSize(QtCore.QSize(0, 24))
        self.layer_all.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_all.setFont(font)
        self.layer_all.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_all.setCheckable(True)
        self.layer_all.setObjectName("layer_all")
        self.layer_layer.addWidget(self.layer_all, 2, 6, 1, 1)
        self.layer_03 = QtWidgets.QPushButton(Finishing)
        self.layer_03.setMinimumSize(QtCore.QSize(35, 24))
        self.layer_03.setMaximumSize(QtCore.QSize(35, 30))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.layer_03.setFont(font)
        self.layer_03.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius:5px ; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QPushButton:hover:!checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:hover::checked{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #BAD0E7, stop:1 #FFFFFF); }")
        self.layer_03.setText("3")
        self.layer_03.setCheckable(True)
        self.layer_03.setObjectName("layer_03")
        self.layer_layer.addWidget(self.layer_03, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(Finishing)
        self.label.setMinimumSize(QtCore.QSize(3, 0))
        self.label.setMaximumSize(QtCore.QSize(3, 16777215))
        self.label.setText("")
        self.label.setObjectName("label")
        self.layer_layer.addWidget(self.label, 1, 5, 1, 1)
        self.gridLayout.addLayout(self.layer_layer, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(9, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.fond = QtWidgets.QWidget(Finishing)
        self.fond.setMinimumSize(QtCore.QSize(0, 38))
        self.fond.setMaximumSize(QtCore.QSize(16777215, 38))
        self.fond.setStyleSheet("QWidget#fond{background-color: #DBE4EE}")
        self.fond.setObjectName("fond")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.fond)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(157, 50, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.ok = QtWidgets.QPushButton(self.fond)
        self.ok.setMinimumSize(QtCore.QSize(120, 24))
        self.ok.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.ok.setFont(font)
        self.ok.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-radius: 5px ; padding-right: 10px; padding-left: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #BAD0E7); }\n"
"QPushButton:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }")
        self.ok.setShortcut("Ctrl+S")
        self.ok.setObjectName("ok")
        self.horizontalLayout_4.addWidget(self.ok)
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
        self.quit.setShortcut("Esc")
        self.quit.setObjectName("quit")
        self.horizontalLayout_4.addWidget(self.quit)
        spacerItem3 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.gridLayout.addWidget(self.fond, 3, 0, 1, 3)

        self.retranslateUi(Finishing)
        QtCore.QMetaObject.connectSlotsByName(Finishing)

    def retranslateUi(self, Finishing):
        _translate = QtCore.QCoreApplication.translate
        Finishing.setWindowTitle(_translate("Finishing", "Second-Œuvre"))
        self.finishing_title.setText(_translate("Finishing", "Type Second-Œuvre "))
        self.finishing.setItemText(0, _translate("Finishing", "Sol"))
        self.finishing.setItemText(1, _translate("Finishing", "Plinthe"))
        self.finishing.setItemText(2, _translate("Finishing", "Paroi verticale (mur)"))
        self.finishing.setItemText(3, _translate("Finishing", "Plafond"))
        self.finishing.setItemText(4, _translate("Finishing", "Matériaux supplémentaires"))
        self.attribute_title.setText(_translate("Finishing", "Information / Attribut à récupérer"))
        self.layer_upper.setText(_translate("Finishing", "Supérieure"))
        self.layer_title.setText(_translate("Finishing", "Couches à évaluer"))
        self.layer_all.setText(_translate("Finishing", "Toutes"))
        self.ok.setText(_translate("Finishing", "Ajouter"))
        self.quit.setText(_translate("Finishing", "Quitter"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Finishing = QtWidgets.QWidget()
    ui = Ui_Finishing()
    ui.setupUi(Finishing)
    Finishing.show()
    sys.exit(app.exec_())
