#!/usr/bin/python3
# -*- coding: utf-8 -*

from main_datas import *


# ====================================================== GENERAL ===============


class MyQstandardItem(QStandardItem):

    def __init__(self):
        super().__init__()

        pass

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self):
        pass

    @staticmethod
    def clone_children(qs_original: QStandardItem, qs_destination: QStandardItem):

        if not isinstance(qs_original, MyQstandardItem):
            return

        children_list = qs_original.get_children_qs(children=True, attributes=True)

        for row_list in children_list:

            row_list: list
            cloned_list = list()

            for column_qs in row_list:

                qs_cloned = column_qs.clone_creation()

                if column_qs.column() == col_cat_value:

                    if column_qs.hasChildren():
                        column_qs.clone_children(column_qs, qs_cloned)

                cloned_list.append(qs_cloned)

            qs_destination.appendRow(cloned_list)

    @staticmethod
    def clone_attributes(qs_orignal: QStandardItem, qs_destination: QStandardItem):

        if not isinstance(qs_orignal, MyQstandardItem):
            return

        children_list = qs_orignal.get_children_qs(children=False, attributes=True)

        attributes_list = [attribute_default_base]

        for row_list in children_list:

            row_list: list
            cloned_list = list()

            qs_number: QStandardItem = row_list[col_cat_number]

            if not isinstance(qs_number, Attribute):
                break

            number_current = qs_number.text()

            if number_current in attributes_list:
                continue

            attributes_list.append(number_current)

            for qs_column in row_list:
                qs_cloned = qs_column.clone_creation()

                cloned_list.append(qs_cloned)

            qs_destination.appendRow(cloned_list)

    @staticmethod
    def a___________________attributes_search______():
        pass

    def get_attribute_numbers_list(self) -> list:

        attributes_list = list()

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, Attribute):
                return attributes_list

            qs_number = self.child(index_row, col_cat_number)

            if not isinstance(qs_number, Attribute):
                continue

            attributes_list.append(qs_number.text())

        return attributes_list

    def get_attribute_numbers_datas(self) -> dict:

        attributes_dict = dict()

        columns_count = self.columnCount()

        for index_row in range(self.rowCount()):

            qs_number = self.child(index_row, col_cat_number)

            if not isinstance(qs_number, Attribute):
                continue

            number = qs_number.text()

            if not isinstance(number, str):
                continue

            if number in attributes_dict:
                continue

            attributes_dict[number] = [self.child(index_row, column) for column in range(columns_count)]

        return attributes_dict

    def get_attribute_value_by_number(self, number: str):

        value = None

        if number == attribute_default_base:
            return self.text()

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, Attribute):
                return value

            qs_number = self.child(index_row, col_cat_number)

            if not isinstance(qs_number, Attribute):
                return value

            number_value = qs_number.text()

            if number_value != number:
                continue

            return qs_value.text()

    def get_attribute_line_by_number(self, number: str) -> list:

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, Attribute):
                return list()

            qs_number = self.child(index_row, col_cat_number)

            if not isinstance(qs_number, Attribute):
                return list()

            if qs_number.text() != number:
                continue

            qs_list = list()

            for column in range(self.columnCount()):

                qs = self.child(index_row, column)

                if qs is None:
                    return list()

                qs_list.append(qs)

            return qs_list

        return list()

    @staticmethod
    def a___________________children_list______():
        pass

    def get_link_infos(self):

        link_datas = list()

        for index_row in range(self.rowCount()):

            # search component

            qs_value = self.child(index_row, col_cat_value)

            if not isinstance(qs_value, Component):
                continue

            code = qs_value.text()
            description = formula = ""

            # Search attributes infos

            for index_attribute_row in range(qs_value.rowCount()):

                qs_number = qs_value.child(index_attribute_row, col_cat_number)

                if not isinstance(qs_number, Attribute):
                    break

                number_value = qs_number.text()

                if number_value == "207":

                    qs_attribute = qs_value.child(index_attribute_row, col_cat_value)

                    if not isinstance(qs_attribute, Attribute):
                        continue

                    description = qs_attribute.text()
                    continue

                if number_value == "267":

                    qs_attribute = qs_value.child(index_attribute_row, col_cat_value)

                    if not isinstance(qs_attribute, Attribute):
                        continue

                    formula = qs_attribute.text()
                    break

            link_datas.append([code, description, formula])

        return link_datas

    def get_children_type_list(self) -> list:

        children_type_list = list()

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if isinstance(qs_value, Attribute):
                continue

            children_type_list.append(qs_value.data(user_data_type))

        return children_type_list

    def get_children_name(self, upper: bool) -> list:

        name_list = list()

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if isinstance(qs_value, Attribute):
                continue

            value = qs_value.text()

            name_list.append(value.upper() if upper else value)

        return name_list

    def get_children_qs(self, children=True, attributes=True) -> list:

        children_qs_list = list()

        if not children and not attributes:
            return children_qs_list

        for index_row in range(self.rowCount()):

            qs_value = self.child(index_row, col_cat_value)

            if not attributes and isinstance(qs_value, Attribute):
                continue

            if not children and not isinstance(qs_value, Attribute):
                continue

            children_qs_column_list = list()

            for column_index in range(self.columnCount()):

                qs_child = self.child(index_row, column_index)

                if qs_child is None:
                    return list()

                children_qs_column_list.append(qs_child)

            children_qs_list.append(children_qs_column_list)

        return children_qs_list

    def has_link(self):

        children_list = self.get_children_type_list()
        return link_code in children_list

    def has_children(self):

        type_ele = self.data(user_data_type)

        if type_ele == component_code or type_ele == link_code:
            return False

        return len(self.get_children_type_list()) != 0

    @staticmethod
    def a___________________insertion_index______():
        pass

    def get_insertion_index(self):

        if self.rowCount() == 0:
            return 0

        return len(self.get_attribute_numbers_list())

    def get_attribute_insertion_index(self, number: str) -> int:

        if self.rowCount() == 0:
            return 0

        liste_actuelle = self.get_attribute_numbers_list()

        liste_actuelle.append(number)
        liste_actuelle.sort(key=int)

        liste_finale = [numero for numero in liste_attributs_ordre if numero in liste_actuelle]
        liste_finale += [numero for numero in liste_actuelle if numero not in liste_finale]

        index_insertion = liste_finale.index(number)
        return index_insertion

    @staticmethod
    def a___________________update______():
        pass

    @staticmethod
    def update_with(qs_current: QStandardItem, qs_futur: QStandardItem) -> bool:

        text_current = qs_current.text()
        text_futur = qs_futur.text()

        if text_current != text_futur:
            return False

        datas_futur = dict()
        numbers_list = list()

        # ----------
        # get datas of futur qs
        # ----------

        for child_index in range(qs_futur.rowCount()):

            qs_number: MyQstandardItem = qs_futur.child(child_index, col_cat_number)

            if not isinstance(qs_number, Attribute):
                break

            number = qs_number.text()

            if number == "":
                continue

            values_list = list()
            column_count = qs_futur.columnCount()

            for column_index in range(qs_futur.columnCount()):
                qs_tps = qs_futur.child(child_index, column_index)

                if qs_tps is None:
                    break

                values_list.append(qs_tps.text())

            if len(values_list) == column_count:
                datas_futur[number] = values_list
                numbers_list.append(number)

        # ----------
        # Update
        # ----------

        for child_index in range(qs_current.rowCount()):

            qs_number: MyQstandardItem = qs_futur.child(child_index, col_cat_number)

            if not isinstance(qs_number, Attribute):
                break

            number = qs_number.text()

            if number not in datas_futur:
                continue

            for column_index, value_futur in enumerate(datas_futur.get(number, list())):

                qs_tps: MyQstandardItem = qs_current.child(child_index, column_index)

                if not isinstance(qs_tps, Attribute):
                    break

                qs_tps.setText(value_futur)

            numbers_list.remove(number)

        return len(numbers_list) == 0


