#!/usr/bin/python3
# -*- coding: utf-8 -*

from hierarchy_qs import *

from tools import set_appearance_number
from ui_attribute_checkbox import Ui_AttributeCheckbox


class AttributeCheckbox(QWidget):
    attribute_changed_signal = pyqtSignal(QStandardItem, str, str, str)

    def __init__(self, qs_value: MyQstandardItem, attribute_datas: dict):
        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeCheckbox()
        self.ui.setupUi(self)

        # ----------------------------------

        if isinstance(attribute_datas, dict):

            self.ui.num_attrib.setText(attribute_datas.get(code_attr_number, ""))

            self.ui.name_attrib.setText(attribute_datas.get(code_attr_name, ""))
            self.ui.name_attrib.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.qs_value = qs_value
        valeur_qs = qs_value.text()

        if valeur_qs == "1":
            self.ui.value_attrib.setChecked(True)

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.value_attrib.clicked.connect(self.checkbox_update)

        # -----------------------------------------------

    @staticmethod
    def a___________________checkbox_loading______():
        pass

    def checkbox_loading(self):

        set_appearance_number(self.ui.num_attrib)

    @staticmethod
    def a___________________checkbox_update______():
        pass

    def checkbox_update(self):

        value_original = self.qs_value.text()

        if self.ui.value_attrib.isChecked():
            value_new = "1"
        else:
            value_new = "0"

        if value_original == value_new:
            return

        self.qs_value.setText(value_new)

        self.attribute_changed_signal.emit(self.qs_value, self.ui.num_attrib.text(), value_original, value_new)

    @staticmethod
    def a___________________end______():
        pass
