#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from catalog_manage import CatalogDatas
from main_datas import material_with_link_list, user_data_type, material_code, col_cat_desc
from tools import get_look_tableview, get_look_qs, qm_check
from ui_link_add import Ui_LinkAdd
from ui_link_add_again import Ui_LinkAddAgain


class LinkAdd(QWidget):
    link_add_signal = pyqtSignal(list)

    def __init__(self, catalogue):
        super().__init__()

        self.ui = Ui_LinkAdd()
        self.ui.setupUi(self)

        self.catalog: CatalogDatas = catalogue

        self.link_model = QStandardItemModel()

        self.link_filter = QSortFilterProxyModel()
        self.link_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.link_filter.setDynamicSortFilter(True)
        self.link_filter.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.link_filter.setSortLocaleAware(True)

        self.ui.links_list.setModel(self.link_filter)

        get_look_tableview(self.ui.links_list)

        self.ui.links_list.doubleClicked.connect(self.save)

        self.ui.links_list.selectionModel().selectionChanged.connect(self.add_button_manage)

        self.add_button_manage()

        self.ui.search_bar.textChanged.connect(self.link_filter.setFilterRegExp)
        self.ui.search_clear.clicked.connect(self.ui.search_bar.clear)

        self.ui.ok.clicked.connect(self.save)
        self.ui.quit.clicked.connect(self.close)

    @staticmethod
    def a___________________loading______():
        pass

    def link_creation_show(self, material_text: str):

        self.link_model.clear()

        a = self.tr("Ouvrage - Actuel")
        b = self.tr("Ouvrage contenant déjà des liens")

        search_start = self.catalog.cat_model.index(0, 0)

        qm_material_list = self.catalog.cat_model.match(search_start, user_data_type, material_code, -1,
                                                        Qt.MatchRecursive)

        for qm_val in qm_material_list:

            if not qm_check(qm_val):
                continue

            material_current = qm_val.data()

            if not isinstance(material_current, str):
                continue

            qm_parent = qm_val.parent()

            description = ""

            if qm_check(qm_parent):

                qm_description = self.catalog.cat_model.index(qm_val.row(), col_cat_desc, qm_parent)

                if qm_check(qm_description):
                    description = qm_description.data()

            if material_current == material_text:
                qs = self.creation_qs_unselectable(material_name=material_current, description=description, message=a)

            elif material_current.upper() in material_with_link_list:
                qs = self.creation_qs_unselectable(material_name=material_current, description=description, message=b)

            else:
                qs = self.creation_qs_selectable(material_name=material_current, description=description)

            self.link_model.appendRow(qs)

        self.link_filter.setSourceModel(self.link_model)
        self.link_filter.sort(0, Qt.AscendingOrder)

        self.show()

    @staticmethod
    def creation_qs_unselectable(material_name: str, description: str, message: str) -> QStandardItem:

        if description == "" or material_name == description:
            title = f'{material_name} -- [{message}]'
        else:
            title = f'{material_name} - {description} -- [{message}]'

        qs = get_look_qs(qs=QStandardItem(title), italic=True)
        qs.setForeground(QColor("red"))
        qs.setFlags(Qt.ItemIsEnabled)

        return qs

    @staticmethod
    def creation_qs_selectable(material_name: str, description: str) -> QStandardItem:

        if description == "" or material_name == description:
            title = f'{material_name}'
        else:
            title = f'{material_name} - {description}'

        qs = get_look_qs(qs=QStandardItem(title))

        qs.setData(material_name, user_data_type)
        qs.setData(description, Qt.UserRole + 2)

        return qs

    @staticmethod
    def a___________________boutons______():
        pass

    def add_button_manage(self):
        self.ui.ok.setEnabled(len(self.ui.links_list.selectionModel().selectedIndexes()) != 0)

    @staticmethod
    def a___________________save______():
        pass

    def save(self):

        qm_selection_list = self.ui.links_list.selectionModel().selectedIndexes()

        qm_selection_list.sort()

        link_list_add = list()

        for qm in qm_selection_list:

            if not qm_check(qm):
                continue

            material_name = qm.data(user_data_type)

            if not isinstance(material_name, str):
                continue

            description = qm.data(Qt.UserRole + 2)

            if not isinstance(description, str):
                description = ""

            link_list_add.append([material_name, description])

        self.link_add_signal.emit(link_list_add)
        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class LinKAddAgain(QWidget):
    link_creation_signal = pyqtSignal(list)
    link_open_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.Popup)

        self.ui = Ui_LinkAddAgain()
        self.ui.setupUi(self)

        self.link_model = QStandardItemModel()

        self.link_filter = QSortFilterProxyModel()
        self.link_filter.setSourceModel(self.link_model)
        self.link_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.ui.links_list.setModel(self.link_filter)

        self.ui.links_list.doubleClicked.connect(self.save)
        self.ui.links_list.selectionModel().selectionChanged.connect(self.add_button_manage)

        self.ui.search_bar.textChanged.connect(self.link_filter.setFilterRegExp)
        self.ui.search_clear.clicked.connect(self.ui.search_bar.clear)

        self.ui.ok.clicked.connect(self.save)
        self.ui.quit.clicked.connect(self.close)

        get_look_tableview(self.ui.links_list)

        self.add_button_manage()

    def add_button_manage(self):
        self.ui.ok.setEnabled(len(self.ui.links_list.selectionModel().selectedRows(0)) != 0)

    def save(self):
        qm = self.ui.links_list.currentIndex()

        if not qm_check(qm):
            return

        title = qm.data()

        if not isinstance(title, str):
            return

        material_name = qm.data(user_data_type)

        if not isinstance(material_name, str):
            return

        description = qm.data(Qt.UserRole + 2)

        if not isinstance(description, str):
            description = ""

        self.link_creation_signal.emit([[material_name, description]])

        self.close()

    @staticmethod
    def a___________________end______():
        pass