# ====================================================== FOLDER ===============

class Folder(MyQstandardItem):

    def __init__(self, value: str, tooltips=True, icon_path=""):
        super().__init__()

        self.setData(folder_code, user_data_type)

        # ---------------- Title ----------------

        self.setText(value)

        # ---------------- Icon ----------------

        if icon_path != "":
            self.icon_path = icon_path
            self.setData(get_icon(icon_path), Qt.DecorationRole)

        else:

            self.icon_path = folder_icon
            self.setData(get_icon(folder_icon), Qt.DecorationRole)

            # ---------------- Tooltips ----------------

        if tooltips:
            a = QCoreApplication.translate("MyQstandarditem", "Dossier")
            b = QCoreApplication.translate("MyQstandarditem", "Classement de vos Dossiers ou de vos Ouvrages")
            c = QCoreApplication.translate("MyQstandarditem", "Un dossier peut contenir des dossiers OU des Ouvrages")

            tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                       f"{b}<br><br>"
                       f"<b><u>/!\\</u> {c} <u>/!\\</u></p>")

            self.setData(tooltip, Qt.ToolTipRole)

        # ---------------- Type Element ----------------

        self.setData(folder_code, user_data_type)

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self):
        return Folder(value=self.text(), tooltips=self.toolTip() != "", icon_path=self.icon_path)

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Component / Link
        # ------------------------------

        if ele_type == component_code or ele_type == link_code:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")
        child = QCoreApplication.translate("hierarchie_qs", "Enfant")

        parent = self.parent()

        if parent is None:
            parent = self.model().invisibleRootItem()

        # ------------------------------
        # Folder
        # ------------------------------

        if ele_type == folder_code:

            children_list = self.get_children_type_list()

            if material_code in children_list:
                return {brother: [parent, self.row() + 1]}

            return {brother: [parent, self.row() + 1],
                    child: [self, self.get_insertion_index()]}

        # ------------------------------
        # Material
        # ------------------------------
        children_list = self.get_children_type_list()

        if folder_code in children_list:
            return dict()

        return {child: [self, self.get_insertion_index()]}

    def get_type_possibilities(self):

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")
        child = QCoreApplication.translate("hierarchie_qs", "Enfant")

        children_list = self.get_children_type_list()

        or_txt = QCoreApplication.translate("hierarchie_qs", "ou")

        if folder_code in children_list:
            return {folder_code: f"{brother} {or_txt} {child}"}

        if material_code in children_list:
            return {folder_code: brother, material_code: child}

        return {folder_code: f"{brother} {or_txt} {child}", material_code: child}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()


