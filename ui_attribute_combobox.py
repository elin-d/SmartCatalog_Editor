# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Stockage\GIT\GitHub\smartest2\ui\ui_attribute_combobox.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AttributeCombobox(object):
    def setupUi(self, AttributeCombobox):
        AttributeCombobox.setObjectName("AttributeCombobox")
        AttributeCombobox.resize(750, 40)
        AttributeCombobox.setMinimumSize(QtCore.QSize(0, 40))
        AttributeCombobox.setMaximumSize(QtCore.QSize(16777215, 40))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(AttributeCombobox)
        self.horizontalLayout_3.setContentsMargins(15, 2, 15, 2)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.num_attrib = QtWidgets.QLabel(AttributeCombobox)
        self.num_attrib.setMinimumSize(QtCore.QSize(50, 26))
        self.num_attrib.setMaximumSize(QtCore.QSize(50, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.num_attrib.setFont(font)
        self.num_attrib.setAlignment(QtCore.Qt.AlignCenter)
        self.num_attrib.setObjectName("num_attrib")
        self.horizontalLayout_3.addWidget(self.num_attrib)
        self.name_attrib = QtWidgets.QLabel(AttributeCombobox)
        self.name_attrib.setMinimumSize(QtCore.QSize(240, 26))
        self.name_attrib.setMaximumSize(QtCore.QSize(240, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.name_attrib.setFont(font)
        self.name_attrib.setObjectName("name_attrib")
        self.horizontalLayout_3.addWidget(self.name_attrib)
        self.type_attrib = QtWidgets.QLabel(AttributeCombobox)
        self.type_attrib.setMinimumSize(QtCore.QSize(40, 26))
        self.type_attrib.setMaximumSize(QtCore.QSize(40, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.type_attrib.setFont(font)
        self.type_attrib.setStyleSheet("QLabel{color: grey; }")
        self.type_attrib.setAlignment(QtCore.Qt.AlignCenter)
        self.type_attrib.setObjectName("type_attrib")
        self.horizontalLayout_3.addWidget(self.type_attrib)
        self.combo_layer = QtWidgets.QHBoxLayout()
        self.combo_layer.setSpacing(0)
        self.combo_layer.setObjectName("combo_layer")
        self.value_attrib = QtWidgets.QComboBox(AttributeCombobox)
        self.value_attrib.setMinimumSize(QtCore.QSize(100, 26))
        self.value_attrib.setMaximumSize(QtCore.QSize(16777215, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.value_attrib.setFont(font)
        self.value_attrib.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.value_attrib.setStyleSheet("QComboBox { border: 1px solid #8f8f91; border-right-width: 0px; padding-right: 1px; border-top-left-radius:5px; border-bottom-left-radius:5px; padding-left: 5px; }\n"
"QComboBox::drop-down{width: 27px; padding-left: 1px; padding-right: 1px; background-color: #FFFFFF; }\n"
"QComboBox::drop-down:hover{border: 1px solid #8f8f91; border-top-width: 0px; border-bottom-width: 0px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #F8F8F8, stop:1 #8FADCC); }\n"
"QComboBox::drop-down:pressed{border: 1px solid #8f8f91; border-top-width: 0px; border-bottom-width: 0px; padding: 0px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #8FADCC, stop:1 #F8F8F8); }\n"
"QComboBox::down-arrow {image: url(:/Images/spin_down.svg); width: 12px; height: 12px; }\n"
"QComboBox QAbstractItemView{background-color:#FFFFFF; }\n"
"QFontComboBox QAbstractItemView::item:hover {background: #BAD0E7; }")
        self.value_attrib.setEditable(True)
        self.value_attrib.setObjectName("value_attrib")
        self.combo_layer.addWidget(self.value_attrib)
        self.index_attrib = QtWidgets.QLabel(AttributeCombobox)
        self.index_attrib.setMinimumSize(QtCore.QSize(40, 26))
        self.index_attrib.setMaximumSize(QtCore.QSize(40, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.index_attrib.setFont(font)
        self.index_attrib.setFocusPolicy(QtCore.Qt.NoFocus)
        self.index_attrib.setStyleSheet("QLabel{border: 1px solid #8f8f91; border-left-width: 0px; padding-left: 1px; border-right-width: 0px; padding-right: 1px; color: grey; background-color:#FFFFFF; }")
        self.index_attrib.setAlignment(QtCore.Qt.AlignCenter)
        self.index_attrib.setObjectName("index_attrib")
        self.combo_layer.addWidget(self.index_attrib)
        self.lock_attrib = QtWidgets.QPushButton(AttributeCombobox)
        self.lock_attrib.setEnabled(False)
        self.lock_attrib.setMinimumSize(QtCore.QSize(40, 26))
        self.lock_attrib.setMaximumSize(QtCore.QSize(40, 26))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.lock_attrib.setFont(font)
        self.lock_attrib.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lock_attrib.setStyleSheet("QPushButton{border: 1px solid #8f8f91; border-left-width: 0px; padding-left: 1px;  border-top-right-radius: 5px ; border-bottom-right-radius: 5px; background-color:#FFFFFF; }")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/attribute_editable.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lock_attrib.setIcon(icon)
        self.lock_attrib.setIconSize(QtCore.QSize(16, 16))
        self.lock_attrib.setFlat(True)
        self.lock_attrib.setObjectName("lock_attrib")
        self.combo_layer.addWidget(self.lock_attrib)
        self.horizontalLayout_3.addLayout(self.combo_layer)

        self.retranslateUi(AttributeCombobox)
        QtCore.QMetaObject.connectSlotsByName(AttributeCombobox)

    def retranslateUi(self, AttributeCombobox):
        _translate = QtCore.QCoreApplication.translate
        self.index_attrib.setToolTip(_translate("AttributeCombobox", "Index de l\'élément choisi"))
        self.lock_attrib.setToolTip(_translate("AttributeCombobox", "Cette liste déroulante est éditable"))
import icons_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AttributeCombobox = QtWidgets.QWidget()
    ui = Ui_AttributeCombobox()
    ui.setupUi(AttributeCombobox)
    AttributeCombobox.show()
    sys.exit(app.exec_())
