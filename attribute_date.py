#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from catalog_manage import MyQstandardItem
from main_datas import code_attr_number, code_attr_name, code_attr_tooltips, code_attr_option
from tools import ValidatorDate, move_widget_ss_bouton, set_appearance_number, date_formatting
from ui_attribute_date import Ui_AttributeDate
from ui_calendar import Ui_Calendar


class AttributeDate(QWidget):
    attribute_changed_signal = pyqtSignal(QStandardItem, str, str, str)

    def __init__(self, qs_value: MyQstandardItem, language, attribute_datas: dict):
        super().__init__()

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.ui = Ui_AttributeDate()
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
        self.ui.value_attrib.setText(self.qs_value.text())

        # -----------------------------------------------
        # Calendar
        # -----------------------------------------------

        self.calendar_widget = WidgetCalendar(parent_widget=self, language=language)
        self.calendar_widget.date_changed.connect(self.date_changed)

        # -----------------------------------------------
        # Validator
        # -----------------------------------------------

        self.ui.value_attrib.setValidator(ValidatorDate())

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.calendar_bt.clicked.connect(self.calendar_show)
        self.ui.value_attrib.editingFinished.connect(self.date_update)

        # -----------------------------------------------

    @staticmethod
    def a___________________date_loading______():
        pass

    def date_loading(self):

        set_appearance_number(self.ui.num_attrib)

    @staticmethod
    def a___________________date_changed______():
        pass

    def date_changed(self, new_date: str):

        self.ui.value_attrib.setText(new_date)
        self.ui.value_attrib.setFocus()

        self.date_update()

    def date_update(self):

        new_date = self.ui.value_attrib.text()
        date_formatted = date_formatting(new_date)

        date_original = self.qs_value.text()

        if date_formatted == "":
            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(date_original)
            self.ui.value_attrib.blockSignals(False)
            return

        if date_formatted != new_date:
            self.ui.value_attrib.blockSignals(True)
            self.ui.value_attrib.setText(date_formatted)
            self.ui.value_attrib.blockSignals(False)

        if date_original == date_formatted:
            return

        self.qs_value.setText(date_formatted)

        self.attribute_changed_signal.emit(self.qs_value, self.ui.num_attrib.text(), date_original, date_formatted)

    @staticmethod
    def a___________________dalendar_show______():
        pass

    def calendar_show(self):

        move_widget_ss_bouton(button=self.ui.calendar_bt, widget=self.calendar_widget)

        self.calendar_widget.calendar_loading(current_date=self.ui.value_attrib.text())

    @staticmethod
    def a___________________end______():
        pass


class WidgetCalendar(QWidget):
    date_changed = pyqtSignal(str)

    def __init__(self, parent_widget, language: str):
        super().__init__(parent=parent_widget)

        # -----------------------------------------------
        # Interface
        # -----------------------------------------------

        self.setWindowFlags(Qt.Popup)

        self.ui = Ui_Calendar()
        self.ui.setupUi(self)

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------
        self.current_date = ""

        if language != "FR":
            self.date_format = "MM/dd/yyyy"
        else:
            self.date_format = "dd/MM/yyyy"

        # -----------------------------------------------
        # Signal buttons
        # -----------------------------------------------

        self.ui.today.clicked.connect(self.calendar_select_today)
        self.installEventFilter(self)

    def calendar_loading(self, current_date: str):

        self.current_date = current_date
        self.ui.calendar_widget.setSelectedDate(QDate.fromString(self.current_date, self.date_format))
        self.ui.calendar_widget.setFocus()
        self.show()

    def calendar_select_today(self):

        self.ui.calendar_widget.setSelectedDate(QDate.currentDate())

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        current_date = self.ui.calendar_widget.selectedDate().toString(self.date_format)

        if current_date != self.current_date:
            self.date_changed.emit(current_date)

        super().closeEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if event.type() == QEvent.MouseButtonRelease:
            self.close()

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