# ====================================================== MATERIAL ===============


class Material(MyQstandardItem):

    def __init__(self, value: str, used_by_links=0, tooltips=True):
        super().__init__()

        self.setData(material_code, user_data_type)

        # ---------------- Value ----------------

        self.setText(value)

        # ---------------- Icon ----------------

        self.setData(get_icon(material_icon), Qt.DecorationRole)

        # ---------------- Font ----------------

        self.setFont(bold_font)

        # ---------------- Link manage ----------------

        self.used_by_links_count = used_by_links

        # ---------------- Tooltips ----------------

        if used_by_links == 0:
            self.set_material_classic(tooltips=tooltips)
        else:
            self.set_material_link(tooltips=tooltips)

        # ---------------- Type Element ----------------

        self.setData(material_code, user_data_type)

    def set_material_look(self, used_by_links_count=0):

        self.used_by_links_count = used_by_links_count

        if used_by_links_count == 0:
            self.set_material_classic()
        else:
            self.set_material_link()

    def set_material_classic(self, tooltips=True):

        self.setData(QBrush(QColor("#000000")), Qt.ForegroundRole)

        if not tooltips:
            return

        a = QCoreApplication.translate("hierarchie_qs", "Ouvrage")
        b = QCoreApplication.translate("hierarchie_qs", "Correspond à la Désignation/Matériaux dans Allplan")
        c = QCoreApplication.translate("hierarchie_qs", "Un Ouvrage peut contenir des composants ou des liens")

        tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                   f"{b}<br><br>"
                   f"<b><u>/!\\</u> {c} <u>/!\\</u></p>")

        self.setData(tooltip, Qt.ToolTipRole)

    def set_material_link(self, tooltips=True):

        self.setData(QBrush(QColor("#ff8a65")), Qt.ForegroundRole)

        if not tooltips:
            return

        a = QCoreApplication.translate("hierarchie_qs", "Ouvrage")
        b = QCoreApplication.translate("hierarchie_qs", "Correspond à la Désignation/Matériaux dans Allplan")
        c = QCoreApplication.translate("hierarchie_qs", "Un Ouvrage peut contenir UNIQUEMENT des composants")

        d = QCoreApplication.translate("hierarchie_qs", "Cette ouvrage est utilisé")
        e = QCoreApplication.translate("hierarchie_qs", "fois en tant que lien")

        tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                   f"{b}<br><br>"
                   f"<b><u>/!\\</u> {c} <u>/!\\</u><br><br>"
                   f"{d} {self.used_by_links_count} {e}.")

        self.setData(tooltip, Qt.ToolTipRole)

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self):
        return Material(value=self.text(), used_by_links=self.used_by_links_count, tooltips=self.toolTip() != "")

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Folder
        # ------------------------------

        if ele_type == folder_code:
            return dict()

        # ------------------------------

        parent = self.parent()

        if parent is None:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")
        child = QCoreApplication.translate("hierarchie_qs", "Enfant")

        # ------------------------------
        # Material
        # ------------------------------

        if ele_type == material_code:
            return {brother: [parent, self.row() + 1]}

        # ------------------------------
        # Component
        # ------------------------------

        if ele_type == component_code:
            insertion_index = self.get_insertion_index()

            return {child: [self, insertion_index]}

        # ------------------------------
        # Link
        # ------------------------------

        if self.text() in link_list:
            return dict()

        insertion_index = self.get_insertion_index()

        return {brother: [self, insertion_index]}

    def get_type_possibilities(self):

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")
        child = QCoreApplication.translate("hierarchie_qs", "Enfant")

        if self.text() in link_list:
            return {material_code: brother, component_code: child}

        if len(material_list) - len(material_with_link_list) < 2:
            return {material_code: brother, component_code: child}

        return {material_code: brother, component_code: child, link_code: child}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()

    def get_component_by_name(self, component_name):

        for row_index in range(self.rowCount()):

            qs_child = self.child(row_index, col_cat_value)

            if not isinstance(qs_child, Component):
                continue

            component_txt = qs_child.text()

            if not component_txt == component_name:
                continue

            return qs_child

        return None

    def get_link_name(self) -> list:

        link_name_list = list()

        for row_index in range(self.rowCount()):

            qs_child = self.child(row_index, col_cat_value)

            if not isinstance(qs_child, Link):
                continue

            link_text = qs_child.text()

            if not isinstance(link_text, str):
                continue

            if link_text in link_name_list:
                continue

            link_name_list.append(link_text)

        return link_name_list

    # def link_is_possible(self, link_name: str, ):





