#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from allplan_manage import AllplanDatas
from main_datas import get_icon, material_icon, component_icon
from tools import get_look_tableview, qm_check, MyContextMenu
from ui_attribute_link import Ui_AttributeLink


class AttributeLink(QWidget):
    material_open = pyqtSignal(str)
    component_open = pyqtSignal(str, str)

    def __init__(self, allplan, link_model):
        super().__init__()

        # Chargement du widget + setup
        self.ui = Ui_AttributeLink()
        self.ui.setupUi(self)

        self.allplan: AllplanDatas = allplan

        self.material_name = ""

        self.ui.bt_afficher.clicked.connect(self.material_show)

        self.link_model = link_model

        self.ui.liste_composants.setModel(self.link_model)

        get_look_tableview(self.ui.liste_composants)

        self.ui.liste_composants.expandAll()

        self.link_manage_header()

        self.ui.liste_composants.doubleClicked.connect(self.component_show)

        self.ui.liste_composants.customContextMenuRequested.connect(self.menu_show)

    def material_show(self):
        self.material_open.emit(self.material_name)

    def component_show(self, qm_component: QModelIndex):

        if not qm_check(qm_component):
            return

        if qm_component.column() != 0:
            qm_component = self.link_model.index(qm_component.row(), 0)
            if not qm_check(qm_component):
                return

        component_txt = qm_component.data()

        if isinstance(component_txt, str) and component_txt != "":
            self.component_open.emit(self.material_name, component_txt)

    def menu_show(self, point: QPoint):

        qm_component = self.ui.liste_composants.indexAt(point)

        if not qm_check(qm_component):
            return

        point = QPoint(point.x(), point.y() + 35)

        menu = MyContextMenu()

        menu.add_title(title=self.tr("Lien"))

        menu.add_action(qicon=get_icon(material_icon),
                        title=self.tr("Afficher l'ouvrage"),
                        action=self.material_show)

        menu.add_action(qicon=get_icon(component_icon),
                        title=self.tr('Afficher le composant'),
                        action=lambda: self.component_show(qm_component=qm_component))

        menu.exec_(self.ui.liste_composants.mapToGlobal(point))

    def link_manage_header(self):

        row_count = self.link_model.rowCount()

        if row_count == 0:
            return

        size_now = self.ui.liste_composants.header().sectionSize(0)

        self.ui.liste_composants.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        size_after = self.ui.liste_composants.header().sectionSize(0)

        if size_after < size_now:
            self.ui.liste_composants.header().setSectionResizeMode(0, QHeaderView.Interactive)
            self.ui.liste_composants.header().resizeSection(0, size_now)
        else:
            self.ui.liste_composants.header().setSectionResizeMode(0, QHeaderView.Interactive)