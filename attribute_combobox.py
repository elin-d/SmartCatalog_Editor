#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from main_datas import lock_icon, get_icon, code_attr_tooltips, code_attr_option, code_attr_combo_str_edit, \
    code_attr_name, code_attr_number
from tools import ValidatorDouble, ValidatorInt, ValidatorModel, set_appearance_number, get_look_combobox
from tools import set_appearence_type
from ui_attribute_combobox import Ui_AttributeCombobox


class AttributeCombobox(QWidget):
    attribute_changed_signal = pyqtSignal(QStandardItem, str, str, str, str, str)

    def __init__(self, model_combo: QStandardItemModel,
                 attribute_datas: dict,
                 qs_value: QStandardItem,
                 qs_index: QStandardItem):

        super().__init__()

        self.ui = Ui_AttributeCombobox()
        self.ui.setupUi(self)

        self.qs_value = qs_value
        self.qs_index = qs_index

        # ----------------------------------

        if isinstance(attribute_datas, dict):

            self.ui.num_attrib.setText(attribute_datas.get(code_attr_number, ""))

            self.ui.name_attrib.setText(attribute_datas.get(code_attr_name, ""))
            self.ui.name_attrib.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

            self.attrib_option = attribute_datas.get(code_attr_option, code_attr_combo_str_edit)

        else:

            self.attrib_option = code_attr_combo_str_edit

        # ----------------------------------

        self.combo_model = model_combo

        self.combo_filter = QSortFilterProxyModel()
        self.combo_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.combo_filter.setSourceModel(self.combo_model)
        self.combo_filter.setFilterKeyColumn(1)

        self.ui.value_attrib.setModel(self.combo_model)
        self.ui.value_attrib.setModelColumn(1)

        get_look_combobox(self.ui.value_attrib)

        combo_qcompleter = QCompleter()
        combo_qcompleter.setModel(self.combo_filter)
        combo_qcompleter.setCompletionColumn(1)
        combo_qcompleter.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        combo_qcompleter.setCaseSensitivity(Qt.CaseInsensitive)

        self.ui.value_attrib.setCompleter(combo_qcompleter)

        self.ui.value_attrib.setCurrentText(self.qs_value.text())
        self.ui.index_attrib.setText(self.qs_index.text())

        self.ui.value_attrib.lineEdit().textEdited.connect(self.combo_filter.setFilterFixedString)
        self.ui.value_attrib.currentIndexChanged.connect(self.combo_changed)

        self.ui.value_attrib.installEventFilter(self)

    @staticmethod
    def a___________________combobox_loading______():
        pass

    def combo_loading(self):

        set_appearance_number(self.ui.num_attrib)
        set_appearence_type(self.ui.type_attrib, self.attrib_option)

        if "entier" in self.attrib_option:
            self.ui.value_attrib.setValidator(ValidatorInt())

        elif "décimal" in self.attrib_option:
            self.ui.value_attrib.setValidator(ValidatorDouble())

        if "modifiable" in self.attrib_option:
            self.ui.lock_attrib.setIcon(get_icon(lock_icon))

            self.ui.lock_attrib.setToolTip(self.tr("Cette liste déroulante n'est pas éditable"))

            self.ui.value_attrib.setValidator(ValidatorModel(self.ui.value_attrib.model()))

    @staticmethod
    def a___________________combobox_changed______():
        pass

    def combo_changed(self):

        if self.combo_model.rowCount() == 0:
            return

        if self.ui.value_attrib.view().isVisible():
            return False

        value_attrib = self.ui.value_attrib.currentText()
        row_index = self.ui.value_attrib.currentIndex()

        if row_index == -1 or value_attrib.strip() == "":
            search_index = self.ui.value_attrib.findText("", Qt.MatchExactly)
            self.ui.value_attrib.setCurrentIndex(search_index)
            self.combo_refresh_index(search_index)
            return

        search = self.ui.value_attrib.findText(value_attrib, Qt.MatchExactly)

        if search == -1:

            if self.ui.num_attrib.text() != "202":
                search_index = self.ui.value_attrib.findText(self.qs_value.text(), Qt.MatchExactly)

                self.ui.value_attrib.setCurrentIndex(search_index)
                self.combo_refresh_index(search_index)

                return

            row_count = self.combo_model.rowCount()
            self.combo_model.appendRow([QStandardItem(f"{row_count}"), QStandardItem(value_attrib)])

        invalid_index = self.ui.value_attrib.findText(self.tr("Index non valide !"), Qt.MatchExactly)

        if invalid_index != -1:
            self.ui.value_attrib.removeItem(invalid_index)

        if search != row_index:
            numero_element = self.combo_model.index(search, 0).data(Qt.DisplayRole)

        else:
            numero_element = self.combo_model.index(row_index, 0).data(Qt.DisplayRole)

        self.ui.index_attrib.setText(numero_element)

        self.combo_update_datas()

    def combo_refresh_index(self, index_row: int):

        if index_row == -1:
            self.ui.index_attrib.setText("-1")
            self.qs_index.setText("-1")
            return

        qmodelindex: QModelIndex = self.combo_model.index(index_row, 0)

        if qmodelindex is None:
            return

        numero_element = qmodelindex.data()

        self.ui.index_attrib.setText(numero_element)

        self.combo_update_datas()

    def combo_update_datas(self):

        if not self.isVisible():
            return

        valeur_originale = self.qs_value.text()
        nouveau_texte = self.ui.value_attrib.currentText()

        ancien_index = self.qs_index.text()
        nouvel_index = self.ui.index_attrib.text()

        if valeur_originale == nouveau_texte and ancien_index == nouvel_index:
            return

        self.qs_value.setText(nouveau_texte)
        self.qs_index.setText(nouvel_index)

        self.attribute_changed_signal.emit(self.qs_value,
                                           self.ui.num_attrib.text(), valeur_originale, nouveau_texte, ancien_index,
                                           nouvel_index)

    @staticmethod
    def a___________________event______():
        pass

    def eventFilter(self, obj: QWidget, event: QEvent):

        if obj != self.ui.value_attrib:
            return super().eventFilter(obj, event)

        if not isinstance(obj, QComboBox):
            return super().eventFilter(obj, event)

        if obj.view().isVisible():
            return super().eventFilter(obj, event)

        if event.type() == QEvent.FocusOut:
            self.combo_changed()
            return super().eventFilter(obj, event)

        if event.type() == QEvent.Wheel:
            if not self.ui.value_attrib.hasFocus():
                event.ignore()
                return True
            else:
                event.accept()
                return super().eventFilter(obj, event)

        if event.type() != QEvent.KeyPress:
            return super().eventFilter(obj, event)

        if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
            event.ignore()
            return True

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