# ====================================================== COMPONENT ===============

class Component(MyQstandardItem):

    def __init__(self, value: str, tooltips=True):
        super().__init__()

        self.setData(component_code, user_data_type)

        # ---------------- Value ----------------

        self.setText(value)

        # ---------------- Icon ----------------

        self.setData(get_icon(component_icon), Qt.DecorationRole)

        # ---------------- Font ----------------

        self.setFont(italic_font)

        # ---------------- Tooltips ----------------

        if tooltips:
            a = QCoreApplication.translate("hierarchie_qs", "Composant")
            b = QCoreApplication.translate("hierarchie_qs",
                                           "Correspond aux élements calculés s'affichant dans les rapports d'Allplan")

            c = QCoreApplication.translate("hierarchie_qs", "Un Composant ne peut pas contenir d'enfants")

            tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                       f"{b}<br><br>"
                       f"<b><u>/!\\</u> {c} <u>/!\\</u></p>")

            self.setData(tooltip, Qt.ToolTipRole)

        # ---------------- Type Element ----------------

        self.setData(component_code, user_data_type)

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self):
        return Component(value=self.text(), tooltips=self.toolTip() != "")

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Folder / Material
        # ------------------------------

        if ele_type == folder_code or ele_type == material_code:
            return dict()

        # ------------------------------

        parent = self.parent()

        if parent is None:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        # ------------------------------
        # Component
        # ------------------------------
        if ele_type == component_code:
            return {brother: [parent, self.row() + 1]}

        # ------------------------------
        # Link
        # ------------------------------

        txt_parent = parent.text()

        if txt_parent not in link_list:
            return {brother: [parent, self.row() + 1]}

        return {}

    @staticmethod
    def get_type_possibilities():

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        if len(material_list) - len(material_with_link_list) < 2:
            return {component_code: brother}

        return {component_code: brother, link_code: brother}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()


