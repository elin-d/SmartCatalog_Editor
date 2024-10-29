#!/usr/bin/python3
# -*- coding: utf-8 -*

from hierarchy_qs import *
from tools import ValidatorInt, ValidatorDouble, format_float_value
from tools import set_appearance_number, set_appearence_type
from ui_attribute_lineedit import Ui_AttributeLineedit


class AttributeLineedit(QWidget):
    attribute_changes_signal = pyqtSignal(QStandardItem, str, str, str)

    def __init__(self, allplan_version: str,
                 qs_value: MyQstandardItem,
                 attribute_datas: dict,
                 is_material=False):

        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeLineedit()
        self.ui.setupUi(self)

        self.allplan_version = allplan_version

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.qs_value = qs_value
        self.ui.value_attrib.setText(self.qs_value.text())
        self.ui.value_attrib.home(False)

        # ----------------------------------

        if isinstance(attribute_datas, dict):

            self.attrib_option = attribute_datas.get(code_attr_option, code_attr_int)

            self.unit_attrib = attribute_datas.get(code_attr_unit, "")

            if is_material:
                min_value = attribute_datas.get(code_attr_min, -2147483648)
                max_value = attribute_datas.get(code_attr_max, 2147483647)

            else:

                min_value = -2147483648
                max_value = 2147483647

            self.ui.num_attrib.setText(attribute_datas.get(code_attr_number, ""))

            self.ui.name_attrib.setText(attribute_datas.get(code_attr_name, ""))
            self.ui.name_attrib.setToolTip(attribute_datas.get(code_attr_tooltips))

        else:

            self.attrib_option = code_attr_str

            self.unit_attrib = ""

            min_value = -2147483648
            max_value = 2147483647

        # ----------------------------------

        if not isinstance(min_value, str):

            self.min_value = None

        else:

            try:

                self.min_value = int(min_value)

            except Exception:

                self.min_value = None

        # ----------------------------------

        if not isinstance(max_value, str):

            self.max_value = None

        else:

            try:

                self.max_value = int(max_value)

            except Exception:

                self.max_value = None

        # ----------------------------------

        if self.unit_attrib != "":
            self.ui.unit_attrib.setText(self.unit_attrib)

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.value_attrib.textChanged.connect(self.lineedit_changed)
        self.ui.value_attrib.editingFinished.connect(self.lineedit_float_formatting)
        self.ui.value_attrib.installEventFilter(self)

        # -----------------------------------------------

    @staticmethod
    def a___________________lineedit_loading______():
        pass

    def lineedit_loading(self):

        set_appearance_number(self.ui.num_attrib)
        set_appearence_type(self.ui.type_attrib, self.attrib_option)

        self.ui.unit_attrib.setVisible(self.unit_attrib != "")

        if self.unit_attrib == "":
            self.ui.value_attrib.setStyleSheet("QLineEdit{"
                                               "padding-left: 5px;"
                                               "border: 1px solid #8f8f91;"
                                               "border-radius:5px}")

        if self.attrib_option == code_attr_int:
            self.ui.value_attrib.setValidator(ValidatorInt(min_val=self.min_value, max_val=self.max_value))
            return

        if self.attrib_option == code_attr_dbl:
            self.ui.value_attrib.setValidator(ValidatorDouble(min_val=self.min_value, max_val=self.max_value))
            return

    @staticmethod
    def a___________________changement______():
        pass

    def lineedit_changed(self):

        if self.attrib_option != code_attr_dbl:
            return

        current_text = self.ui.value_attrib.text()

        if self.allplan_version in ["2022", "2023"]:
            value = current_text.replace(".", ",")
        else:
            value = current_text.replace(",", ".")

        if value != current_text:
            cursor_position = self.ui.value_attrib.cursorPosition()

            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(value)
            self.ui.value_attrib.blockSignals(False)

            self.ui.value_attrib.setCursorPosition(cursor_position)

    def lineedit_float_formatting(self):

        if self.attrib_option != code_attr_dbl:
            self.lineedit_update()
            return

        current_text = self.ui.value_attrib.text()

        value = format_float_value(value=current_text, allplan_version=self.allplan_version)

        if value != current_text:
            cursor_position = self.ui.value_attrib.cursorPosition()

            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(value)
            self.ui.value_attrib.blockSignals(False)

            self.ui.value_attrib.setCursorPosition(cursor_position)

        self.lineedit_update()

    def lineedit_update(self):

        value_original = self.qs_value.text()
        value = self.ui.value_attrib.text()

        if value_original == value:
            return

        self.qs_value.setText(value)
        self.attribute_changes_signal.emit(self.qs_value, self.ui.num_attrib.text(), value_original, value)

    @staticmethod
    def a___________________end______():
        pass
