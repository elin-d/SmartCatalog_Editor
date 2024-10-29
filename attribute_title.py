#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *
from ui_title import Ui_Title


class AttributeTitle(QWidget):

    def __init__(self, asc, title: str):
        super().__init__()
        self.ui = Ui_Title()
        self.ui.setupUi(self)

        self.ui.title.setText(title)

        attributes_order_custom: bool = asc.attributes_order_custom
        attributes_order: int = asc.attributes_order
        attributes_order_col: int = asc.attributes_order_col
        attributes_order_list: list = asc.attributes_order_list

        if attributes_order_custom and len(attributes_order_list) != 0:
            self.ui.order_custom.setChecked(True)

        else:

            if attributes_order == 1 and attributes_order_col == 0:
                self.ui.order_91.setChecked(True)

            elif attributes_order == 0 and attributes_order_col == 1:
                self.ui.order_az.setChecked(True)

            elif attributes_order == 1 and attributes_order_col == 1:
                self.ui.order_za.setChecked(True)

            else:
                self.ui.order_19.setChecked(True)