# ====================================================== LINK ===============


class Link(MyQstandardItem):

    def __init__(self, value: str, tooltips=True):
        super().__init__()

        self.setData(link_code, user_data_type)

        # ---------------- Value ----------------

        self.setText(value)

        # ---------------- Icon ----------------

        self.setIcon(get_icon(link_icon))

        # ---------------- Font ----------------

        self.setFont(italic_font)

        # ---------------- Tooltips ----------------

        if tooltips:
            a = QCoreApplication.translate("hierarchie_qs", "Lien")
            b = QCoreApplication.translate("hierarchie_qs", "Raccourci vers les composants d'un autre Ouvrage")

            d = QCoreApplication.translate("hierarchie_qs",
                                           "Évite de dupliquer les mêmes Composants dans plusieurs Ouvrages")

            c = QCoreApplication.translate("hierarchie_qs", "Un Lien ne peut pas contenir d'enfants")

            tooltip = (f"<p style='white-space:pre'><center><b><u>{a}</b></u><br>"
                       f"{b}<br>{d}<br><br>"
                       f"<b><u>/!\\</u> {c} <u>/!\\</u></p>")

            self.setData(tooltip, Qt.ToolTipRole)

        # ---------------- Type Element ----------------

        self.setData(link_code, user_data_type)

    @staticmethod
    def a___________________clone______():
        pass

    def clone_creation(self):
        return Link(value=self.text(), tooltips=self.toolTip() != "")

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Folder / Material
        # ------------------------------

        if ele_type == folder_code or ele_type == material_code:
            return dict()

        # ------------------------------

        parent = self.parent()

        if parent is None:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        # ------------------------------
        # Link
        # ------------------------------
        if ele_type == link_code:
            return {brother: [parent, self.row() + 1]}

        # ------------------------------
        # Component
        # ------------------------------

        if link_list is None:
            return {}

        txt_parent = parent.text()

        if txt_parent not in link_list:
            return {brother: [parent, self.row() + 1]}

        return dict()

    def get_type_possibilities(self):

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        his_parent = self.parent()

        if his_parent is None:
            return dict()

        txt_parent = his_parent.text()

        if txt_parent in link_list:
            return {component_code: brother}

        return {component_code: brother, link_code: brother}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()


# ====================================================== ATTRIBUTE ===============

class Attribute(MyQstandardItem):

    def __init__(self, value: str):
        super().__init__()

        self.setData(attribute_code, user_data_type)

        # ---------------- Value ----------------

        self.setText(value)

    def clone_creation(self, type_ele=""):
        if type_ele == "":
            return Attribute(value=self.text())

        return Attribute(value=self.text())

    @staticmethod
    def a___________________possibility_creation______():
        pass

    def get_add_possibilities(self, ele_type: str) -> dict:

        # ------------------------------
        # Folder / Material
        # ------------------------------

        if ele_type == folder_code or ele_type == material_code:
            return dict()

        # ------------------------------

        parent = self.parent()

        if parent is None:
            return dict()

        # ------------------------------

        brother = QCoreApplication.translate("hierarchie_qs", "Frère")

        # ------------------------------
        # Link
        # ------------------------------
        if ele_type == link_code:
            return {brother: [parent, self.row() + 1]}

        # ------------------------------
        # Component
        # ------------------------------

        if link_list is None:
            return {}

        txt_parent = parent.text()

        if txt_parent not in link_list:
            return {brother: [parent, self.row() + 1]}

        return dict()

    @staticmethod
    def get_type_possibilities():
        return {}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()


# ====================================================== INFO ===============


class Info(MyQstandardItem):

    def __init__(self, value: str, type_ele):
        super().__init__()

        self.setData(type_ele, user_data_type)

        self.type_ele = type_ele

        # ---------------- Value ----------------

        self.setText(value)

    def clone_creation(self, type_ele=""):
        if type_ele == "":
            return Info(value=self.text(), type_ele=self.type_ele)

        return Info(value=self.text(), type_ele=type_ele)

    @staticmethod
    def get_type_possibilities():
        return {}

    def is_possible_to_add(self, ele_type: str) -> bool:
        return ele_type in self.get_type_possibilities()
