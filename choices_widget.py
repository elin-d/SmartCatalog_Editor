#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from main_datas import application_title
from tools import changer_selection_apparence, qm_check, move_window_tool
from ui_choices import Ui_Choices


class ChoicesWidget(QDialog):
    save_modif_choice = pyqtSignal(str, list)

    def __init__(self, asc):
        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_Choices()
        self.ui.setupUi(self)

        self.setWindowTitle(application_title)

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.choices_model = QStandardItemModel()

        self.ui.choices_table.setModel(self.choices_model)

        changer_selection_apparence(self.ui.choices_table)

        self.choice_dict = dict()
        self.save_ok = False

        self.ui.choices_table.doubleClicked.connect(self.choices_save)

        self.ui.ok.clicked.connect(self.choices_save)
        self.ui.quit.clicked.connect(self.close)

    def choice_show(self, choice_dict: dict, title: str):

        self.save_ok = False
        self.choice_dict = choice_dict

        self.ui.title.setText(title)

        self.choices_model.clear()

        for choice in choice_dict.keys():

            if isinstance(choice, str):
                self.choices_model.appendRow([QStandardItem(choice)])

        self.ui.choices_table.setCurrentIndex(self.choices_model.index(0, 0))

        self.ui.ok.setFocus()

        move_window_tool(widget_parent=self.asc, widget_current=self)

        self.exec()

    @staticmethod
    def a___________________save______():
        pass

    def choices_save(self):

        selection_list = self.ui.choices_table.selectionModel().selectedRows()

        if len(selection_list) != 1:
            self.close()
            return

        qm = selection_list[0]

        if not qm_check(qm):
            self.close()
            return

        value = qm.data()

        if value not in self.choice_dict:
            self.close()
            return

        files_list = self.choice_dict.get(value, list())

        self.save_modif_choice.emit(value, files_list)
        self.save_ok = True
        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        super().keyPressEvent(event)

        if event.key() == Qt.Key_Escape:
            self.close()
            return

    def closeEvent(self, event: QCloseEvent):

        if not self.save_ok:
            self.save_modif_choice.emit("", list())

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass
