#!/usr/bin/python3
# -*- coding: utf-8 -*
from attribute_lineedit_str import AttributeLineeditStr
from catalog_manage import *
from attribute_date import AttributeDate
from attribute_checkbox import AttributeCheckbox
from attribute_code import AttributeCode
from attribute_combobox import AttributeCombobox
from formula_attribute import AttributeFormula
from link_attribute import AttributeLink
from attribute_lineedit import AttributeLineedit
from attribute_name import AttributeName
from attribute_335 import Attribute335
from attribute_layer import AttributeLayer
from room_attribute import AttributeRoom
from attribute_filling import AttributeFilling
from attribute_title import AttributeTitle


class AttributesDetailLoader(QWidget):

    def __init__(self, asc):
        super().__init__()

        self.asc = asc

        self.catalog: CatalogDatas = self.asc.catalog
        self.allplan: AllplanDatas = self.asc.allplan

        self.liste_details: QListWidget = self.asc.ui.attributes_detail

    @staticmethod
    def a___________________creation_widgets______():
        pass

    def add_name(self, qs_value: QStandardItem, qs_selection_list=None):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setFlags(listwidgetitem.flags() & ~Qt.ItemIsSelectable)
        listwidgetitem.setData(user_data_type, type_nom)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeName(allplan=self.allplan,
                               qs_value=qs_value,
                               qs_selection_list=qs_selection_list)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        widget.attribute_changed_signal.connect(self.catalog.catalog_header_manage)

        widget.icon_changed_signal.connect(self.catalog.undo_icon_changed)

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.formatting_bt.installEventFilter(self)
        widget.ui.verification_bt.installEventFilter(self)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setData(user_data_number, "Nom")
        listwidgetitem.setSizeHint(widget.sizeHint())

        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def ajouter_lien(self, parent_index: QModelIndex, current_row: int, link_model: QStandardItemModel):

        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setFlags(listwidgetitem.flags() & ~Qt.ItemIsSelectable)
        listwidgetitem.setData(user_data_type, type_lien)

        # Création widget
        # ---------------

        widget = AttributeLink(allplan=self.allplan, link_model=link_model)

        widget.ui.bt_afficher.installEventFilter(self)
        widget.ui.liste_composants.installEventFilter(self)

        widget.material_open.connect(self.catalog.goto_material)
        widget.component_open.connect(self.catalog.goto_component)

        # Création mapper
        # ---------------

        qm_material_name = self.catalog.cat_model.index(current_row, col_cat_value, parent_index)

        if not qm_check(qm_material_name):
            material_name = self.tr("Lien")
        else:
            material_name = qm_material_name.data()

        qm_material_desc = self.catalog.cat_model.index(current_row, col_cat_desc, parent_index)

        if not qm_check(qm_material_desc):
            description = ""
        else:
            description = qm_material_desc.data()

        if description != "" and description != material_name:
            title = f"{material_name} - {description}"
        else:
            title = material_name

        widget.ui.nom_attr.setText(title)

        widget.material_name = material_name

        # Création listwidgetitem
        # ---------------

        listwidgetitem.setData(user_data_number, "Lien")
        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

    def add_code(self, qs_value: MyQstandardItem, forbidden_names_list: list, attribute_datas: dict,
                 material_linked=False):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setFlags(listwidgetitem.flags() & ~Qt.ItemIsSelectable)
        listwidgetitem.setData(user_data_type, type_code)

        # listwidgetitem.setBackground(QColor("#e9e7e3"))

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeCode(qs_value=qs_value,
                               material_linked=material_linked,
                               forbidden_names_list=forbidden_names_list,
                               attribute_datas=attribute_datas)

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.formatting_bt.installEventFilter(self)
        widget.ui.verification_bt.installEventFilter(self)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.code_changed_signal.connect(self.catalog.material_code_renamed)

        if material_linked:
            widget.link_code_changed_signal.connect(self.catalog.link_refresh_code)
            self.catalog.material_update_link_number(widget.ui.value_attrib.text())

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        widget.attribute_changed_signal.connect(self.catalog.catalog_header_manage)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setData(user_data_number, attribute_default_base)
        listwidgetitem.setSizeHint(widget.sizeHint())

        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_lineedit(self, qs_value: MyQstandardItem, attribute_datas: dict,
                     is_material=False):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_ligne)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeLineedit(allplan_version=self.allplan.version_allplan_current,
                                   qs_value=qs_value,
                                   attribute_datas=attribute_datas,
                                   is_material=is_material)

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.lineedit_loading()

        # ------------------------
        # Creation signals
        # ------------------------

        widget.attribute_changes_signal.connect(self.catalog.undo_modify_attribute)

        widget.ui.value_attrib.installEventFilter(self)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setData(user_data_number, widget.ui.num_attrib.text())

        listwidgetitem.setSizeHint(widget.sizeHint())

        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_lineedit_str(self, qm_parent: QModelIndex, qs_value: MyQstandardItem, qs_desc, attribute_datas: dict,
                         is_material=False):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_ligne)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeLineeditStr(allplan_version=self.allplan.version_allplan_current,
                                      qs_value=qs_value,
                                      qs_desc=qs_desc,
                                      attribute_datas=attribute_datas,
                                      is_material=is_material,
                                      listwidgetitem=listwidgetitem)

        # ------------------------
        # Creation mapper -- code
        # ------------------------

        mapper_parent = QDataWidgetMapper(self.asc)
        mapper_parent.setModel(self.catalog.cat_model)

        mapper_parent.addMapping(widget.code_title, col_cat_value, b"text")

        code_index: QModelIndex = qm_parent.parent()

        mapper_parent.setRootIndex(code_index)
        mapper_parent.setCurrentIndex(qm_parent.row())

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.lineedit_loading()

        self.asc.ui.splitter.splitterMoved.connect(widget.adjust_width)
        self.asc.ui_resized.connect(widget.adjust_width)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.formatting_bt.installEventFilter(self)

        widget.link_desc_changed_signal.connect(self.catalog.link_refresh_desc)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setData(user_data_number, widget.ui.num_attrib.text())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_formula(self, qs_val: QStandardItem, attribute_datas: dict):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_formule)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeFormula(asc=self.asc,
                                  qs_value=qs_val,
                                  attribute_datas=attribute_datas,
                                  listwidgetitem=listwidgetitem)

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.chargement()

        self.asc.ui.splitter.splitterMoved.connect(widget.adjust_width)
        self.asc.ui_resized.connect(widget.adjust_width)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.viewport().installEventFilter(self)
        widget.ui.formula_verification_bt.installEventFilter(self)
        widget.ui.formula_editor_bt.installEventFilter(self)
        widget.ui.formula_color_bt.installEventFilter(self)
        widget.ui.formula_favorite_bt.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)
        widget.formula_changed.connect(self.catalog.erreur_selectionner_premiere)

        widget.ui.value_attrib.size_change.connect(self.catalog.formula_size_change_signal.emit)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setData(user_data_number, widget.ui.num_attrib.text())

        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_combobox(self, qs_value: QStandardItem, qs_index: QStandardItem, attribute_datas: dict):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_combo)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeCombobox(model_combo=attribute_datas.get(code_attr_enumeration, QStandardItemModel()),
                                   attribute_datas=attribute_datas,
                                   qs_value=qs_value,
                                   qs_index=qs_index)

        # ------------------------
        # Define Number & Name of attribute
        # ------------------------

        widget.ui.num_attrib.setText(attribute_datas.get(code_attr_number, ""))
        widget.ui.name_attrib.setText(attribute_datas.get(code_attr_name, ""))

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.combo_loading()

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.lineEdit().installEventFilter(self)
        widget.ui.value_attrib.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setData(user_data_number, widget.ui.num_attrib.text())

        listwidgetitem.setSizeHint(widget.sizeHint())

        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def ajouter_checkbox(self, qs_val: QStandardItem, attribute_datas: dict):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_checkbox)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeCheckbox(qs_value=qs_val, attribute_datas=attribute_datas)

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.checkbox_loading()

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        # Création listwidgetitem
        # ---------------

        listwidgetitem.setData(user_data_number, widget.ui.num_attrib.text())

        listwidgetitem.setSizeHint(widget.sizeHint())

        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_date(self, qs_value: QStandardItem, attribute_datas: dict):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_date)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = AttributeDate(qs_value=qs_value, language=self.asc.langue, attribute_datas=attribute_datas)

        # ------------------------
        # Widget Loading
        # ------------------------

        widget.date_loading()

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.calendar_bt.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setData(user_data_number, widget.ui.num_attrib.text())

        listwidgetitem.setSizeHint(widget.sizeHint())

        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_surface(self, qs_val: QStandardItem, attribute_datas: dict):

        # ------------------------
        # Creation listwidgetitem
        # ------------------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_texture)

        # ------------------------
        # Creation widget
        # ------------------------

        widget = Attribute335(asc=self.asc, qs_value=qs_val, attribute_datas=attribute_datas)

        # ------------------------
        # Creation signals
        # ------------------------

        widget.ui.value_attrib.installEventFilter(self)
        widget.ui.browser_bt.installEventFilter(self)
        widget.ui.preview_bt.installEventFilter(self)

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        # ------------------------
        # Add listwidgetitem
        # ------------------------

        listwidgetitem.setData(user_data_number, widget.ui.num_attrib.text())

        listwidgetitem.setSizeHint(widget.sizeHint())

        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        # ------------------------

    def add_layer(self, qs_val: QStandardItem, datas_index_row: dict):

        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_layer)

        # Création widget
        # ---------------

        widget = AttributeLayer(self.asc)

        widget.ui.value_141.lineEdit().installEventFilter(self)
        widget.ui.value_346.lineEdit().installEventFilter(self)
        widget.ui.value_345.lineEdit().installEventFilter(self)
        widget.ui.value_347.lineEdit().installEventFilter(self)

        widget.ui.value_349_stroke.installEventFilter(self)
        widget.ui.value_349_pen.installEventFilter(self)
        widget.ui.value_349_color.installEventFilter(self)

        widget.ui.lock_141.installEventFilter(self)

        # Création mapper - Layer
        # ---------------

        numero = "141"

        if numero in datas_index_row:
            widget.qs_141_ind = qs_val.child(datas_index_row[numero], col_cat_index)
            widget.qs_141_val = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.name_141.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.name_141.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - style de ligne
        # ---------------

        numero = "349"

        if numero in datas_index_row:
            widget.qs_349 = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.name_349.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.name_349.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - épaisseur
        # ---------------

        numero = "346"

        if numero in datas_index_row:
            widget.qs_346_ind = qs_val.child(datas_index_row[numero], col_cat_index)
            widget.qs_346_val = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.name_346.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.name_346.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - trait
        # ---------------

        numero = "345"

        if numero in datas_index_row:
            widget.qs_345_ind = qs_val.child(datas_index_row[numero], col_cat_index)
            widget.qs_345_val = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.name_345.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.name_345.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - couleur
        # ---------------

        numero = "347"

        if numero in datas_index_row:
            widget.qs_347_ind = qs_val.child(datas_index_row[numero], col_cat_index)
            widget.qs_347_val = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.name_347.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.name_347.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # chargement
        # ---------------

        widget.chargement(row_index=self.liste_details.count())

        # Définition signal
        # ---------------

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        # Création listwidgetitem
        # ---------------

        listwidgetitem.setData(user_data_number, "141")
        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        widget.listwidgetitem = listwidgetitem

    def add_filling(self, qs_val: QStandardItem, datas_index_row: dict):

        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_fill)

        # Création widget
        # ---------------

        widget = AttributeFilling(self.asc)

        widget.ui.hachurage.lineEdit().installEventFilter(self)
        widget.ui.motif.lineEdit().installEventFilter(self)
        widget.ui.couleur.lineEdit().installEventFilter(self)
        widget.ui.surface.installEventFilter(self)
        widget.ui.style.lineEdit().installEventFilter(self)

        widget.ui.chb_hachurage.installEventFilter(self)
        widget.ui.chb_motif.installEventFilter(self)
        widget.ui.chb_style.installEventFilter(self)
        widget.ui.chb_couleur.installEventFilter(self)
        widget.ui.chb_surface.installEventFilter(self)

        widget.ui.browser_bt.installEventFilter(self)
        widget.ui.preview_bt.installEventFilter(self)

        # Création mapper - 118
        # ---------------

        numero = "118"

        if numero in datas_index_row:
            widget.qs_118 = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.titre_infos.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_infos.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - 111
        # ---------------

        numero = "111"

        if numero in datas_index_row:
            widget.qs_111_val = qs_val.child(datas_index_row[numero], col_cat_value)
            widget.qs_111_ind = qs_val.child(datas_index_row[numero], col_cat_index)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.titre_hachurage.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_hachurage.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

                    widget.ui.titre_motif.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_motif.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

                    widget.ui.titre_style.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_style.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - 252
        # ---------------
        numero = "252"

        if numero in datas_index_row:
            widget.qs_252_ind = qs_val.child(datas_index_row[numero], col_cat_index)
            widget.qs_252_val = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.titre_couleur_2.setText(attribute_datas.get(code_attr_name, ""))
                    widget.titre_couleur_2.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - 336
        # ---------------
        numero = "336"

        if numero in datas_index_row:
            widget.qs_336 = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.titre_surface.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_surface.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # chargement
        # ---------------
        widget.chargement(row_index=self.liste_details.count())

        # Définition signal
        # ---------------

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        # Création listwidgetitem
        # ---------------

        listwidgetitem.setData(user_data_number, attribute_val_default_fill_first)

        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

        widget.listwidgetitem = listwidgetitem

    def add_room(self, qs_val: QStandardItem, datas_index_row: dict):

        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)
        listwidgetitem.setData(user_data_type, type_room)

        # Création widget
        # ---------------

        widget = AttributeRoom(self.asc)

        widget.ui.valeur_fav.lineEdit().installEventFilter(self)
        widget.ui.valeur_231.lineEdit().installEventFilter(self)
        widget.ui.valeur_235.lineEdit().installEventFilter(self)
        widget.ui.valeur_232.lineEdit().installEventFilter(self)
        widget.ui.valeur_266.installEventFilter(self)
        widget.ui.valeur_233.lineEdit().installEventFilter(self)
        widget.ui.valeur_264.installEventFilter(self)

        widget.ui.formatting_bt.installEventFilter(self)
        widget.ui.formatting_2_bt.installEventFilter(self)
        widget.ui.bt_231.installEventFilter(self)
        widget.ui.bt_235.installEventFilter(self)
        widget.ui.bt_232.installEventFilter(self)
        widget.ui.bt_233.installEventFilter(self)

        # Création mapper - Pourtour de salle
        # ---------------

        numero = "231"

        if numero in datas_index_row:
            widget.qs_231_ind = qs_val.child(datas_index_row[numero], col_cat_index)
            widget.qs_231_val = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.titre_231.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_231.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - type d'utilisation
        # ---------------

        numero = "235"

        if numero in datas_index_row:
            widget.qs_235_ind = qs_val.child(datas_index_row[numero], col_cat_index)
            widget.qs_235_val = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.titre_235.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_235.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

            widget.qstandarditem_349 = qs_val.child(datas_index_row[numero], col_cat_value)

        # Création mapper - Type de surface
        # ---------------

        numero = "232"

        if numero in datas_index_row:
            widget.qs_232_ind = qs_val.child(datas_index_row[numero], col_cat_index)
            widget.qs_232_val = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.titre_232.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_232.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - facteur_din
        # ---------------

        numero = "266"

        if numero in datas_index_row:
            widget.qs_266 = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.titre_266.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_266.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - Type surface habitable
        # ---------------

        numero = "233"

        if numero in datas_index_row:
            widget.qs_233_ind = qs_val.child(datas_index_row[numero], col_cat_index)
            widget.qs_233_val = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.titre_233.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_233.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Création mapper - facteur_surface_hab
        # ---------------

        numero = "264"

        if numero in datas_index_row:
            widget.qs_264 = qs_val.child(datas_index_row[numero], col_cat_value)

            if numero in self.allplan.attributes_dict:

                attribute_datas = self.allplan.attributes_dict.get(numero, dict)

                if isinstance(attribute_datas, dict):
                    widget.ui.titre_264.setText(attribute_datas.get(code_attr_name, ""))
                    widget.ui.titre_264.setToolTip(attribute_datas.get(code_attr_tooltips, ""))

        # Définition variable
        # ---------------

        widget.chargement()

        # Définition signal
        # ---------------

        widget.attribute_changed_signal.connect(self.catalog.undo_modify_attribute)

        # Création listwidgetitem
        # ---------------

        listwidgetitem.setData(user_data_number, "231")
        listwidgetitem.setSizeHint(widget.sizeHint())

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

    def add_title(self, title: str):

        # Création listwidgetitem
        # ---------------

        listwidgetitem = QListWidgetItem(self.liste_details)

        listwidgetitem.setFlags(listwidgetitem.flags() & ~Qt.ItemIsSelectable)

        widget = AttributeTitle(self.asc, title=title)

        # ---------------------

        widget.ui.attribute_add_bt.clicked.connect(self.asc.action_bar.attributs_ajouter)
        widget.ui.attribute_add_bt.customContextMenuRequested.connect(self.asc.action_bar.attributs_ajouter)

        widget.ui.order_19.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=0,
                                                                 attributes_order_col=0,
                                                                 attributes_order_custom=False))

        widget.ui.order_91.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=1,
                                                                 attributes_order_col=0,
                                                                 attributes_order_custom=False))

        widget.ui.order_az.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=0,
                                                                 attributes_order_col=1,
                                                                 attributes_order_custom=False))

        widget.ui.order_za.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=1,
                                                                 attributes_order_col=1,
                                                                 attributes_order_custom=False))

        widget.ui.order_custom.clicked.connect(
            lambda: self.asc.action_bar.attributes_order_changed(attributes_order=0,
                                                                 attributes_order_col=0,
                                                                 attributes_order_custom=True))

        widget.ui.order_setting.clicked.connect(self.asc.action_bar.attributes_order_custom_clicked)

        listwidgetitem.setSizeHint(widget.sizeHint())

        listwidgetitem.setSizeHint(QSize(widget.width(), 40))

        self.liste_details.addItem(listwidgetitem)
        self.liste_details.setItemWidget(listwidgetitem, widget)

    @staticmethod
    def a___________________event______():
        pass

    def eventFilter(self, obj: QWidget, event: QEvent):

        if event.type() != event.MouseButtonPress:
            return super().eventFilter(obj, event)

        if not isinstance(obj, QWidget):
            self.asc.attribut_clic()
            return super().eventFilter(obj, event)

        parent_actuel = obj.parent()

        if parent_actuel is None:
            self.asc.attribut_clic()
            return super().eventFilter(obj, event)

        if isinstance(parent_actuel, QComboBox) or isinstance(parent_actuel, QPlainTextEdit):

            parent_actuel = parent_actuel.parent()

            if parent_actuel is None:
                self.asc.attribut_clic()
                return super().eventFilter(obj, event)

        nb_details = self.liste_details.count()

        if nb_details < 2:
            self.asc.attribut_clic()
            return super().eventFilter(obj, event)

        for index_row in range(1, nb_details):

            qm = self.liste_details.model().index(index_row, 0)

            if qm_check(qm):
                self.asc.attribut_clic()
                return super().eventFilter(obj, event)

            obj_actuel = self.liste_details.indexWidget(self.liste_details.model().index(index_row, 0))

            if obj_actuel != parent_actuel:
                continue

            self.liste_details.setCurrentRow(index_row)

            self.asc.attribut_clic()

            break

        self.asc.attribut_clic()

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass
