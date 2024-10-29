#!/usr/bin/python3
# -*- coding: utf-8 -*

import os.path
import time
from datetime import datetime
from typing import Tuple

from attribute_layer import AttributeLayer
from room_attribute import AttributeRoom
from attribute_filling import AttributeFilling
from allplan_manage import *
from attribute_code import AttributeCode
from attribute_name import AttributeName
from convert_manage import ConvertAllmetre, ConvertBcmOuvrages, ConvertKukat, ConvertNevarisXml
from hierarchy_qs import *
from history_manage import *
from message import *
from tools import afficher_message as msg
from tools import get_catalog_setting_display_file, catalog_xml_region, read_catalog_paths_file, catalog_xml_date
from tools import get_catalog_setting_folder, get_catalog_setting_path_file, find_new_title, settings_list
from tools import make_backup, settings_save_value, settings_get, find_folder_path
from tools import recherche_chemin_bcm, find_filename, write_catalog_paths_file, move_window_tool, qm_check
from tools import catalog_xml_find_all
from ui_main_windows import Ui_MainWindow


class ClipboardDatas:

    def __init__(self, type_element):
        super().__init__()

        self.type_element = type_element
        self.datas = []

    def append(self, key: str, value: list) -> None:

        if key != "":
            self.datas.append({"key": key, "value": value, "id": f"{id(key)}"})

    def keys(self) -> list:

        liste_keys = [item["key"] for item in self.datas]
        return liste_keys

    def get_titles_list(self, upper=False) -> list:

        titles_list = list()

        for item in self.datas:

            if not isinstance(item, dict):
                continue

            qs_list = item.get("value")

            if not isinstance(qs_list, list):
                continue

            qs = qs_list[0]

            if not isinstance(qs, QStandardItem):
                continue

            title_current = qs.text()

            if upper:
                title_current = title_current.upper()

            titles_list.append(title_current)

        return titles_list

    def get_values_list(self) -> list:

        values_list = [item["value"] for item in self.datas]

        return values_list

    def clear(self) -> None:

        self.datas.clear()

    def check_title_exist(self, title: str) -> bool:

        title_list = self.keys()

        return title in title_list

    def get_datas_title(self, title: str, id_ele="0") -> list:

        for datas_current in self.datas:

            datas_current: dict

            title_current = datas_current["key"]

            if title == title_current:

                if id_ele == "0":
                    return [datas_current["value"]]

                id_current = datas_current["id"]

                if id_current == id_ele:
                    return [datas_current["value"]]

        return list()

    def get_real_title(self, title: str, ele_id="0") -> str:

        for datas_current in self.datas:

            datas_current: dict

            title_current = datas_current["key"]

            if title == title_current:

                if ele_id == "0":

                    datas: list = datas_current.get("value", list())

                    if len(datas) == 0:
                        return title

                    qs: QStandardItem = datas[0]

                    if not isinstance(qs, QStandardItem):
                        return title

                    return qs.text()

                id_current = datas_current["id"]

                if id_current == ele_id:

                    datas: list = datas_current.get("value", list())

                    if len(datas) == 0:
                        return title

                    qs: QStandardItem = datas[0]

                    if not isinstance(qs, QStandardItem):
                        return title

                    return qs.text()

        return title

    def len_datas(self) -> int:
        return len(self.datas)

    def get_cut_datas(self, title: str) -> tuple:

        datas_full: list = self.get_datas_title(title)

        if len(datas_full) == 0:
            return None, None

        datas = datas_full[0]

        if len(datas) < 2:
            return None, None

        qs_parent: QStandardItem = datas[0]

        if qs_parent is None:
            return None, None

        qs_current: MyQstandardItem = datas[1]

        if qs_current is None:
            return None, None

        row_index: int = qs_current.row()

        return qs_parent, row_index


class CatalogDatas(QObject):
    formula_color_change_signal = pyqtSignal()
    formula_size_change_signal = pyqtSignal(int)
    close_library_signal = pyqtSignal()

    def __init__(self, asc):
        super().__init__()

        self.asc = asc
        self.allplan: AllplanDatas = self.asc.allplan
        self.ui: Ui_MainWindow = self.asc.ui

        self.loading: LoadingSplash = self.asc.loading

        self.catalog_path = ""

        self.catalog_region = ""

        self.catalog_folder = ""
        self.catalog_name = ""
        self.catalog_settings_folder = ""
        self.catalog_setting_path_file = ""
        self.catalog_setting_display_file = ""

        self.cat_model = QStandardItemModel()

        self.change_made = False
        self.undo_list = ActionsData()
        self.redo_list = ActionsData()
        self.library_synchro_list = list()

        self.description_show = settings_get(file_name=app_setting_file, info_name="description_show")

        if self.description_show is None:
            self.description_show = True

        self.expanded_list = list()
        self.selected_list = list()

        self.error_current_qs = None

        # ---------------------------------------
        # FILTER TYPE
        # ---------------------------------------

        self.cat_filter = SpecialFilterProxyModel()
        self.cat_filter.setRecursiveFilteringEnabled(True)
        self.cat_filter.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.cat_filter.setSortLocaleAware(True)
        self.cat_filter.setSourceModel(self.cat_model)

        self.cat_filter_2 = QSortFilterProxyModel()
        self.cat_filter_2.setRecursiveFilteringEnabled(True)
        self.cat_filter_2.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.cat_filter_2.setFilterKeyColumn(col_cat_value)
        self.cat_filter_2.setFilterRole(user_data_type)
        self.cat_filter_2.setSortLocaleAware(True)
        self.cat_filter_2.setSourceModel(self.cat_filter)

        self.ui.hierarchy.setModel(self.cat_filter_2)

        self.bcm_path = recherche_chemin_bcm()
        self.allmetre_path = settings_get(library_setting_file, "path_alltop")

        # ---------------------------------------
        # Loading Clipboard
        # ---------------------------------------

        self.clipboard_folder = ClipboardDatas(folder_code)
        self.clipboard_folder_cut = ClipboardDatas(folder_code)

        self.clipboard_material = ClipboardDatas(material_code)
        self.clipboard_material_cut = ClipboardDatas(material_code)

        self.clipboard_component = ClipboardDatas(component_code)
        self.clipboard_component_cut = ClipboardDatas(component_code)

        self.clipboard_link = ClipboardDatas(link_code)
        self.clipboard_link_cut = ClipboardDatas(link_code)

        self.clipboard_attribute = ClipboardDatas(attribute_code)
        self.clipboard_attribute_cut = ClipboardDatas(attribute_code)

        self.clipboard_current = ""

    @staticmethod
    def a___________________catalog_creation___________________():
        pass

    def catalog_create_new(self, catalog_folder: str, catalog_name, user_folder: str, version_allplan: str) -> bool:

        # ------------------------------
        # Catalog path
        # ------------------------------

        catalog_path = f"{catalog_folder}{catalog_name}.xml"

        # ------------------------------
        # display path
        # ------------------------------

        if not self.catalog_create_path_file(catalog_folder=catalog_folder,
                                             catalog_name=catalog_name,
                                             user_data_path=user_folder,
                                             allplan_version=version_allplan):
            return False

        # ------------------------------
        # display creation
        # ------------------------------

        catalog_settings_folder = get_catalog_setting_folder(catalog_folder=catalog_folder)

        if not catalog_settings_folder:
            print("catalog_manage -- catalog_create_new -- not catalog_settings_folder")
            return False

        catalog_setting_display_file = get_catalog_setting_display_file(catalog_settings_folder=catalog_settings_folder,
                                                                        catalog_name=catalog_name)

        if not catalog_setting_display_file:
            print("catalog_manage -- catalog_create_new -- not catalog_setting_display_file")
            return False

        return self.catalog_create_new_action(version_allplan="1.0",
                                              catalog_path=catalog_path,
                                              catalog_setting_display_file=catalog_setting_display_file)

    def catalog_create_new_action(self, version_allplan: str, catalog_path: str, catalog_setting_display_file) -> bool:

        region = catalog_xml_region(current_language=self.allplan.langue)

        version_xml = version_allplan
        # version_xml = catalog_xml_version(allplan_version=version_allplan)

        date_modif = catalog_xml_date(current_language=self.allplan.langue)

        a = self.tr("Dernier enregistrement")
        new = self.tr("Nouveau dossier")

        root = etree.Element('AllplanCatalog',
                             Region=region,
                             version=version_xml)

        root.set("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation",
                 "../Xsd/AllplanCatalog.xsd")

        root_expand = etree.Element('Smart-Catalog')

        etree.SubElement(root, 'Node', name=f"------------------- {a} : {date_modif} ------------------- ")
        etree.SubElement(root, 'Node', name=new)

        etree.SubElement(root_expand, 'Node', name=f"------------------- {a} : {date_modif} ------------------- ")
        etree.SubElement(root_expand, 'Node', name=new)

        a = self.tr("Une erreur est survenue.")

        try:
            catalogue = etree.tostring(root,
                                       pretty_print=True,
                                       xml_declaration=True,
                                       encoding='UTF-8').decode()

            sauvegarde_expand = etree.tostring(root_expand,
                                               pretty_print=True,
                                               xml_declaration=True,
                                               encoding='UTF-8').decode()

        except Exception as erreur:
            msg(titre=application_title,
                message=f'{a} : {catalog_path}',
                icone_critique=True,
                details=f"{erreur}")
            return False

        try:

            with open(catalog_path, "w", encoding="utf_8_sig") as file:
                file.write(catalogue)

        except IOError as erreur:

            msg(titre=application_title,
                message=f'{a} : {catalog_path}',
                icone_critique=True,
                details=f"{erreur}")
            return False

        except Exception as erreur:
            msg(titre=application_title,
                message=f'{a} : {catalog_path}',
                icone_critique=True,
                details=f"{erreur}")
            return False

        try:
            with open(catalog_setting_display_file, "w", encoding="utf_8") as file:

                file.write(sauvegarde_expand)

        except OSError as erreur:

            msg(titre=application_title,
                message=f"{a} : {catalog_setting_display_file}",
                icone_avertissement=True,
                details=f"{erreur}")
            return False

        return True

    @staticmethod
    def a___________________catalog_path_file___________________():
        pass

    def catalog_define_paths(self, catalog_path: str) -> bool:

        # -----------------------------
        #         catalog_folder
        # -----------------------------

        catalog_folder = find_folder_path(file_path=catalog_path)

        if not catalog_folder:
            print("catalog_manage -- catalog_define_paths -- not catalog_folder")
            return False

        # -----------------------------
        #         catalog_name
        # -----------------------------

        catalog_name = find_filename(file_path=catalog_path)

        if not catalog_name:
            print("catalog_manage -- catalog_define_paths -- not catalog_name")
            return False

        # -----------------------------
        #    catalog_settings_folder
        # -----------------------------

        catalog_settings_folder = get_catalog_setting_folder(catalog_folder=catalog_folder)

        if not catalog_settings_folder:
            print("catalog_manage -- catalog_define_paths -- not catalog_settings_folder")
            return False

        # -----------------------------
        #    catalog_setting_path_file
        # -----------------------------

        catalog_setting_path_file = get_catalog_setting_path_file(catalog_settings_folder=catalog_settings_folder,
                                                                  catalog_name=catalog_name)

        if not catalog_setting_path_file:
            print("catalog_manage -- catalog_define_paths -- not catalog_setting_path_file")
            return False

        # -----------------------------
        #    catalog_setting_display_file
        # -----------------------------

        catalog_setting_display_file = get_catalog_setting_display_file(catalog_settings_folder=catalog_settings_folder,
                                                                        catalog_name=catalog_name)

        if not catalog_setting_display_file:
            print("catalog_manage -- catalog_define_paths -- not catalog_setting_display_file")
            return False

        # -----------------------------
        #    copy all paths
        # -----------------------------

        self.catalog_path = catalog_path

        self.catalog_folder = catalog_folder
        self.catalog_name = catalog_name

        self.catalog_settings_folder = catalog_settings_folder
        self.catalog_setting_path_file = catalog_setting_path_file
        self.catalog_setting_display_file = catalog_setting_display_file

        return True

    @staticmethod
    def catalog_create_path_file(catalog_folder: str, catalog_name: str,
                                 user_data_path: str, allplan_version: str) -> bool:

        """
        Creation of the catalog setting file : CatalogName_path.ini
        :param catalog_folder: path of catalog's folder
        :param catalog_name: name of catalog
        :param user_data_path: path of user's datas
        :param allplan_version: name of version Allplan
        :return: success (bool)
        """

        # -----------------------------
        # Définie the path of settings
        # -----------------------------

        catalog_settings_folder = get_catalog_setting_folder(catalog_folder=catalog_folder)

        if not catalog_settings_folder:
            print("catalog_manage -- catalog_create_path_file -- not catalog_settings_folder")
            return False

        # -----------------------------
        # Define the path of the file : CatalogName_path.ini
        # -----------------------------

        catalog_setting_path_file = get_catalog_setting_path_file(catalog_settings_folder=catalog_settings_folder,
                                                                  catalog_name=catalog_name)

        if not catalog_setting_path_file:
            print("catalog_manage -- catalog_create_path_file -- not catalog_setting_path_file")
            return False

        # -----------------------------
        # write the file
        # -----------------------------

        if not write_catalog_paths_file(catalog_setting_path_file=catalog_setting_path_file,
                                        datas={"user_data_path": user_data_path,
                                               "allplan_version": allplan_version}):
            print("catalog_manage -- catalog_create_path_file -- not write_catalog_paths_file")
            return False

        return True

    def catalog_load_path_file(self, catalog_setting_path_file) -> bool:
        """
        Load
        :return:
        """

        # -----------------------------
        # find default settings
        # -----------------------------

        version_allplan_default = self.allplan.versions_list[0]

        if version_allplan_default == "99" and len(self.allplan.versions_list) > 1:
            version_allplan_default = self.allplan.versions_list[1]

        for annee in reversed(self.allplan.versions_list):

            if annee in catalog_setting_path_file:
                version_allplan_default = annee
                break

        if version_allplan_default not in self.allplan.version_datas:
            return False

        version_obj = self.allplan.version_datas[version_allplan_default]

        if not isinstance(version_obj, AllplanPaths):
            return False

        folder_std = version_obj.std_path
        folder_prj = version_obj.prj_path

        if folder_std == "" or folder_prj == "":
            print("catalog_manage -- catalog_load_path_file -- folder_std is empty or folder_prj is empty")
            return False

        # -----------------------------
        # load settings
        # -----------------------------

        datas = read_catalog_paths_file(catalog_setting_path_file=catalog_setting_path_file,
                                        folder_std=folder_std,
                                        folder_prj=folder_prj,
                                        allplan_version_default=version_allplan_default,
                                        allplan_version_list=self.allplan.versions_list)

        # -----------------------------
        # Apply settings
        # -----------------------------

        user_data_path = datas.get("user_data_path", folder_std)

        self.allplan.catalog_user_path = user_data_path
        self.allplan.user_attributes_xml_path = self.allplan.search_xml_file(xml_folder_path=f"{user_data_path}Xml\\")

        self.allplan.version_allplan_current = datas.get("allplan_version", version_allplan_default)

        if help_mode:
            self.ui.statusbar.showMessage('Allplan 202X -- C:\\Data\\Allplan\\202X\\STD\\')

        else:

            self.ui.statusbar.showMessage(f'Allplan {self.allplan.version_allplan_current} -- '
                                          f'{self.allplan.catalog_user_path}')

        return True

    @staticmethod
    def a___________________catalog_user_path___________________():
        pass

    def catalog_user_path_check(self, user_path: str):

        version_allplan = self.allplan.version_allplan_current

        if version_allplan not in self.allplan.version_datas:
            return

        version_obj = self.allplan.version_datas[version_allplan]

        if not isinstance(version_obj, AllplanPaths):
            return

        folder_std = version_obj.std_path
        folder_prj = version_obj.prj_path

        if user_path is None:
            print("catalog_manage -- catalog_user_path_check -- user_path is None")
            return self.catalog_user_path_define(user_path=folder_std)

        if user_path == "":
            print("catalog_manage -- catalog_user_path_check -- user_path is empty")
            return self.catalog_user_path_define(user_path=folder_std)

        user_path = user_path.strip()

        if os.path.exists(user_path):
            return self.catalog_user_path_define(user_path=user_path)

        try:
            project_name = os.path.basename(os.path.normpath(user_path))

            # dernier_backslash = chemin_utilisateur.rfind('\\')
            #
            # nom_projet = chemin_utilisateur[dernier_backslash + 1:-1]

            if project_name.endswith(".prj"):

                tmp_path = f"{folder_prj}{project_name}"

                if os.path.exists(tmp_path):
                    return self.catalog_user_path_define(tmp_path)

        except Exception as error:
            print(f"catalog_manage -- catalog_user_path_check -- error : {error}")
            return self.catalog_user_path_define(folder_std)

        return self.catalog_user_path_define(user_path=folder_std)

    def catalog_user_path_define(self, user_path: str):

        folder_changed = self.allplan.catalog_user_path != user_path

        self.allplan.catalog_user_path = user_path
        self.allplan.user_attributes_xml_path = self.allplan.search_xml_file(xml_folder_path=f"{user_path}Xml\\")

        print(f"catalog_manage -- catalog_user_path_define -- catalog_user_path ==> "
              f"{self.allplan.catalog_user_path}")

        print(f"catalog_manage -- catalog_user_path_define -- user_attributes_xml_path ==> "
              f"{self.allplan.user_attributes_xml_path}")

        self.ui.statusbar.showMessage(f'Allplan {self.allplan.version_allplan_current} -- '
                                      f'{self.allplan.catalog_user_path}')

        return folder_changed

    @staticmethod
    def a___________________catalog_loading___________________():
        pass

    def catalog_load_start(self, catalog_path: str, loader="xml", chemin_bdd=""):

        self.close_library_signal.emit()

        # ------------------------
        # Define all paths
        # ------------------------

        self.catalog_define_paths(catalog_path=catalog_path)

        # ------------------------
        # Clear attributes (ui)
        # ------------------------

        self.ui.attributes_detail.clear()

        # ------------------------
        # clear current search (ui)
        # ------------------------

        if self.ui.search_error_bt.isChecked():
            self.ui.search_error_bt.setChecked(False)
            self.ui.search_error_bt.clicked.emit()

        if self.ui.search_line.text() != "":
            self.ui.search_line.setText("")

        print("------------------------------------------------------------")

        # ------------------------
        # Show avertissements message
        # ------------------------

        catalog_name = self.catalog_name.lower()

        if catalog_name == "test":
            a = self.tr("Il est déconseillé d'utiliser 'test' comme nom de catalogue")
            b = self.tr("Allplan ne voudra pas l'afficher")

            msg(titre=application_title,
                message=f"{a}.\n{b}.")

        elif len(catalog_name) > 27:
            a = self.tr("Le nom de catalogue ne doit pas dépassé 27 caractères")
            b = self.tr("actuellement")
            c = self.tr("Allplan ne voudra pas l'afficher")

            msg(titre=application_title,
                message=f"{a} \n"
                        f"({b} : {len(catalog_name)}.\n"
                        f"{c}.")

        # ------------------------
        # Show "Loading"
        # ------------------------

        move_window_tool(widget_parent=self.asc, widget_current=self.loading, always_center=True)

        if loader == "Allmétré" or loader == "BCM" or loader == "KUKAT":

            a = self.tr("Conversion de la base de données")

            self.asc.loading.launch_show(f"{a} : {loader} ...")

        else:

            self.loading.launch_show(self.tr("Chargement en cours ..."))

        # ------------------------
        # Load setting file : CatalogName_path.ini
        # ------------------------

        if not self.catalog_load_path_file(catalog_setting_path_file=self.catalog_setting_path_file):
            print("catalog_manage -- catalog_load_start -- not self.catalog_load_path_file")
            return

        # ------------------------
        # Load datas Allplan
        # ------------------------

        self.allplan.allplan_loading()

        # ------------------------
        # Initialisation of catalog loading
        # ------------------------

        if loader == "Allmétré":
            catalog_loading = ConvertAllmetre(allplan=self.allplan,
                                              file_path=chemin_bdd,
                                              bdd_title=self.catalog_name,
                                              conversion=True)

        elif loader == "BCM":
            catalog_loading = ConvertBcmOuvrages(allplan=self.allplan,
                                                 file_path=chemin_bdd,
                                                 bdd_title=self.catalog_name,
                                                 conversion=True)

        elif loader == "KUKAT":
            catalog_loading = ConvertKukat(allplan=self.allplan,
                                           file_path=chemin_bdd,
                                           bdd_title=self.catalog_name,
                                           conversion=True)

        elif loader == "NEVARIS":
            catalog_loading = ConvertNevarisXml(allplan=self.allplan,
                                                file_path=chemin_bdd,
                                                bdd_title=self.catalog_name,
                                                conversion=True)

        else:

            catalog_loading = CatalogLoad(allplan=self.allplan,
                                          file_path=self.catalog_path,
                                          bdd_title=self.catalog_name)

        print(f"catalog_manage -- catalog_load_start -- starting load catalog : {self.catalog_name}")

        # ------------------------

        material_list.clear()
        catalog_loading.material_list = material_list

        material_upper_list.clear()
        catalog_loading.material_upper_list = material_upper_list

        link_list.clear()
        catalog_loading.link_list = link_list

        material_with_link_list.clear()
        catalog_loading.material_with_link_list = material_with_link_list

        # ------------------------
        # Connecting end signals
        # ------------------------

        catalog_loading.loading_completed.connect(self.catalog_load_end)
        catalog_loading.errors_signal.connect(self.catalog_load_error_msg)

        # ------------------------
        # start
        # ------------------------

        catalog_loading.run()

    def catalog_load_end(self, model_cat: QStandardItemModel, expanded_list: list, selected_list: list):

        self.loading.hide()

        settings_save_value(file_name=app_setting_file, key_name="path_catalog", value=self.catalog_path)

        catalog_opened_list = settings_list(file_name=cat_list_file, ele_add=self.catalog_path)

        self.asc.open_list_manage(catalog_opened_list=catalog_opened_list)

        self.cat_model = model_cat

        self.expanded_list = expanded_list
        self.selected_list = selected_list

        self.cat_filter.setSourceModel(self.cat_model)
        self.cat_filter.setFilterRole(user_data_type)

        # Modification du titre
        self.asc.catalog_load_title()

        # suppression du ctrl+z / ctrl+y
        self.undo_list.clear()
        self.redo_list.clear()
        self.undo_button_manage()
        self.redo_button_manage()

        if not debug:
            self.cat_filter.setFilterRegExp(pattern_filter)

        if len(expanded_list) != 0:
            self.catalog_expand()

        # Définition de l'header de la hiérarchie
        self.catalog_header_manage()

        if len(selected_list) == 0:
            self.change_made = False
            return

        if self.ui.hierarchy.selectionModel() is None:
            self.change_made = False
            print("catalog_manage -- catalog_load_end -- self.ui.hierarchy.selectionModel() is None")
            return

        self.catalog_select_action(selected_list=self.selected_list, scrollto=True)
        self.selected_list = list()

        self.change_made = False

    def catalog_load_error_msg(self, liste_erreurs):
        b = self.tr("Des erreurs ont été détectées lors de la lecture du catalogue")

        msg(titre=application_title,
            message=f"{b} : {self.catalog_name}.xml",
            details=liste_erreurs,
            afficher_details=True,
            icone_avertissement=True)

    @staticmethod
    def a___________________catalogue_save___________________():
        pass

    def catalog_save_ask(self):

        if self.cat_model.rowCount() == 0:
            return True

        print(f"catalog_manage -- demande_enregistrer -- modification_en_cours == {self.change_made}")

        if not self.change_made:
            return True

        result = msg(titre=application_title,
                     message=self.tr("Voulez-vous sauvegarder votre travail?"),
                     type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                     defaut_bouton=QMessageBox.Ok,
                     icone_sauvegarde=True)

        if result == QMessageBox.Ok:

            if self.ui.search_error_bt.isChecked():
                self.ui.search_error_bt.setChecked(False)
                self.ui.search_error_bt.clicked.emit()

            self.catalog_save_action()
            self.change_made = False
            return True

        if result == QMessageBox.No:

            if self.ui.search_error_bt.isChecked():
                self.ui.search_error_bt.setChecked(False)
                self.ui.search_error_bt.clicked.emit()

            self.change_made = False
            return True

        return False

    def catalog_save(self):

        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ControlModifier:
            self.asc.app_save_datas()
        else:
            self.asc.app_save_all()

    def catalog_save_action(self):

        tps_start = time.perf_counter()

        move_window_tool(widget_parent=self.asc, widget_current=self.loading, always_center=True)

        self.loading.launch_show(self.tr("Enregistrement du catalogue ..."))

        CatalogSave(asc=self.asc, catalog=self, allplan=self.allplan)

        self.asc.catalog_load_title()

        self.loading.hide()

        self.change_made = False

        print(f"enregistrement terminé en {time.perf_counter() - tps_start}sec")

    @staticmethod
    def a___________________catalog_modification___________________():
        pass

    def catalog_modif_manage(self):

        if self.change_made:
            return

        # print("catalog_manage -- gestion_modification")
        self.change_made = True

    @staticmethod
    def a___________________clipboard___________________():
        pass

    def clipboard_clear_all(self):

        self.clipboard_folder = ClipboardDatas(folder_code)
        self.clipboard_folder_cut = ClipboardDatas(folder_code)

        self.clipboard_material = ClipboardDatas(material_code)
        self.clipboard_material_cut = ClipboardDatas(material_code)

        self.clipboard_component = ClipboardDatas(component_code)
        self.clipboard_component_cut = ClipboardDatas(component_code)

        self.clipboard_link = ClipboardDatas(link_code)
        self.clipboard_link_cut = ClipboardDatas(link_code)

        self.clipboard_attribute = ClipboardDatas(attribute_code)
        self.clipboard_attribute_cut = ClipboardDatas(attribute_code)

        self.clipboard_current = ""

    def get_clipboard(self, ele_type: str, reset_clipboard=False) -> tuple:

        if ele_type == folder_code:
            if reset_clipboard:
                self.clipboard_folder = ClipboardDatas(folder_code)
                self.clipboard_folder_cut = ClipboardDatas(folder_code)
            return self.clipboard_folder, self.clipboard_folder_cut

        if ele_type == material_code:
            if reset_clipboard:
                self.clipboard_material = ClipboardDatas(material_code)
                self.clipboard_material_cut = ClipboardDatas(material_code)
            return self.clipboard_material, self.clipboard_material_cut

        if ele_type == component_code:
            if reset_clipboard:
                self.clipboard_component = ClipboardDatas(component_code)
                self.clipboard_component_cut = ClipboardDatas(component_code)
            return self.clipboard_component, self.clipboard_component_cut

        if ele_type == link_code:

            if reset_clipboard:
                self.clipboard_link = ClipboardDatas(link_code)
                self.clipboard_link_cut = ClipboardDatas(link_code)
            return self.clipboard_link, self.clipboard_link_cut

        if ele_type == attribute_code:

            if reset_clipboard:
                self.clipboard_attribute = ClipboardDatas(attribute_code)
                self.clipboard_attribute_cut = ClipboardDatas(attribute_code)
            return self.clipboard_attribute, self.clipboard_attribute_cut

        return None, None

    @staticmethod
    def a___________________catalog_header___________________():
        pass

    def catalog_header_manage(self) -> None:

        if not debug and not self.ui.hierarchy.hideColumn(col_cat_index):
            self.ui.hierarchy.setColumnHidden(col_cat_index, True)
            self.ui.hierarchy.setColumnHidden(col_cat_number, True)

        self.ui.hierarchy.setColumnHidden(col_cat_desc, not self.description_show)

        if self.ui.hierarchy.header() is None:
            return

        if self.ui.hierarchy.header().height() != 24:
            self.ui.hierarchy.header().setFixedHeight(24)

        row_count = self.cat_model.rowCount()

        if row_count == 0:
            return

        size_now = self.ui.hierarchy.header().sectionSize(col_cat_value)

        self.ui.hierarchy.header().setSectionResizeMode(col_cat_value, QHeaderView.ResizeToContents)

        size_after = self.ui.hierarchy.header().sectionSize(col_cat_value)

        if size_after < size_now:
            self.ui.hierarchy.header().setSectionResizeMode(col_cat_value, QHeaderView.Interactive)
            self.ui.hierarchy.header().resizeSection(col_cat_value, size_now)
        else:
            self.ui.hierarchy.header().setSectionResizeMode(col_cat_value, QHeaderView.Interactive)

        # print("catalog_manage -- hierarchie_gestion_header -- fin")

    @staticmethod
    def a___________________catalog_expand___________________():
        pass

    def save_all_expand_qs_in_list(self, expanded_list: list) -> None:
        """
        Creation list of All QStandardItem and save it in expanded_list
        :param expanded_list: list where QS will be saved
        :return: 
        """

        self.save_expand_qs_in_list_of(qs_parent=self.cat_model.invisibleRootItem(), expanded_list=expanded_list)

    def save_expand_qs_in_list_of(self, qs_parent: MyQstandardItem, expanded_list: list) -> list:
        """
        Creation list of All QStandardItem of qs_parent and save it in expanded_list
        :param qs_parent: current parent
        :param expanded_list: list where QS will be saved
        :return: None
        """

        for row_index in range(qs_parent.rowCount()):

            qs: MyQstandardItem = qs_parent.child(row_index, col_cat_value)

            if isinstance(qs, Attribute):
                continue

            if not isinstance(qs, Material) and not isinstance(qs, Folder):
                return expanded_list

            qm_filter: QModelIndex = self.map_to_filter(qs.index())

            if qm_filter is None:
                print("catalog_manage -- save_expand_qs_in_list_of -- qm_filter is None")
                continue

            if not self.ui.hierarchy.isExpanded(qm_filter):
                continue

            expanded_list.append(qs)

            if qs.hasChildren():
                self.save_expand_qs_in_list_of(qs_parent=qs, expanded_list=expanded_list)

        return expanded_list

    def catalog_expand(self) -> None:

        if len(self.expanded_list) == 0:
            return

        self.ui.hierarchy.blockSignals(True)

        self.catalog_expand_action(self.expanded_list)

        self.catalog_header_manage()

        self.ui.hierarchy.blockSignals(False)

        self.expanded_list = list()

    def catalog_expand_action(self, expanded_list: list) -> None:

        if len(expanded_list) == 0:
            return

        self.ui.hierarchy.blockSignals(True)

        for item in expanded_list:

            if isinstance(item, MyQstandardItem):
                qmodelindex_model: QModelIndex = item.index()

            elif isinstance(item, QModelIndex):
                qmodelindex_model = item

            else:
                print("catalog_manage -- catalog_expand_action -- bad item")
                continue

            qm_filter: QModelIndex = self.map_to_filter(qmodelindex_model)

            if qm_filter is None:
                print("catalog_manage -- catalog_expand_action -- qm_filter is None")
                continue

            self.ui.hierarchy.setExpanded(qm_filter, True)

        self.ui.hierarchy.blockSignals(False)

    def catalog_expand_all_parents(self, qm: QModelIndex):

        if not isinstance(qm, QModelIndex):
            print("catalog_manage -- catalog_expand_all_parents -- not isinstance(qm, QModelIndex)")
            return

        model = qm.model()

        if model is None:
            print("catalog_manage -- catalog_expand_all_parents -- model is None")
            return

        if model != self.ui.hierarchy.model():
            qm_filter = self.map_to_filter(qm)
        else:
            qm_filter = qm

        qm_parent = qm_filter.parent()

        self.ui.hierarchy.blockSignals(True)

        while True:

            if not qm_check(qm_parent):
                break

            self.ui.hierarchy.setExpanded(qm_parent, True)
            qm_parent = qm_parent.parent()

        self.ui.hierarchy.blockSignals(False)

    @staticmethod
    def a___________________catalog_select___________________():
        pass

    def get_filter_selection_list(self) -> list:

        if self.ui.hierarchy.selectionModel() is None:
            print("catalog_manage -- get_filter_selection_list -- self.ui.hierarchy.selectionModel() is None")
            return list()

        selected_list = self.ui.hierarchy.selectionModel().selectedRows(col_cat_value)

        selected_list.sort()

        return selected_list

    def get_qm_model_selection_list(self, selected_list: list) -> list:

        if self.ui.hierarchy.selectionModel() is None:
            print("catalog_manage -- get_model_selection_list -- self.ui.hierarchy.selectionModel() is None")
            return list()

        selected_list.clear()

        selected_tps_list = self.get_filter_selection_list()

        for qm_filter in selected_tps_list:

            qm_model: QModelIndex = self.map_to_model(qm_filter)

            if qm_model is None:
                print("catalog_manage -- get_model_selection_list -- qm_model is None")
                continue

            selected_list.append(qm_model)

        return selected_list

    def get_qs_selection_list(self) -> list:

        qs_list = list()

        if self.ui.hierarchy.selectionModel() is None:
            print("catalog_manage -- get_qs_selection_list -- self.ui.hierarchy.selectionModel()")
            return qs_list

        selected_list = self.get_filter_selection_list()

        if len(selected_list) == 0:
            return qs_list

        for qm_filter in selected_list:
            qs: MyQstandardItem = self.get_qs_by_qm(qm_filter)

            if qs is None:
                print("catalog_manage -- get_qs_selection_list -- qs is None")
                continue

            qs_list.append(qs)

        return qs_list

    def catalog_select(self) -> None:
        self.catalog_select_action(selected_list=self.selected_list)
        self.selected_list.clear()

    def catalog_select_action(self, selected_list: list, scrollto=True) -> bool:

        if self.ui.hierarchy.selectionModel() is None:
            print("catalog_manage -- catalog_select_action -- selectionModel is None")
            return False

        if len(selected_list) == 0:
            print("catalog_manage -- catalog_select_action -- len(selected_list) == 0")
            return False

        current_list = list()

        qitemselection = QItemSelection()

        for qm_model in selected_list:

            if isinstance(qm_model, MyQstandardItem):
                qm_model = self.cat_model.indexFromItem(qm_model)

            elif not isinstance(qm_model, QModelIndex):
                print("catalog_manage -- catalog_select_action -- not isinstance(qm_model, QModelIndex)")
                continue

            if not qm_check(qm_model):
                print("catalog_manage -- catalog_select_action -- qm_check(qm_model)")
                continue

            if qm_model.data(user_data_type) == attribute_code:
                qm_model = qm_model.parent()

                if not qm_check(qm_model):
                    print("catalog_manage -- catalog_select_action -- qm_check(qm_model)")
                    continue

            qm_filter: QModelIndex = self.map_to_filter(qm_model)

            if qm_filter is None:
                print("catalog_manage -- catalog_select_action -- qm_filtre is None")
                continue

            if qm_filter in current_list:
                print("catalog_manage -- catalog_select_action -- qm_filter in current_list")
                continue

            self.catalog_expand_all_parents(qm_filter)

            # if len(selected_list) == 1:
            #     self.ui.hierarchy.setCurrentIndex(qm_filter)

            if qm_filter is None:
                print("catalog_manage -- catalog_select_action -- qm_filter is None")
                continue

            model = qm_filter.model()

            if model is None:
                print("catalog_manage -- catalog_select_action -- model is None")
                continue

            current_row: int = qm_filter.row()
            current_parent: QModelIndex = qm_filter.parent()

            if current_parent is None:
                print("catalog_manage -- catalog_select_action -- current_parent is None")
                continue

            current_list.append(qm_filter)

            qm_start = model.index(current_row, 0, current_parent)
            qm_end = model.index(current_row, model.columnCount() - 1, current_parent)

            qitemselection.select(qm_start, qm_end)

        if len(current_list) == 0:
            return True

        if scrollto:
            qm_filter = current_list[-1]

            self.ui.hierarchy.scrollTo(qm_filter, QAbstractItemView.PositionAtCenter)
            self.ui.hierarchy.horizontalScrollBar().setValue(0)

        self.ui.hierarchy.clearSelection()

        self.ui.hierarchy.selectionModel().blockSignals(True)

        self.ui.hierarchy.selectionModel().select(qitemselection,
                                                  QItemSelectionModel.Select | QItemSelectionModel.Rows)

        self.ui.hierarchy.selectionModel().blockSignals(False)

        self.ui.hierarchy.selectionModel().selectionChanged.emit(qitemselection, qitemselection)

        return True

    @staticmethod
    def a___________________catalog_search___________________():
        pass

    def get_parent(self, qs: MyQstandardItem) -> MyQstandardItem:

        qs_parent = qs.parent()

        if qs_parent is None:
            return self.cat_model.invisibleRootItem()

        return qs_parent

    def get_qs_by_qm(self, qm: QModelIndex):

        if not qm_check(qm):
            print("catalog_manage -- get_qs_by_qm -- not qm_check(qm)")
            return None

        if qm.model() == self.cat_model:
            return self.cat_model.itemFromIndex(qm)

        qm_model: QModelIndex = self.map_to_model(qm)

        if qm_model is None:
            print("catalog_manage -- get_qs_by_qm -- qm_model is None")
            return None

        qs = self.cat_model.itemFromIndex(qm_model)

        if qs is None:
            print("catalog_manage -- get_qs_by_qm -- qs is None")

        return qs

    def get_current_qs(self):

        selected_list: list = self.get_filter_selection_list()

        if len(selected_list) == 0:
            return None

        qs = self.get_qs_by_qm(selected_list[0])

        if qs is None:
            print("catalog_manage -- get_current_qs -- qs is None")

        return qs

    def get_current_model_qm_in_list(self, selected_list: list):

        if len(selected_list) == 0:
            return None

        qm_filter: QModelIndex = selected_list[0]

        if not qm_check(qm_filter):
            print("catalog_manage -- get_current_model_qm_in_list -- not qm_check(qm_filter)")
            return None

        qm_model: QModelIndex = self.map_to_model(qm_filter)

        if qm_model is None:
            print("catalog_manage -- get_current_model_qm_in_list -- qm_model is None")
            return None

        return qm_model

    def get_root_children_name(self, upper=True):

        names_list = list()

        for row_index in range(self.cat_model.rowCount()):

            qm: QModelIndex = self.cat_model.index(row_index, col_cat_value)

            if not qm_check(qm):
                print("catalog_manage -- get_root_children_name -- not qm_check(qm)")
                continue

            title: str = qm.data()

            if title is None:
                print("catalog_manage -- get_root_children_name -- title is None")
                continue

            if upper:
                names_list.append(title.upper())
            else:
                names_list.append(title)

        return names_list

    def get_root_children_type_list(self) -> list:

        children_type_list = list()

        for index_row in range(self.cat_model.invisibleRootItem().rowCount()):

            qs_value = self.cat_model.invisibleRootItem().child(index_row, col_cat_value)

            if isinstance(qs_value, Attribute):
                continue

            children_type_list.append(qs_value.data(user_data_type))

        return children_type_list

    def search_current_selection_text(self) -> str:

        qm_selection_list = self.get_qm_model_selection_list(list())

        if len(qm_selection_list) != 1:
            return ""

        qm_current: QModelIndex = qm_selection_list[0]

        if not qm_check(qm_current):
            print("catalog_manage -- search_current_selection_text -- not qm_check(qm_current)")
            return ""

        text_current: str = qm_current.data()

        actionbar_widget: QWidget = self.ui.actionbar

        try:
            last_focused_widget = QApplication.focusWidget()

            if last_focused_widget is None:
                return text_current

            if last_focused_widget == actionbar_widget:
                return text_current

            parent_current = last_focused_widget.parent()

            if parent_current is None:
                return text_current

        except Exception as error:
            print(f"catalog_manage -- search_current_selection_text -- error : {error}")
            return text_current

        liste_details: QListWidget = self.ui.attributes_detail

        nb_attributs = liste_details.count()
        liste_valeur_attr = [type_nom, type_code, type_ligne, type_date, type_texture, type_formule, type_combo]

        for index_row in range(nb_attributs):

            listwidgetitem: QListWidgetItem = liste_details.item(index_row)

            type_widget = listwidgetitem.data(user_data_type)

            if type_widget == type_checkbox or type_widget == type_lien:
                continue

            widget = liste_details.itemWidget(listwidgetitem)

            if widget is None:
                print("catalog_manage -- search_current_selection_text -- widget is None")
                continue

            if parent_current != widget:
                continue

            if type_widget in liste_valeur_attr:
                return self.search_selected_text(widget=widget.ui.value_attrib, text_current=text_current)

            if type_widget == type_layer:

                widget: AttributeLayer

                widget_layer: QComboBox = widget.ui.value_141

                if widget_layer != last_focused_widget:
                    return text_current

                return self.search_selected_text(widget=widget_layer, text_current=text_current)

            if type_widget == type_fill:

                widget: AttributeFilling
                widget_style: QComboBox = widget.ui.style

                if widget_style == last_focused_widget:
                    return self.search_selected_text(widget=widget_style, text_current=text_current)

                widget_surface: QLineEdit = widget.ui.surface

                if widget_surface == last_focused_widget:
                    return self.search_selected_text(widget=widget_surface, text_current=text_current)

            if type_widget == type_room:

                widget: AttributeRoom

                widget_valeur: QLineEdit = widget.ui.valeur_fav

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                widget_valeur: QLineEdit = widget.ui.valeur_231

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                widget_valeur: QLineEdit = widget.ui.valeur_235

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                widget_valeur: QLineEdit = widget.ui.valeur_232

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                widget_valeur: QLineEdit = widget.ui.valeur_233

                if widget_valeur == last_focused_widget:
                    return self.search_selected_text(widget=widget_valeur, text_current=text_current)

                return text_current

        return text_current

    @staticmethod
    def search_selected_text(widget: QWidget, text_current: str) -> str:

        if isinstance(widget, QLineEdit):

            text_selected = widget.selectedText()

            if text_selected != "":
                return text_selected

            text_selected = widget.text()

            if text_selected != "":
                return text_selected

            return text_current

        if isinstance(widget, QComboBox):

            text_selected = widget.lineEdit().selectedText()

            if text_selected != "":
                return text_selected

            text_selected = widget.currentText()

            if text_selected != "":
                return text_selected

            return text_current

        if isinstance(widget, QPlainTextEdit):

            text_selected = widget.textCursor().selectedText()

            if text_selected != "":
                return text_selected

            text_selected = widget.toPlainText()

            if text_selected != "":
                return text_selected

            return text_current
        return text_current

    def get_attributes_list(self) -> list:

        search_start = self.cat_model.index(0, col_cat_number)

        search = self.cat_model.match(search_start, user_data_type, attribute_code, -1,
                                      Qt.MatchExactly | Qt.MatchRecursive)

        attributes_list = list()

        if len(search) == 0:
            return attributes_list

        exclude_list = ["83", "207"]

        for qm_number in search:

            if not qm_check(qm_number):
                continue

            number = qm_number.data()

            if not isinstance(number, str):
                continue

            if number in exclude_list:
                continue

            if number in attribute_val_default_layer:
                number = attribute_val_default_layer_first

            elif number in attribute_val_default_fill:
                number = attribute_val_default_fill_first

            elif number in attribute_val_default_room:
                number = attribute_val_default_room_first

            if number in attributes_list:
                continue

            attributes_list.append(number)

        # -----------------------------

        if self.asc.attributes_order_col == 0:

            try:

                attributes_list.sort(key=int, reverse=self.asc.attributes_order == 1)

            except Exception:
                pass

        else:

            attributes_list.sort(reverse=self.asc.attributes_order == 1)

        return attributes_list

    @staticmethod
    def a___________________catalog_map___________________():
        pass

    def map_to_model(self, qm: QModelIndex):

        if not qm_check(qm):
            print("catalog_manage -- map_to_model -- not qm_check(qm)")
            return None

        model = qm.model()

        if model is None:
            print("catalog_manage -- map_to_model -- model is None")
            return None

        if model == self.cat_model:
            return qm

        if model == self.cat_filter:
            qm_model = self.cat_filter.mapToSource(qm)

            if not qm_check(qm_model):
                print("catalog_manage -- map_to_model -- not qm_check(qm_model)")
                return None

            return qm_model

        if model == self.cat_filter_2:

            qm_filter1 = self.cat_filter_2.mapToSource(qm)

            if not qm_check(qm_filter1):
                print("catalog_manage -- map_to_model -- not qm_check(qm_filter1)")
                return None

            qm_model = self.cat_filter.mapToSource(qm_filter1)

            if not qm_check(qm_model):
                print("catalog_manage -- map_to_model -- not qm_check(qm_model)")
                return None

            return qm_model

    def map_to_filter(self, qm: QModelIndex):

        if not qm_check(qm):
            print("catalog_manage -- map_to_filter -- not qm_check(qm)")
            return None

        model = qm.model()

        if model is None:
            print("catalog_manage -- map_to_filter -- model is None")
            return None

        if model == self.cat_filter_2:
            return qm

        if model == self.cat_filter:

            qm_filter2 = self.cat_filter_2.mapFromSource(qm)

            if not qm_check(qm_filter2):
                print("catalog_manage -- map_to_filter -- not qm_check(qm_filter2)")
                return None

            return qm_filter2

        if model == self.cat_model:

            qm_filter1 = self.cat_filter.mapFromSource(qm)

            if not qm_check(qm_filter1):
                print("catalog_manage -- map_to_filter -- not qm_check(qm_filter1)")
                return None

            qm_filter2 = self.cat_filter_2.mapFromSource(qm_filter1)

            if not qm_check(qm_filter2):
                print("catalog_manage -- map_to_filter -- not qm_check(qm_filter2)")
                return None

            return qm_filter2

    @staticmethod
    def a___________________material_manage___________________():
        pass

    def get_qm_filter_by_material_name(self, material_name: str) -> list:

        if not isinstance(material_name, str) or material_name == "":
            return list()

        search_start: QModelIndex = self.cat_model.index(0, 0)

        qm_list: list = self.cat_model.match(search_start,
                                             Qt.DisplayRole,
                                             material_name,
                                             -1,
                                             Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_list) == 0:
            print("catalog_manage -- ouvrage_rechercher_qmodelindex_filtre -- recherche == 0")
            return list()

        qm_filter_list = list()

        for qm_model in qm_list:

            if qm_model.data(user_data_type) != material_code:
                continue

            qm_filter = self.map_to_filter(qm_model)

            if qm_filter is None:
                print("catalog_manage -- ouvrage_rechercher_qmodelindex_filtre -- qmodelindex_filtre is None")
                continue

            qm_filter_list.append(qm_filter)

        return qm_filter_list

    def get_qs_by_material_name(self, material_name: str):

        if not isinstance(material_name, str) or material_name == "":
            return

        search_start: QModelIndex = self.cat_model.index(0, 0)

        qm_list: list = self.cat_model.match(search_start,
                                             Qt.DisplayRole,
                                             material_name,
                                             -1,
                                             Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_list) == 0:
            print("catalog_manage -- ouvrage_rechercher_qmodelindex_filtre -- recherche == 0")
            return

        for qm in qm_list:

            if qm.data(user_data_type) != material_code:
                continue

            qs: MyQstandardItem = self.get_qs_by_qm(qm)

            if qs is None:
                print("catalog_manage -- ouvrage_rechercher_qstandarditem -- qmodelindex_filtre is None")
                continue

            return qs

    def goto_material(self, material_name: str):

        if self.ui.search_bt.isChecked():
            self.ui.search_bt.setChecked(False)
            self.ui.search_bt.clicked.emit()

        elif self.ui.search_error_bt.isChecked():
            self.ui.search_error_bt.setChecked(False)
            self.ui.search_error_bt.clicked.emit()

        search_qm = self.get_qm_filter_by_material_name(material_name)

        if len(search_qm) == 0:
            msg(titre=application_title,
                message=self.tr("L'ouvrage n'a pas été trouvé."),
                icone_avertissement=True)
            return

        qm_filter: QModelIndex = search_qm[0]

        self.catalog_select_action([qm_filter])

    def goto_component(self, material_name: str, component_name: str):

        if self.ui.search_bt.isChecked():
            self.ui.search_bt.setChecked(False)
            self.ui.search_bt.clicked.emit()

        elif self.ui.search_error_bt.isChecked():
            self.ui.search_error_bt.setChecked(False)
            self.ui.search_error_bt.clicked.emit()

        qs_material = self.get_qs_by_material_name(material_name)

        if not isinstance(qs_material, Material):
            msg(titre=application_title,
                message=self.tr("L'ouvrage n'a pas été trouvé."),
                icone_avertissement=True)
            return

        qs_component = qs_material.get_component_by_name(component_name)

        if qs_component is None:
            msg(titre=application_title,
                message=self.tr("Le composant n'a pas été trouvé."),
                icone_avertissement=True)
            return

        qm_filter = self.map_to_filter(qs_component.index())

        if not qm_check(qm_filter):
            msg(titre=application_title,
                message=self.tr("Le composant n'a pas été trouvé."),
                icone_avertissement=True)
            return

        self.catalog_select_action([qm_filter])

    def material_refresh_look(self, material_name: str):

        if not isinstance(material_name, str) or material_name == "":
            return

        search_start: QModelIndex = self.cat_model.index(0, 0)

        qm_list: list = self.cat_model.match(search_start,
                                             Qt.DisplayRole,
                                             material_name,
                                             -1,
                                             Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_list) == 0:
            print("catalog_manage -- ouvrage_rechercher_qmodelindex_filtre -- recherche == 0")
            return

        for qm in qm_list:

            qs: MyQstandardItem = self.get_qs_by_qm(qm)

            if not isinstance(qs, Material):
                continue

            value: str = qs.text()

            link_count = link_list.count(value)

            used_by_links_count = qs.used_by_links_count != 0

            if not used_by_links_count and link_count == 0:
                return

            if link_count == 0:
                qs.set_material_classic()
                return

            qs.set_material_look(used_by_links_count=link_count)
            return

    def material_update_link_number(self, material_name: str):

        link_count = link_list.count(material_name)

        search_start: QModelIndex = self.cat_model.index(0, 0)

        qm_list: list = self.cat_model.match(search_start,
                                             Qt.DisplayRole,
                                             material_name,
                                             -1,
                                             Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_list) == 0:
            return

        for qm in qm_list:
            qm: QModelIndex

            qs: MyQstandardItem = self.get_qs_by_qm(qm)

            if not isinstance(qs, Material):
                continue

            qs.set_material_look(link_count)

    @staticmethod
    def material_code_renamed(code_before: str, code_after: str):

        if not isinstance(code_before, str) or not isinstance(code_after, str):
            return

        if code_before == code_after:
            return

        if code_before in material_list:

            code_index = material_list.index(code_before)

            if code_index < 0:
                print("catalog_manage -- ouvrage_modifier_code_in_listes -- index_code < 0")
                return

            material_list[code_index] = code_after

        code_before = code_before.upper()
        code_after = code_after.upper()

        if code_before in material_with_link_list:

            code_index = material_with_link_list.index(code_before)

            if code_index < 0:
                print("catalog_manage -- ouvrage_modifier_code_in_listes -- index_code < 0")
                return

            material_with_link_list[code_index] = code_after

        if code_before == code_after:
            return

        if code_before in material_upper_list:

            code_index = material_upper_list.index(code_before)

            if code_index < 0:
                print("catalog_manage -- ouvrage_modifier_code_in_listes -- index_code_upper < 0")
                return

            material_upper_list[code_index] = code_after

    def material_add(self, qs: MyQstandardItem):

        if not isinstance(qs, MyQstandardItem):
            return

        if isinstance(qs, Component):
            return

        if isinstance(qs, Link):

            title = qs.text()

            if title in link_list:
                link_list.append(title)

            self.material_update_link_number(material_name=title)

            qs_parent = self.get_parent(qs)

            if qs_parent is None:
                return

            parent_text = qs_parent.text()

            if parent_text is None:
                return

            parent_text = parent_text.upper()

            if parent_text in material_with_link_list:
                material_with_link_list.append(parent_text)

            return

        if isinstance(qs, Folder):

            if not qs.hasChildren():
                return

            children_list = qs.get_children_qs(children=True, attributes=False)

            for qs_columns_list in children_list:
                qs_columns_list: list

                qs_val: MyQstandardItem = qs_columns_list[0]

                self.material_add(qs_val)

            return

        if not isinstance(qs, Material):
            return

        title = qs.text()
        title_upper = title.upper()

        if title_upper in material_upper_list:
            material_upper_list.append(title_upper)

        if title in material_list:
            material_list.append(title)

        link_name_list = qs.get_link_name()

        if len(link_name_list) == 0:
            return

        for link_name in link_name_list:

            if not isinstance(link_name, str):
                continue

            link_list.append(link_name)
            material_with_link_list.append(link_name.upper())

            self.material_update_link_number(material_name=link_name)

    def material_is_deletable(self, qs: MyQstandardItem, delete=True) -> bool:

        if not isinstance(qs, MyQstandardItem):
            return True

        if isinstance(qs, Component):
            return True

        if isinstance(qs, Link):

            title = qs.text()

            qs_parent = self.get_parent(qs)

            if qs_parent is None:
                return True

            parent_text = qs_parent.text()

            if parent_text is None:
                return True

            parent_text = parent_text.upper()

            if not delete:
                return True

            if title in link_list:
                link_list.remove(title)
                self.material_update_link_number(title)

            if parent_text in material_with_link_list:
                material_with_link_list.remove(parent_text)

            return True

        if isinstance(qs, Folder):

            children_list = qs.get_children_qs(children=True, attributes=False)

            if len(children_list) == 0:
                return True

            for qs_columns_list in children_list:
                qs_columns_list: list

                qs_val: MyQstandardItem = qs_columns_list[0]

                if not self.material_is_deletable(qs=qs_val, delete=delete):
                    return False

            return True

        if isinstance(qs, Material):

            material_name = qs.text()

            if material_name in link_list:
                return False

            if delete:

                if material_name in material_list:
                    material_list.remove(material_name)

                if material_name.upper() in material_upper_list:
                    material_upper_list.remove(material_name.upper())

            children_list = qs.get_children_qs(children=True, attributes=False)

            if len(children_list) == 0:
                return True

            for qs_columns_list in children_list:
                qs_columns_list: list

                qs_val: MyQstandardItem = qs_columns_list[0]

                if not self.material_is_deletable(qs=qs_val, delete=delete):
                    return False

            return True

        return True

    def material_to_new_folder(self):

        selection_qs_list = self.get_qs_selection_list()

        if len(selection_qs_list) == 0:
            return

        selection_qs_list.sort()

        expanded_list = list()
        qs_parent_list = list()

        for qs in selection_qs_list:

            if not isinstance(qs, Material):
                continue

            qs_parent = qs.parent()

            if not isinstance(qs_parent, Folder):
                continue

            parent_id = id(qs_parent_list)

            if parent_id in qs_parent_list:
                continue

            title = qs.text()

            if title == "":
                continue

            qs_description = qs_parent.child(qs.row(), col_cat_desc)

            if isinstance(qs_description, Info):
                description = qs_description.text()
            else:
                description = ""

            folder_qs_list = self.allplan.creation.folder_line(value=title, description=description)

            qs_folder_new = folder_qs_list[0]

            if not isinstance(qs_folder_new, Folder):
                continue

            attributes_list = qs_folder_new.get_attribute_numbers_list()
            attributes_count = len(attributes_list)

            parent_child_count = qs_parent.rowCount()

            for row_index in reversed(range(parent_child_count)):

                child_qs_current = qs_parent.child(row_index, 0)

                if not isinstance(child_qs_current, Material):
                    continue

                material_qs_list = qs_parent.takeRow(row_index)

                if len(material_qs_list) != qs_parent.columnCount():
                    continue

                qs_folder_new.insertRow(attributes_count, material_qs_list)

            expanded_list.append(qs_folder_new)
            qs_parent.appendRow(folder_qs_list)

            self.undo_move_materials(qs_parent=qs_parent,
                                     qs_new_list=folder_qs_list)

        self.catalog_expand_action(expanded_list=expanded_list)
        self.catalog_select_action(selected_list=expanded_list, scrollto=True)

    @staticmethod
    def a___________________link_mange___________________():
        pass

    def link_refresh_code(self, link_name_before: str, link_name_after: str):

        search_start: QModelIndex = self.cat_model.index(0, 0)

        qm_model_list: list = self.cat_model.match(search_start,
                                                   Qt.DisplayRole,
                                                   link_name_before,
                                                   -1,
                                                   Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_model_list) == 0:
            return

        for qm in qm_model_list:

            qs: MyQstandardItem = self.get_qs_by_qm(qm)

            if not isinstance(qs, Link):
                continue

            qs.setText(link_name_after)

        if link_name_before not in link_list:
            print(f"catalog_manage -- lien_actualiser_code -- {link_name_before} not in links_list)")
            return

        link_list[:] = [x if x != link_name_before else link_name_after for x in link_list]

    def link_refresh_desc(self, material_name: str, link_name_after: str):

        search_start: QModelIndex = self.cat_model.index(0, 0)

        qm_model_list: list = self.cat_model.match(search_start,
                                                   Qt.DisplayRole,
                                                   material_name,
                                                   -1,
                                                   Qt.MatchExactly | Qt.MatchRecursive)

        if len(qm_model_list) == 0:
            return

        for qm in qm_model_list:

            qs_val: MyQstandardItem = self.get_qs_by_qm(qm)

            if not isinstance(qs_val, Link):
                continue

            qs_parent = qs_val.parent()

            if not isinstance(qs_parent, Material):
                continue

            qs_desc = qs_parent.child(qs_val.row(), col_cat_desc)

            if not isinstance(qs_desc, Info):
                continue

            qs_desc.setText(link_name_after)

    def link_get_structure(self, material_name: str, qs_parent: Material):

        qs_material: MyQstandardItem = self.get_qs_by_material_name(material_name)

        if not isinstance(qs_material, Material):
            return

        qs_children_list = qs_material.get_children_qs(children=True, attributes=False)

        if len(qs_children_list) == 0:
            return

        for qs_list in qs_children_list:

            if not isinstance(qs_list, list):
                print("catalog_manage -- link_get_structure -- not isinstance(qs_list, list)")
                continue

            if len(qs_list) < qs_material.columnCount():
                print("catalog_manage -- link_get_structure -- len(qs_list) < qs_material.columnCount()")
                continue

            qs_value = qs_list[col_cat_value]
            qs_desc = qs_list[col_cat_desc]

            if not isinstance(qs_desc, MyQstandardItem):
                print("catalog_manage -- link_get_structure -- not isinstance(qs_desc, MyQstandardItem)")
                continue

            if isinstance(qs_value, Component):
                qs_parent.appendRow([qs_value.clone_creation(), qs_desc.clone_creation()])
                continue

            if isinstance(qs_value, Link):
                sub_material_name = qs_value.text()

                qs_sub_material = QStandardItem(get_icon(link_icon), sub_material_name)

                self.link_get_structure(sub_material_name, qs_sub_material)

                qs_parent.appendRow([qs_sub_material, qs_desc.clone_creation()])
                continue

            print("catalog_manage -- link_get_structure -- error type element !!!")

    @staticmethod
    def a___________________catalog_delete___________________():
        pass

    def catalog_delete(self):

        qs_selecion_list = self.get_qs_selection_list()
        selection_index = 0
        parent_selection = None

        for qs in reversed(qs_selecion_list):

            qs: MyQstandardItem

            if qs is None:
                print("onglet_hierarchie -- supprimer --> qstandarditem is None")
                return None

            children_list = qs.get_children_name(upper=False)
            children_count = len(children_list)

            if children_count == 1:

                question = msg(titre=application_title,
                               message=self.tr("Voulez-vous vraiment supprimer cet élément?"),
                               infos="hierarchy_delete_item",
                               type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                               defaut_bouton=QMessageBox.Ok,
                               icone_avertissement=True,
                               infos_defaut=QMessageBox.Ok,
                               details=children_list)

            elif children_count > 1:

                question = msg(titre=application_title,
                               message=self.tr("Voulez-vous vraiment supprimer ces éléments?"),
                               infos="hierarchy_delete_item",
                               type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                               defaut_bouton=QMessageBox.Ok,
                               icone_avertissement=True,
                               infos_defaut=QMessageBox.Ok,
                               details=children_list)

            else:
                question = QMessageBox.Ok

            if question == QMessageBox.Cancel:
                return

            if question == QMessageBox.No:
                continue

            qs_parent = self.get_parent(qs)

            if qs_parent is None:
                continue

            current_row = qs.row()

            if not self.material_is_deletable(qs=qs, delete=True):

                if isinstance(qs, Material):

                    msg(titre=application_title,
                        message=self.tr("Vous ne pouvez supprimer cet ouvrage, "
                                        "il est encore utilisé en tant que lien."),
                        icone_critique=True)

                else:

                    msg(titre=application_title,
                        message=self.tr("Vous ne pouvez supprimer ce dossier, "
                                        "des ouvrages sont utilisés en tant que lien."),
                        icone_critique=True)

                continue

            ele_list = qs_parent.takeRow(current_row)

            self.undo_del_ele(qs_parent, qs, current_row, ele_list)

            selection_index = current_row
            parent_selection = qs_parent

        if isinstance(parent_selection, MyQstandardItem):

            children_list = parent_selection.get_children_type_list()
            children_count = len(children_list)

            if children_count == 0:
                selection_item = parent_selection

            elif selection_index > children_count:
                selection_item = parent_selection.child(selection_index - 1, col_cat_value)

            else:
                selection_item = parent_selection.child(selection_index, col_cat_value)

            self.catalog_select_action([selection_item])

        self.change_made = True

        return

    @staticmethod
    def a___________________catalog_copy___________________():
        pass

    def catalog_copy_action(self, cut=False):

        qs_selected_list = self.get_qs_selection_list()

        ele_list = list()

        for qs in qs_selected_list:

            qs: MyQstandardItem

            if qs is None:
                print("onglet_hierarchie -- copier_recherche --> qs is None")
                self.asc.boutons_hierarchie_coller(attribute_code)
                return

            ele_type = qs.data(user_data_type)

            self.clipboard_current = ele_type

            if ele_type not in ele_list:
                ele_list.append(ele_type)
                zero = True
            else:
                zero = False

            clipboard, clipboard_cut = self.get_clipboard(ele_type=ele_type, reset_clipboard=zero)

            if clipboard is None:
                print("onglet_hierarchie -- copier_recherche --> clipboard is None")
                continue

            title = qs.text()
            description = qs.get_attribute_value_by_number(number="207")

            if description is None or description == "":
                text = title
            else:
                text = f"{title} - {description}"

            current_row = qs.row()
            qs_parent = self.get_parent(qs)

            qs_list = self.catalog_copy_search_column(qs_parent, current_row)

            if qs_list is None:
                print("onglet_hierarchie -- copier_recherche --> qs_list is None")
                self.asc.boutons_hierarchie_coller(None)
                return

            clipboard.append(text, qs_list)

            if cut:
                clipboard_cut.append(text, [qs_parent, qs])

            self.asc.boutons_hierarchie_coller(ele_type)

    @staticmethod
    def catalog_copy_search_column(qs_parent: MyQstandardItem, child_index: int):

        qs_list = list()

        column_count = qs_parent.columnCount()

        for column_index in range(column_count):

            qs = qs_parent.child(child_index, column_index)

            if not isinstance(qs, (Folder, Material, Component, Attribute, Link, Info)):
                print("onglet_hierarchie -- copier_colonnes --> qstandarditem is None")
                return None

            qs_clone = qs.clone_creation()

            if column_index == col_cat_value and qs.hasChildren():
                qs.clone_children(qs_original=qs, qs_destination=qs_clone)

            qs_list.append(qs_clone)

        if len(qs_list) != column_count:
            print("onglet_hierarchie -- copier_colonnes --> len(liste_qstandarditem) != columnCount()")
            return None

        return qs_list

    @staticmethod
    def a___________________catalog_paste___________________():
        pass

    def catalog_paste(self, ele_type):
        clipboard, clipboard_cut = self.get_clipboard(ele_type=ele_type, reset_clipboard=False)

        clipboard: ClipboardDatas
        clipboard_cut: ClipboardDatas

        result = self.hierarchie_coller_datas(pressepapier=clipboard, presse_papier_couper=clipboard_cut)

        if not result:
            return

        if clipboard_cut.len_datas() == 0:
            return

        self.hierarchie_couper_coller_action(clipboard_cut)

    def hierarchie_couper_coller_action(self, presse_papier_couper: ClipboardDatas):

        liste_elements = presse_papier_couper.get_values_list()

        for liste_datas in liste_elements:
            liste_datas: list

            # liste_datas = [qstandarditem_parent, qstandarditem]

            qstandarditem_parent: MyQstandardItem = liste_datas[0]
            datas: MyQstandardItem = liste_datas[1]

            if not isinstance(qstandarditem_parent, QStandardItem):
                continue

            if isinstance(datas, MyQstandardItem):

                index_row: int = datas.row()

                qstandarditem_sup = qstandarditem_parent.child(index_row, col_cat_value)

                if qstandarditem_sup != datas:
                    continue

                qstandarditem_parent.takeRow(index_row)

            elif isinstance(datas, list):

                for qs in datas:

                    index_row: int = qs.row()

                    qstandarditem_sup = qstandarditem_parent.child(index_row, col_cat_value)

                    if qstandarditem_sup != qs:
                        continue

                    qstandarditem_parent.takeRow(index_row)

        # reset cup clipboard !

        presse_papier_couper.clear()
        self.change_made = True

    def hierarchie_coller_datas(self, pressepapier: ClipboardDatas, presse_papier_couper: ClipboardDatas,
                                titre_spe="", id_ele="0") -> bool:

        bible_externe_open = self.asc.library_widget.isVisible()
        couper = presse_papier_couper.len_datas() != 0

        type_element_futur = pressepapier.type_element
        liste_titres_futur = pressepapier.get_titles_list(upper=True)

        if titre_spe == "":
            liste_qs_futur_tous: list = pressepapier.get_values_list()

        else:

            liste_qs_futur_tous: list = pressepapier.get_datas_title(titre_spe, id_ele)

            titre_spe = pressepapier.get_real_title(titre_spe, id_ele)

        if couper:
            liste_copier_enfants = [liste_qstandarditem_pp_row[0]
                                    for liste_qstandarditem_pp_row in liste_qs_futur_tous]

        else:
            liste_copier_enfants: list = self.recherche_enfants(liste_qs_futur_tous=liste_qs_futur_tous)

            if liste_copier_enfants is None:

                if bible_externe_open:
                    self.asc.library_widget.ne_pas_fermer_ui()
                return False

        datas: list = self.recherche_localisation(type_element_futur=type_element_futur,
                                                  liste_titre_futur=liste_titres_futur)

        if len(datas) == 0:

            if bible_externe_open:
                self.asc.library_widget.ne_pas_fermer_ui()
            return False

        for dict_datas in datas:
            for index_liste, liste_qs_futur in enumerate(liste_qs_futur_tous):
                qs_futur: MyQstandardItem = liste_qs_futur[0]
                dict_datas["ajouter_enfants"] = qs_futur in liste_copier_enfants

        datas: list = self.recherche_existant(datas=datas,
                                              titre_spe=titre_spe,
                                              liste_titre_futur=liste_titres_futur)

        if len(datas) == 0:
            if bible_externe_open:
                self.asc.library_widget.ne_pas_fermer_ui()
            return False

        liste_selection_futur = list()

        for dict_datas in datas:
            qs_parent: QStandardItem = dict_datas["qstandarditem_destination"]
            nom: str = dict_datas["nom_parent"]
            index_insertion: int = dict_datas["index_insertion"]
            update: bool = dict_datas["update"]
            remplacer: bool = dict_datas["remplacer"]
            ignorer: bool = dict_datas["ignorer"]

            qs_actuel: QStandardItem = dict_datas["qs_actuel"]
            # nom_actuel: str = dict_datas["nom_actuel"]
            index_actuel = qs_actuel.row()

            if index_actuel == -1 and nom == self.tr("Racine de la hiérarchie"):
                index_actuel = self.cat_model.invisibleRootItem().rowCount()
            elif index_actuel == -1:
                continue

            if remplacer:
                self.material_is_deletable(qs=qs_actuel, delete=True)
                qs_parent.takeRow(qs_actuel.row())

            if ignorer:
                continue

            for index_liste, liste_qs_futur in enumerate(liste_qs_futur_tous):
                index_final = index_insertion + index_liste

                qs_futur: MyQstandardItem = liste_qs_futur[0]
                texte_futur = qs_futur.text()

                ajouter_enfants = qs_futur in liste_copier_enfants

                if update:
                    txt = "Update"
                elif remplacer:
                    txt = "Remplacer"
                else:
                    txt = "Copie"

                print(f"catalog_manage -- hierarchie_coller_datas -- {txt} de : '{texte_futur}' dans '{nom}' "
                      f"à l'index : {index_final} -- avec enfants : {ajouter_enfants}")

                # if remplacer:
                #     index_final = index_actuel
                #     self.supprimer_ouvrage_bdd(qs_actuel)
                #     qs_parent.takeRow(qs_actuel.row())
                #
                # if ignorer:
                #     continue

                self.coller_update(qs_parent=qs_parent,
                                   liste_qs_futur=liste_qs_futur,
                                   index_insertion=index_final,
                                   index_actuel=index_actuel,
                                   ajouter_enfant=ajouter_enfants,
                                   couper=couper,
                                   update=update)

                qm = qs_parent.child(index_final, col_cat_value)

                if not isinstance(qs_futur, Attribute):
                    if qm not in liste_selection_futur:
                        liste_selection_futur.append(qm)

                    continue

                qm = qs_parent.index()

                if qm not in liste_selection_futur:
                    liste_selection_futur.append(qm)

        self.catalog_select_action(liste_selection_futur, len(liste_selection_futur) != 1)
        return True

    def recherche_enfants(self, liste_qs_futur_tous: list):

        dict_futur = dict()

        for index_item, liste_qs_futur_row in enumerate(liste_qs_futur_tous):

            qs_futur: MyQstandardItem = liste_qs_futur_row[0]
            texte_futur = qs_futur.text()

            liste_enfants_futur = qs_futur.get_children_name(upper=False)
            nb_enfants_futur = len(liste_enfants_futur)

            if nb_enfants_futur == 0:
                continue

            dict_futur[texte_futur] = [qs_futur, liste_enfants_futur]

        nb_items_futur = len(dict_futur)

        if nb_items_futur == 0:
            return list()

        msgbox = MessageChildren()

        liste_copie_enfants = list()
        defaut_bouton = "ok"
        reponse_enfants = None

        index_actuel = 0

        checkbox = True

        for texte_futur, donnees in dict_futur.items():

            qs_futur = donnees[0]
            liste_enfants_futur: list = donnees[1]
            nb_enfants_futur = len(liste_enfants_futur)
            index_actuel += 1

            if reponse_enfants is None:

                if nb_enfants_futur == 1:

                    a = self.tr("contient 1 enfant")
                    b = self.tr("Voulez-vous l'ajouter également")

                    msgbox.show_message_children(message=f"<b>'{texte_futur}'</b> {a}. {b} ?",
                                                 bt_ok=self.tr("Avec l'enfant"),
                                                 bt_no=self.tr("Sans l'enfant"),
                                                 chk_all=checkbox,
                                                 checkbox_index=index_actuel,
                                                 checkbox_total=nb_items_futur,
                                                 checkbox_tooltips="\n".join(dict_futur),
                                                 details=liste_enfants_futur,
                                                 default_bouton=defaut_bouton)

                else:

                    a = self.tr("contient des enfants")
                    c = self.tr("Voulez-vous les ajouter également")

                    msgbox.show_message_children(message=f"<b>'{texte_futur}'</b> {a}. {c}?",
                                                 bt_ok=self.tr("Avec les enfants"),
                                                 bt_no=self.tr("Sans les enfants"),
                                                 chk_all=checkbox,
                                                 checkbox_index=index_actuel,
                                                 checkbox_total=nb_items_futur,
                                                 checkbox_tooltips="\n".join(dict_futur),
                                                 details=liste_enfants_futur,
                                                 default_bouton=defaut_bouton)

                reponse_enfants = msgbox.reponse

            if reponse_enfants == QMessageBox.Cancel:
                return None

            if reponse_enfants == QMessageBox.NoAll:
                return list()

            if reponse_enfants == QMessageBox.YesAll:
                liste_copie_enfants.append(qs_futur)
                continue

            if reponse_enfants == QMessageBox.No:
                checkbox = False
                defaut_bouton = "no"
                reponse_enfants = None
                continue

            if reponse_enfants == QMessageBox.Yes:
                liste_copie_enfants.append(qs_futur)
                checkbox = False
                reponse_enfants = None
                defaut_bouton = "ok"
                continue

        return liste_copie_enfants

    def recherche_localisation(self, type_element_futur: str, liste_titre_futur: list) -> list:

        nb_titre_futur = len(liste_titre_futur)

        liste_selection_actuel = self.get_qs_selection_list()
        liste_selection_actuel.sort()
        # liste_parent_actuel = list()

        datas = list()

        if len(liste_selection_actuel) == 0:
            liste_selection_actuel.append(self.cat_model.invisibleRootItem())

        for qs_selection in liste_selection_actuel:

            if not isinstance(qs_selection, (Folder, Material, Component, Link)):
                continue

            index_selection = qs_selection.row()

            if qs_selection == self.cat_model.invisibleRootItem():

                elements_compatibles = {self.tr("Frère"): [qs_selection, self.cat_model.rowCount()]}

            else:

                elements_compatibles = qs_selection.get_add_possibilities(ele_type=type_element_futur)

            nb_elements_compatibles = len(elements_compatibles)

            if nb_elements_compatibles == 0:
                continue

            if nb_elements_compatibles != 1:

                liste_enfant: list = elements_compatibles[self.tr("Enfant")]
                liste_frere: list = elements_compatibles[self.tr("Frère")]

                qs_enfant_actuel: MyQstandardItem = liste_enfant[0]
                enfant_actuel_index = liste_enfant[1]
                enfant_actuel_texte = qs_enfant_actuel.text()
                enfant_actuel_type = qs_enfant_actuel.data(user_data_type)

                qs_parent_actuel: MyQstandardItem = liste_frere[0]
                parent_type_actuel = qs_parent_actuel.data(user_data_type)

                if qs_parent_actuel == self.cat_model.invisibleRootItem():
                    parent_texte_actuel = self.tr("Racine de la hiérarchie")
                else:
                    parent_texte_actuel = qs_parent_actuel.text()

                parent_index_actuel = liste_frere[1]

                msgbox = MessageLocation()

                if nb_titre_futur == 1:

                    msgbox.show_message_location(message=self.tr("Où voulez-vous ajouter cet élément?"),
                                                 parent_txt=parent_texte_actuel,
                                                 parent_type=parent_type_actuel,
                                                 child_txt=enfant_actuel_texte,
                                                 child_type=enfant_actuel_type)

                else:
                    msgbox.show_message_location(message=self.tr("Où voulez-vous ajouter ces éléments?"),
                                                 parent_txt=parent_texte_actuel,
                                                 parent_type=parent_type_actuel,
                                                 child_txt=enfant_actuel_texte,
                                                 child_type=enfant_actuel_type)

                reponse_loc = msgbox.reponse

                if reponse_loc == QMessageBox.Yes:
                    qstandarditem_destination: MyQstandardItem = qs_enfant_actuel
                    index_insertion: int = enfant_actuel_index

                elif reponse_loc == QMessageBox.No:
                    qstandarditem_destination: MyQstandardItem = qs_parent_actuel
                    index_insertion: int = parent_index_actuel

                else:
                    return list()

            else:

                resultat: list = list(elements_compatibles.values())[0]

                qstandarditem_destination: MyQstandardItem = resultat[0]
                index_insertion: int = resultat[1]

            if qstandarditem_destination is None:
                continue

            if qstandarditem_destination == self.cat_model.invisibleRootItem():

                ses_enfants = self.get_root_children_name()

            else:

                ses_enfants = qstandarditem_destination.get_children_name(upper=True)
            #
            # if qstandarditem_destination in liste_parent_actuel:
            #     if type_element_futur == type_element_actuel:
            #         continue
            #
            # liste_parent_actuel.append(qstandarditem_destination)

            if qstandarditem_destination == self.cat_model.invisibleRootItem():
                nom_parent = self.tr("Racine de la hiérarchie")
            else:
                nom_parent = qstandarditem_destination.text()

            datas.append({"qstandarditem_destination": qstandarditem_destination,
                          "nom_parent": nom_parent,
                          "parent_ses_enfants": ses_enfants,
                          "qs_actuel": qs_selection,
                          "nom_actuel": qs_selection.text(),
                          "index_insertion": index_insertion,
                          "index_actuel": index_selection,
                          "update": False,
                          "remplacer": False,
                          "ajouter_enfants": False,
                          "ignorer": False})

        return datas

    def recherche_existant(self, datas: list, titre_spe: str, liste_titre_futur: list) -> list:

        dict_doublons = dict()
        liste_suivants = list()
        liste_parents = list()

        for index_item, datas_dict in enumerate(datas):
            qs_destination: str = datas_dict["qstandarditem_destination"]
            texte_actuel: str = datas_dict["nom_parent"]
            ses_enfants_actuel: list = datas_dict["parent_ses_enfants"]
            ajouter_enfants = datas_dict["ajouter_enfants"]

            if titre_spe == "":

                liste_similaire = [titre for titre in ses_enfants_actuel if titre in liste_titre_futur]

            else:

                if titre_spe.upper() in ses_enfants_actuel:

                    liste_similaire = [titre_spe]
                else:

                    liste_similaire = list()

            if len(liste_similaire) == 0:
                continue

            if qs_destination in liste_parents:
                index_doublons = liste_parents.index(qs_destination)

                liste_doublons_precedent = dict_doublons[index_doublons][1]

                if liste_doublons_precedent == liste_similaire:
                    datas_dict["ignorer"] = True

            else:
                liste_parents.append(qs_destination)

            dict_doublons[index_item] = [texte_actuel, liste_similaire, ajouter_enfants]
            liste_suivants.append(texte_actuel)

        nb_items = len(dict_doublons)

        if nb_items == 0:
            return datas

        msgbox = MessageExisting()

        reponse_exist = None

        checkbox = True
        defaut_bouton = "bt_maj"

        index_actuel = 0

        for index_item, donnees in dict_doublons.items():

            texte_actuel: str = donnees[0]
            liste_similaire: list = donnees[1]
            ajouter_enfants = donnees[2]

            if ajouter_enfants:

                update_txt = self.tr("Mettre à jour et ses enfants")
                replace_txt = self.tr("Remplacer et ses enfants")
                duplicate_txt = self.tr("Dupliquer et ses enfants")

            else:

                update_txt = self.tr("Mettre à jour et ses enfants")
                replace_txt = self.tr("Remplacer et ses enfants")
                duplicate_txt = self.tr("Dupliquer et ses enfants")

            nb_elements_existants = len(liste_similaire)
            index_actuel += 1

            datas_dict: dict = datas[index_item]

            liste_similaire.insert(0, f" --- {texte_actuel} ---\n")

            if reponse_exist is None:

                todo = self.tr("Que souhaitez-vous faire")

                if nb_elements_existants == 1:

                    all_ready_exist = self.tr("existe déjà")

                    msgbox.show_message_existing(message=f"<b>'{liste_similaire[1]}' {all_ready_exist} !</b><br>"
                                                         f'{todo} ? ',
                                                 bt_update=update_txt,
                                                 bt_replace=replace_txt,
                                                 bt_duplicate=duplicate_txt,
                                                 chk_all=checkbox,
                                                 checkbox_index=index_actuel,
                                                 checkbox_total=nb_items,
                                                 checkbox_tooltips="\n".join(liste_suivants),
                                                 details=liste_similaire,
                                                 default_bouton=defaut_bouton)
                else:

                    all_ready_exist = self.tr("éléments existent déjà")

                    msgbox.show_message_existing(message=f"<b>{nb_elements_existants}</b> {all_ready_exist} !\n"
                                                         f'{todo} ? ',
                                                 bt_update=update_txt,
                                                 bt_replace=replace_txt,
                                                 bt_duplicate=duplicate_txt,
                                                 chk_all=checkbox,
                                                 checkbox_index=index_actuel,
                                                 checkbox_total=nb_items,
                                                 checkbox_tooltips="\n".join(liste_suivants),
                                                 details=liste_similaire,
                                                 default_bouton=defaut_bouton)

                reponse_exist = msgbox.reponse

            if reponse_exist == QMessageBox.Cancel:
                return list()

            if reponse_exist == QMessageBox.YesAll:
                datas_dict["update"] = True
                datas_dict["remplacer"] = False
                continue

            if reponse_exist == QMessageBox.SaveAll:
                datas_dict["update"] = False
                datas_dict["remplacer"] = True
                continue

            if reponse_exist == QMessageBox.NoAll:
                return datas

            if reponse_exist == QMessageBox.Yes:
                datas_dict["update"] = True
                datas_dict["remplacer"] = False
                checkbox = False
                reponse_exist = None
                defaut_bouton = "bt_maj"
                continue

            if reponse_exist == QMessageBox.Save:
                datas_dict["update"] = False
                datas_dict["remplacer"] = True
                checkbox = False
                reponse_exist = None
                defaut_bouton = "bt_dupliquer"
                continue

            if reponse_exist == QMessageBox.No:
                checkbox = False
                reponse_exist = None
                defaut_bouton = "bt_remplacer"
                continue

        return datas

    def coller_update(self, qs_parent: MyQstandardItem, liste_qs_futur: list, index_insertion: int, index_actuel: int,
                      ajouter_enfant: bool, couper=False, update=False) -> int:

        qs_futur: MyQstandardItem = liste_qs_futur[0]
        texte_futur = qs_futur.text()

        index_recherche = self.recherche_index_valeur(qs_parent=qs_parent,
                                                      valeur=texte_futur, index_initial=index_actuel)

        attributes_count = 0

        if not update:
            nouveau_qs_parent = self.coller_creation(qs_parent=qs_parent,
                                                     index_insertion=index_insertion,
                                                     liste_qs_futur=liste_qs_futur,
                                                     couper=couper)

            attributes_count = nouveau_qs_parent.rowCount()
            index_tps = index_insertion + attributes_count

        else:

            self.update_with(qs_parent=qs_parent,
                             index_actuel=index_recherche,
                             liste_qs_futur=liste_qs_futur)

            nouveau_qs_parent = qs_parent.child(index_recherche, col_cat_value)

            if nouveau_qs_parent is None:
                print(f"{qs_parent.text(), qs_parent.data(user_data_type)}")

            index_tps = index_recherche

        if not ajouter_enfant:
            return index_tps

        liste_enfants = qs_futur.get_children_qs(children=True, attributes=False)

        for index_insertion, liste_qs_futur in enumerate(liste_enfants):

            if len(liste_qs_futur) == 0:
                return index_tps

            self.coller_update(qs_parent=nouveau_qs_parent,
                               liste_qs_futur=liste_qs_futur,
                               index_insertion=index_insertion + attributes_count,
                               index_actuel=index_insertion,
                               ajouter_enfant=ajouter_enfant,
                               couper=couper,
                               update=update)

        return index_tps

    def coller_creation(self, qs_parent: QStandardItem, index_insertion: int, liste_qs_futur: list,
                        couper: bool) -> QStandardItem:

        print("catalog_manage -- coller_creation")

        liste_cloner = list()

        for qs_futur in liste_qs_futur:

            qs_futur: Material

            qs_clone: Material = qs_futur.clone_creation()

            if not couper:
                self.coller_gestion_nom_ouvrage(qs_clone)

                if isinstance(qs_clone, Folder):

                    if qs_parent == self.cat_model.invisibleRootItem():
                        liste_dossiers = self.get_root_children_name()
                    else:
                        if isinstance(qs_parent, MyQstandardItem):
                            liste_dossiers = qs_parent.get_children_name(upper=True)
                        else:
                            liste_dossiers = list()

                    nouveau_nom = find_new_title(qs_clone.text(), liste_dossiers)

                    qs_clone.setText(nouveau_nom)

            if isinstance(qs_clone, Link):
                nom_ouvrage_lien = qs_clone.text()

                if not couper:
                    link_list.append(nom_ouvrage_lien)

                qs_text = qs_parent.text()

                if not isinstance(qs_text, str):
                    continue

                qs_text = qs_text.upper()

                if qs_text not in material_with_link_list:
                    material_with_link_list.append(qs_text)

                self.material_update_link_number(nom_ouvrage_lien)

            liste_cloner.append(qs_clone)

            if qs_futur.column() == col_cat_value:
                print(f"catalog_manage -- creation -- {qs_futur.text()} ({qs_futur.data(user_data_type)})")

            if qs_futur.hasChildren():
                qs_futur.clone_attributes(qs_orignal=qs_futur, qs_destination=qs_clone)

        qs_parent.insertRow(index_insertion, liste_cloner)

        if couper:

            qs_actuel = liste_cloner[col_cat_value]

            if not isinstance(qs_actuel, MyQstandardItem):
                return liste_cloner[0]

            type_element = qs_actuel.data(user_data_type)
            titre_actuel = qs_actuel.text()

            qs_description = liste_cloner[col_cat_desc]

            if not isinstance(qs_description, Info):
                return liste_cloner[0]

            description = qs_description.text()

            full_title = f"{titre_actuel} - {description}"

            _, presse_papier_couper = self.get_clipboard(ele_type=type_element, reset_clipboard=False)

            presse_papier_couper: ClipboardDatas

            if presse_papier_couper is None:
                return liste_cloner[0]

            qs_parent_actuel, row_actuel = presse_papier_couper.get_cut_datas(full_title)

            if qs_parent_actuel is None:
                return liste_cloner[0]

            self.undo_cut_ele(qs_parent_actuel=qs_parent_actuel, qs_parent_futur=qs_parent,
                              qs_actuel=liste_cloner[col_cat_value],
                              row_actuel=row_actuel, row_futur=index_insertion,
                              liste_ele=liste_cloner)
        else:
            self.undo_add_ele(qs_parent=qs_parent, qs_actuel=liste_cloner[0], index_ele=index_insertion,
                              liste_ele=liste_cloner, coller=True)

        if qs_parent == self.cat_model.invisibleRootItem():
            return liste_cloner[0]

        if not isinstance(qs_parent, Component) and not isinstance(qs_parent, Link):

            qm_filter: QModelIndex = self.map_to_filter(qs_parent.index())

            if qm_filter is not None:
                self.ui.hierarchy.expand(qm_filter)

        print(f"catalog_manage -- creation -- Fin")
        return liste_cloner[0]

    def update_with(self, qs_parent: QStandardItem, index_actuel, liste_qs_futur: list):

        print("catalog_manage -- update_with")

        # --------------------------------------------------------------------------------------
        # Mise à jour de l'élément actuel : colonnes  = valeur, description, index, numero, nom
        # --------------------------------------------------------------------------------------

        nb_colonnes = qs_parent.columnCount()

        if len(liste_qs_futur) != nb_colonnes:
            return False

        qs_actuel = qs_parent.child(index_actuel, col_cat_value)

        if not isinstance(qs_actuel, MyQstandardItem):
            return False

        texte_actuel = qs_actuel.text()
        type_actuel = qs_actuel.data(user_data_type)

        qs_futur = liste_qs_futur[0]

        if not isinstance(qs_futur, MyQstandardItem):
            return False

        texte_futur = qs_futur.text()

        if texte_actuel != texte_futur:
            return False

        print(f"catalog_manage -- update_with -- {qs_futur.text()} ({qs_futur.data(user_data_type)})")

        for numero_col in [col_cat_value, col_cat_desc]:
            qs_tps_actuel = qs_parent.child(index_actuel, numero_col)

            if qs_tps_actuel is None:
                return False

            texte_actuel = qs_parent.text()

            qs_tps_futur: QStandardItem = liste_qs_futur[numero_col]

            if qs_tps_futur is None:
                return False

            if type_actuel == material_code:
                continue

            texte_futur = qs_tps_futur.text()

            if texte_actuel == texte_futur:
                continue

            qs_tps_actuel.setText(texte_futur)

        # --------------------------------------------------------------------------------------
        # Analyse des numéros d'attributs présent dans l'élément actuel
        # --------------------------------------------------------------------------------------

        datas_actuel = dict()
        liste_numeros_actuels = list()

        for index_child_actuel in range(qs_actuel.rowCount()):

            qs_val_actuel: MyQstandardItem = qs_actuel.child(index_child_actuel, col_cat_value)

            if qs_val_actuel is None:
                return False

            if not isinstance(qs_val_actuel, Attribute):
                continue

            liste = list()
            numero_actuel = ""

            for index_colonne in range(nb_colonnes):
                qs_tps = qs_actuel.child(index_child_actuel, index_colonne)

                if qs_tps is None:
                    return False

                if index_colonne == col_cat_number:
                    numero_actuel = qs_tps.text()

                liste.append(qs_tps)

            datas_actuel[numero_actuel] = liste
            liste_numeros_actuels.append(numero_actuel)

        # --------------------------------------------------------------------------------------
        # Copie / Mise à jour des attributs
        # --------------------------------------------------------------------------------------

        for index_child_futur in range(qs_futur.rowCount()):

            qs_val_futur: MyQstandardItem = qs_futur.child(index_child_futur, col_cat_value)

            if qs_val_futur is None:
                return False

            if not isinstance(qs_val_futur, Attribute):
                continue

            qs_numero_futur = qs_futur.child(index_child_futur, col_cat_number)

            if qs_val_futur is None:
                return False

            numero_futur = qs_numero_futur.text()

            # --------------------------------------------------------------------------------------
            # Mise à jour attribut
            # --------------------------------------------------------------------------------------

            if numero_futur in liste_numeros_actuels:

                print(f"catalog_manage -- update_with -- {qs_futur.text()} : MAJ attribut {numero_futur} = "
                      f"{qs_futur.child(index_child_futur, col_cat_value).text()}")

                liste_colonnes_actuelle: list = datas_actuel[numero_futur]

                for index_colonne in [col_cat_value, col_cat_index]:
                    qs_tps_actuel: QStandardItem = liste_colonnes_actuelle[index_colonne]
                    valeur_actuelle = qs_tps_actuel.text()
                    valeur_future = qs_futur.child(index_child_futur, index_colonne).text()

                    if valeur_actuelle == valeur_future:
                        continue

                    qs_tps_actuel.setText(valeur_future)

                continue

            # --------------------------------------------------------------------------------------
            # Copie attribut
            # --------------------------------------------------------------------------------------

            print(f"catalog_manage -- update_with -- {qs_futur.text()} : Création attribut {numero_futur} = "
                  f"{qs_futur.child(index_child_futur, col_cat_value).text()}")

            index_insertion = qs_actuel.get_attribute_insertion_index(number=numero_futur)

            nb_colonnes_futur = qs_futur.columnCount()
            liste_qs_creation = list()

            for index_colonne in range(nb_colonnes_futur):
                liste_qs_creation.append(qs_futur.child(index_child_futur, index_colonne).clone_creation())

            qs_actuel.insertRow(index_insertion, liste_qs_creation)

        if qs_parent == self.cat_model.invisibleRootItem():
            return

        if not isinstance(qs_parent, Component) and not isinstance(qs_parent, Link):

            qmodelindex_filtre: QModelIndex = self.map_to_filter(qs_parent.index())

            if qmodelindex_filtre is not None:
                self.ui.hierarchy.expand(qmodelindex_filtre)

        print("catalog_manage -- update_with -- Fin")
        return True

    def coller_cloner(self, qs_destination: MyQstandardItem, liste_qstandarditem: list, index_insertion: int,
                      ajouter_enfant: bool, couper=False, update=False):

        liste_cloner = list()

        for qstandarditem_creation in liste_qstandarditem:

            qstandarditem_creation: MyQstandardItem

            qs_clone: MyQstandardItem = qstandarditem_creation.clone_creation()

            if isinstance(qs_clone, Link):
                nom_ouvrage_lien = qs_clone.text()

                if not couper or not update:
                    link_list.append(nom_ouvrage_lien)

                self.material_update_link_number(nom_ouvrage_lien)

            if qstandarditem_creation.hasChildren() and ajouter_enfant:
                qstandarditem_creation.clone_children(qs_original=qstandarditem_creation, qs_destination=qs_clone)

            if not couper and not update:
                self.coller_gestion_nom_ouvrage(qs_clone)

            liste_cloner.append(qs_clone)

        qs_destination.insertRow(index_insertion, liste_cloner)

        if qs_destination == self.cat_model.invisibleRootItem():
            return

        if not isinstance(qs_destination, Component) and not isinstance(qs_destination, Link):

            qmodelindex_filtre: QModelIndex = self.map_to_filter(qs_destination.index())

            if qmodelindex_filtre is not None:
                self.ui.hierarchy.expand(qmodelindex_filtre)

    def coller_gestion_nom_ouvrage(self, qs_clone: MyQstandardItem):

        if isinstance(qs_clone, Attribute):
            return

        if isinstance(qs_clone, Component) or isinstance(qs_clone, Link):
            return

        if isinstance(qs_clone, Material):

            texte = qs_clone.text()
            texte_upper = texte.upper()

            if texte_upper in material_upper_list:
                texte = find_new_title(texte, material_upper_list)
                texte_upper = texte.upper()

                qs_clone.setText(texte)
                qs_clone.ouvrage_lien = False

                material_list.append(texte)
                material_upper_list.append(texte_upper)

            else:

                material_list.append(texte)
                material_upper_list.append(texte_upper)
                qs_clone.setText(texte)

            return

        nb_enfants = qs_clone.rowCount()

        if nb_enfants == 0:
            return

        for index_child in range(nb_enfants):
            qstandarditem_child: MyQstandardItem = qs_clone.child(index_child, col_cat_value)

            self.coller_gestion_nom_ouvrage(qstandarditem_child)

    @staticmethod
    def recherche_index_valeur(qs_parent: QStandardItem, valeur: str, index_initial: int) -> int:

        if qs_parent.rowCount() == 0:
            return index_initial

        for index_qstandarditem in range(qs_parent.rowCount()):

            qstandarditem_enfant_valeur = qs_parent.child(index_qstandarditem, col_cat_value)
            valeur_actuelle = qstandarditem_enfant_valeur.text()

            if valeur_actuelle == valeur:
                return index_qstandarditem

        return index_initial

    @staticmethod
    def a___________________attribute_clean______():
        pass

    def attributes_clean_up(self):

        self.ui.attributes_detail.clear()

    @staticmethod
    def a___________________attribute_delete______():
        pass

    def attribute_delete(self):

        selection_list = self.ui.attributes_detail.selectedItems()

        if len(selection_list) == 0:
            return

        qm_list: list = self.get_filter_selection_list()

        if len(qm_list) > 1:
            return

        qm: QModelIndex = qm_list[0]
        ele_type = qm.data(user_data_type)

        if ele_type != material_code and ele_type != component_code:
            return

        for qlistwidgetitem in selection_list:

            qlistwidgetitem: QListWidgetItem

            widget_type = qlistwidgetitem.data(user_data_type)
            number = qlistwidgetitem.data(user_data_number)

            if widget_type == type_nom or widget_type == type_code or \
                    widget_type == type_lien:
                continue

            detail_row = self.ui.attributes_detail.row(qlistwidgetitem)

            if widget_type == type_layer:
                if number == attribute_val_default_layer_first:
                    self.attribute_delete_ation(qm, number, detail_row)
                    continue

            if widget_type == type_fill:
                if number == attribute_val_default_fill_first:
                    self.attribute_delete_ation(qm, number, detail_row)
                    continue

            if widget_type == type_room:
                if number == attribute_val_default_room_first:
                    self.attribute_delete_ation(qm, number, detail_row)
                    continue

            self.attribute_delete_ation(qm, number, detail_row)

    def attribute_delete_ation(self, qm: QModelIndex, number: str, detail_row: int):

        qs: MyQstandardItem = self.get_qs_by_qm(qm)

        attributes_count = qs.rowCount()

        if number == attribute_val_default_layer_first:
            numbers_list = list(attribute_val_default_layer)
            attribute_type = type_layer
            attribute_val_first = attribute_val_default_layer_first
            attribute_val_last = attribute_val_default_layer_last

        elif number == attribute_val_default_fill_first:
            numbers_list = list(attribute_val_default_fill)
            attribute_type = type_fill
            attribute_val_first = attribute_val_default_fill_first
            attribute_val_last = attribute_val_default_fill_last

        elif number == attribute_val_default_room_first:
            numbers_list = list(attribute_val_default_room)
            attribute_type = type_room
            attribute_val_first = attribute_val_default_room_first
            attribute_val_last = attribute_val_default_room_last

        # elif number == attribute_val_default_ht_first:
        #     numbers_list = list(attribute_val_default_ht)
        #     attribute_type = type_ht
        #     attribute_val_first = attribute_val_default_ht_first
        #     attribute_val_last = attribute_val_default_ht_last

        else:
            numbers_list = [number]
            attribute_type = ""
            attribute_val_first = ""
            attribute_val_last = ""

        dict_comp = dict()
        index_sup_list = list()
        current_row_s = -1
        liste_ele_s = list()

        for attribute_index in range(attributes_count):

            qs_val: MyQstandardItem = qs.child(attribute_index, col_cat_value)
            qs_number: MyQstandardItem = qs.child(attribute_index, col_cat_number)

            if qs_val is None or qs_number is None:
                continue

            if not isinstance(qs_val, Attribute):
                return

            current_number: str = qs_number.text()

            if current_number == "207":
                continue

            if current_number not in numbers_list:
                continue

            current_row = qs_number.row()

            # ---------------------------------------
            # Gestion suppression attribut non spécial
            # ---------------------------------------

            if attribute_type == "":

                liste_ele = qs.takeRow(current_row)

                self.undo_del_attribute(qs_parent=qs,
                                        index_attribut=current_row,
                                        liste_ele=liste_ele,
                                        dict_comp=dict(),
                                        type_attribut="")
                if detail_row == -1:
                    self.change_made = True
                    return

                self.ui.attributes_detail.takeItem(detail_row)
                self.change_made = True
                return

            # ---------------------------------------
            # Gestion suppression attribut spécial
            # ---------------------------------------

            if current_number == attribute_val_first:

                current_row_s = current_row
                liste_ele_s: list = [qs.child(attribute_index, index_colonne)
                                     for index_colonne in range(qs.columnCount())]

            else:

                dict_comp[current_row] = [qs.child(attribute_index, index_colonne)
                                          for index_colonne in range(qs.columnCount())]

            index_sup_list.append(current_row)

            if current_number != attribute_val_last:
                continue

            self.undo_del_attribute(qs_parent=qs,
                                    index_attribut=current_row_s,
                                    liste_ele=liste_ele_s,
                                    dict_comp=dict_comp,
                                    type_attribut=attribute_type)
            break

        index_sup_list.sort(key=int, reverse=True)

        # Suppression attribut
        for index_sup in index_sup_list:
            qs.takeRow(index_sup)

        if detail_row == -1:
            self.change_made = True
            return

        self.ui.attributes_detail.takeItem(detail_row)
        self.change_made = True
        return

    def attribute_delete_check(self):
        """Permet d'autoriser ou refuser la suppression d'un attribut protéger (Nom ou Code)"""

        selection_list = self.ui.attributes_detail.selectedItems()

        if len(selection_list) == 0:
            return False, False

        selection_list.sort(key=lambda v: self.ui.attributes_detail.row(v), reverse=True)

        for qlistwidgetitem in selection_list:

            qlistwidgetitem: QListWidgetItem

            widget_type = qlistwidgetitem.data(user_data_number)

            if widget_type == attribute_default_base or widget_type == type_nom:
                return False, False

            if widget_type == "207":
                return len(selection_list) != 1, True

        return True, True

    @staticmethod
    def a___________________attributes_copy______():
        pass

    def attribute_cut(self):

        self.attribute_copy_search(cut=True)

    def attribute_copy(self):

        self.attribute_copy_search()

    def attribute_copy_search(self, cut=False):

        selection_list = self.get_attribute_selection_list()

        if len(selection_list) == 0:
            return

        qs_selection_list = self.get_qs_selection_list()

        if len(qs_selection_list) == 0:
            return

        first_qs: MyQstandardItem = qs_selection_list[0]

        if not isinstance(first_qs, MyQstandardItem):
            return

        if isinstance(first_qs, Link):
            return

        clipboard, clipboard_cut = self.get_clipboard(ele_type=attribute_code, reset_clipboard=True)

        self.clipboard_current = attribute_code

        for qlistwidgetitem in selection_list:

            qlistwidgetitem: QListWidgetItem

            widget_type = qlistwidgetitem.data(user_data_type)
            number = qlistwidgetitem.data(user_data_number)

            if widget_type == type_nom or widget_type == type_code or \
                    widget_type == type_lien:
                continue

            if widget_type == type_layer:

                temp_list = list()
                cut_list = list()

                for number in attribute_val_default_layer:

                    qs_list: list = self.attribute_copy_action(first_qs, number)

                    if qs_list is None:
                        temp_list = list()
                        break

                    temp_list.extend(qs_list)
                    cut_list.append(qs_list[0])

                if len(temp_list) == 0:
                    continue

                clipboard.append(key=self.tr("Groupe Layer"),
                                 value=temp_list)

                if cut:

                    qs_value_list = self.attribute_get_original(qs_parent=first_qs,
                                                                numbers_list=list(attribute_val_default_layer.keys()))

                    if len(qs_value_list) != len(attribute_val_default_layer):
                        continue

                    clipboard_cut.append(key=self.tr("Groupe Layer"),
                                         value=[first_qs, qs_value_list])

                continue

            if widget_type == type_fill:

                temp_list = list()
                cut_list = list()

                for number in attribute_val_default_fill:

                    qs_list: list = self.attribute_copy_action(first_qs, number)

                    if qs_list is None:
                        temp_list = list()
                        break

                    temp_list.extend(qs_list)
                    cut_list.append(qs_list[0])

                if len(temp_list) == 0:
                    continue

                clipboard.append(key=self.tr("Groupe Remplissage"),
                                 value=temp_list)

                if cut:

                    qs_value_list = self.attribute_get_original(qs_parent=first_qs,
                                                                numbers_list=list(attribute_val_default_fill.keys()))

                    if len(qs_value_list) != len(attribute_val_default_fill):
                        continue

                    clipboard_cut.append(key=self.tr("Groupe Remplissage"),
                                         value=[first_qs, qs_value_list])

                continue

            if widget_type == type_room:

                temp_list = list()
                cut_list = list()

                for number in attribute_val_default_room:

                    qs_list: list = self.attribute_copy_action(first_qs, number)

                    if qs_list is None:
                        temp_list = list()
                        break

                    temp_list.extend(qs_list)
                    cut_list.append(qs_list[0])

                if len(temp_list) == 0:
                    continue

                clipboard.append(key=self.tr("Groupe Pièce"),
                                 value=temp_list)

                if cut:

                    qs_value_list = self.attribute_get_original(qs_parent=first_qs,
                                                                numbers_list=list(attribute_val_default_room.keys()))

                    if len(qs_value_list) != len(attribute_val_default_room):
                        continue

                    clipboard_cut.append(key=self.tr("Groupe Pièce"),
                                         value=[first_qs, qs_value_list])
                continue

            qs_list: list = self.attribute_copy_action(first_qs, number)

            if qs_list is None:
                continue

            attribute_name = self.allplan.find_datas_by_number(number, code_attr_name)

            qs_value: MyQstandardItem = qs_list[0]
            value = qs_value.text()

            clipboard.append(key=f"{number} -- {attribute_name} -- {value}",
                             value=qs_list)

            if cut:

                qs_value_list = self.attribute_get_original(qs_parent=first_qs, numbers_list=[number])

                if len(qs_value_list) != 1:
                    continue

                clipboard_cut.append(key=f"{number} -- {attribute_name} -- {value}",
                                     value=[first_qs, qs_value_list[0]])

        self.asc.boutons_hierarchie_coller(attribute_code)

    @staticmethod
    def attribute_get_original(qs_parent: MyQstandardItem, numbers_list: list) -> list:

        if not isinstance(qs_parent, (Material, Component)) or not isinstance(numbers_list, list):
            return list()

        qs_value_list = list()

        for number in numbers_list:

            qs_original_list = qs_parent.get_attribute_line_by_number(number=number)

            if len(qs_original_list) != qs_parent.columnCount():
                return list()

            qs_value_original = qs_original_list[col_cat_value]

            if not isinstance(qs_value_original, Attribute):
                continue

            qs_value_list.append(qs_value_original)

        return qs_value_list

    def get_attribute_selection_list(self) -> list:

        selection_list = self.ui.attributes_detail.selectedItems()

        if len(selection_list) == 0:
            return selection_list

        datas = dict()
        row_list = list()

        for qlistwidgetitem in selection_list:
            qlistwidgetitem: QListWidgetItem

            row_index = self.ui.attributes_detail.row(qlistwidgetitem)

            datas[row_index] = qlistwidgetitem
            row_list.append(row_index)

        row_list.sort(key=int)

        final_list = [datas[row_index] for row_index in row_list]

        return final_list

    @staticmethod
    def attribute_copy_action(qs: MyQstandardItem, number: str):

        attributes_count = qs.rowCount()

        qs_list = list()

        for attribute_index in range(attributes_count):

            qs_value: MyQstandardItem = qs.child(attribute_index, col_cat_value)
            qs_number: MyQstandardItem = qs.child(attribute_index, col_cat_number)

            if not isinstance(qs_value, Attribute):
                return qs_list

            current_number: str = qs_number.text()

            if current_number != number:
                continue

            for column_index in range(qs.columnCount()):
                qs_copy: MyQstandardItem = qs.child(attribute_index, column_index)

                if qs_copy is None:
                    return qs_list

                qs_list.append(qs_copy.clone_creation())

            return qs_list

        return list()

    @staticmethod
    def a___________________attributes_paste______():
        pass

    def attribute_paste(self, title="", id_ele="0") -> bool:

        cut = self.clipboard_attribute_cut.len_datas() != 0

        result = self.attribute_paste_action(clipboard_attribute=self.clipboard_attribute,
                                             title=title, id_ele=id_ele)

        if not cut:
            return result

        if not result:
            return False

        self.attribute_couper_coller_action()
        return True

    def attribute_paste_action(self, clipboard_attribute: ClipboardDatas, title="", id_ele="0") -> bool:

        columns_count: int = self.cat_model.columnCount()

        liste_hierarchie_qs_selection: list = self.get_qs_selection_list()
        nb_qstandarditem: int = len(liste_hierarchie_qs_selection)

        attributs_copier = dict()

        if title == "":

            for titre_actuel in clipboard_attribute.keys():
                self.attributs_coller_datas(clipboard_attribute=clipboard_attribute,
                                            titre_actuel=titre_actuel,
                                            attributs_copier=attributs_copier,
                                            id_ele=id_ele)

        elif title in clipboard_attribute.keys():
            self.attributs_coller_datas(clipboard_attribute=clipboard_attribute,
                                        titre_actuel=title,
                                        attributs_copier=attributs_copier,
                                        id_ele=id_ele)

        else:
            print("onglet_hierarchie -- attributs_coller_action --> nb_items_copier = 0")
            return False

        nb_items_copier: int = len(attributs_copier)

        # ------------------------------------------------------------------------
        # Vérification si la sélection de la hiérarchie est une simple ou étendue
        # ------------------------------------------------------------------------
        if nb_qstandarditem == 0:
            return False

        if nb_qstandarditem > 1:

            if nb_items_copier == 1:

                for liste_datas in attributs_copier.items():

                    liste_datas: tuple

                    if len(liste_datas) != 2:
                        continue

                    liste_qs_copier = liste_datas[1]

                    # liste_datas = ( numero, [qstandarditem col0, qstandarditem col1, ...])

                    if len(liste_qs_copier) != columns_count:
                        continue

                    question = msg(titre=application_title,
                                   message=self.tr("Voulez-vous vraiment coller l'attribut dans "
                                                   "les éléments selectionnés?"),
                                   type_bouton=QMessageBox.Ok | QMessageBox.No,
                                   defaut_bouton=QMessageBox.Ok,
                                   icone_avertissement=True)

                    if question == QMessageBox.No or question == QMessageBox.Cancel:
                        return False

            else:

                question = msg(titre=application_title,
                               message=self.tr("Voulez-vous vraiment coller les attributs "
                                               "dans les éléments selectionnés?"),
                               type_bouton=QMessageBox.Ok | QMessageBox.No,
                               defaut_bouton=QMessageBox.Ok,
                               icone_avertissement=True)

                if question == QMessageBox.No or question == QMessageBox.Cancel:
                    return False

        # ------------------------------------------------------------------------
        # rechercher si des attributs sont déjà existants dans la sélection
        # ------------------------------------------------------------------------

        maj_attribut = True
        liste_attributs_existants = list()

        premier: MyQstandardItem = liste_hierarchie_qs_selection[0]

        for qstandarditem in liste_hierarchie_qs_selection:

            if qstandarditem is None:
                print("onglet_hierarchie -- attributs_coller_action --> qstandarditem is None")
                continue

            qstandarditem: MyQstandardItem
            current_colone = qstandarditem.column()

            if current_colone != col_cat_value:
                continue

            liste_numeros = qstandarditem.get_attribute_numbers_list()

            for number in liste_numeros:

                if number == attribute_default_base:
                    continue

                if number in attribute_val_default_layer:
                    number = attribute_val_default_layer_first

                elif number in attribute_val_default_fill:
                    number = attribute_val_default_fill_first

                elif number in attribute_val_default_room:
                    number = attribute_val_default_room_first

                # elif number in attribute_val_default_ht:
                #     number = "112"

                if number not in attributs_copier:
                    continue

                if number not in liste_attributs_existants:
                    liste_attributs_existants.append(number)

        if not isinstance(premier, Folder):

            b = self.tr("existe déjà, voulez-vous le mettre à jour?")

            if len(liste_attributs_existants) != 0:

                title = liste_attributs_existants[0]

                question = msg(titre=application_title,
                               message=f"{title} {b}",
                               type_bouton=QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel,
                               defaut_bouton=QMessageBox.Ok,
                               infos="attributes_update",
                               bt_ok=self.tr("Mettre à jour"),
                               bt_no=self.tr("Ignorer"),
                               icone_question=True)

                if question == QMessageBox.Cancel:
                    return False

                if question == QMessageBox.No:
                    maj_attribut = False

        # ------------------------------------------------------------------------
        # rechercher si des attributs sont déjà existants dans la sélection
        # ------------------------------------------------------------------------

        for qstandarditem in liste_hierarchie_qs_selection:

            if qstandarditem is None:
                print("onglet_hierarchie -- attributs_coller_action --> qstandarditem is None")
                continue

            qstandarditem: MyQstandardItem
            current_colone = qstandarditem.column()

            if current_colone != col_cat_value:
                continue

            if isinstance(qstandarditem, Link):
                continue

            liste_attributs = qstandarditem.get_attribute_numbers_list()

            dict_comp_l = dict()
            dict_comp_ml = dict()

            dict_comp_r = dict()
            dict_comp_mr = dict()

            dict_comp_p = dict()
            dict_comp_mp = dict()

            # dict_comp_h = dict()
            # dict_comp_mh = dict()

            for number in attributs_copier:

                if number == "207":
                    self.attributs_update_description(qstandarditem, attributs_copier[number])

                # ----------------------------------
                #  Mise à jour
                # ----------------------------------

                if number in liste_attributs and maj_attribut:

                    line_list = qstandarditem.get_attribute_line_by_number(number)

                    if len(line_list) != self.cat_model.columnCount():
                        print("catalog_manage -- attributs_paste --> len(line_list) != self.cat_model.columnCount()")
                        continue

                    qs_value, qs_index = line_list[col_cat_value], line_list[col_cat_index]

                    if not isinstance(qs_value, Attribute) or not isinstance(qs_index, Attribute):
                        print("catalog_manage -- attributs_paste --> "
                              "not isinstance(qs_value, Attribute) or not isinstance(qs_index, Attribute)")
                        continue

                    val1 = qs_value.text()
                    index1 = qs_index.text()

                    qs_value_copy: MyQstandardItem = attributs_copier[number][col_cat_value]
                    qs_index_copy: MyQstandardItem = attributs_copier[number][col_cat_index]

                    if not isinstance(qs_value_copy, Attribute) or not isinstance(qs_index_copy, Attribute):
                        print("catalog_manage -- attributs_paste --> "
                              "not isinstance(qs_value_copy, Attribute) or not isinstance(qs_index_copy, Attribute)")
                        continue

                    val2 = qs_value_copy.text()
                    index2 = qs_index_copy.text()

                    print(f"{val1} ({qs_value.text()}) --> {val2} ({qs_index_copy.text()})")

                    qs_value.setText(val2)
                    qs_index.setText(index2)

                    self.change_made = True

                    if number in attribute_val_default_layer:

                        dict_comp_ml[number] = {"numero": number,
                                                "valeur_originale": val1,
                                                "nouveau_texte": val2,
                                                "ancien_index": index1,
                                                "nouvel_index": index2,
                                                "qs_value": qs_value}

                        if number != attribute_val_default_layer_last:
                            continue

                        val1 = dict_comp_ml[attribute_val_default_layer_first]["valeur_originale"]
                        val2 = dict_comp_ml[attribute_val_default_layer_first]["nouveau_texte"]
                        ancien_index = dict_comp_ml[attribute_val_default_layer_first]["ancien_index"]
                        nouvel_index = dict_comp_ml[attribute_val_default_layer_first]["nouvel_index"]
                        qs_value = dict_comp_ml[attribute_val_default_layer_first]["qs_value"]

                        dict_comp_ml.pop(attribute_val_default_layer_first)

                        self.undo_modify_attribute(qs_actuel=qs_value,
                                                   numero=attribute_val_default_layer_first,
                                                   ancienne_valeur=val1,
                                                   nouvelle_valeur=val2,
                                                   ancien_index=ancien_index,
                                                   nouvel_index=nouvel_index,
                                                   dict_comp=dict_comp_ml,
                                                   type_attribut=self.tr("Groupe Layer"))

                        continue

                    if number in attribute_val_default_fill:

                        dict_comp_mr[number] = {"numero": number,
                                                "valeur_originale": val1,
                                                "nouveau_texte": val2,
                                                "ancien_index": index1,
                                                "nouvel_index": index2,
                                                "qs_value": qs_value}

                        if number != attribute_val_default_fill_last:
                            continue

                        val1 = dict_comp_mr[attribute_val_default_fill_first]["valeur_originale"]
                        val2 = dict_comp_mr[attribute_val_default_fill_first]["nouveau_texte"]
                        ancien_index = dict_comp_mr[attribute_val_default_fill_first]["ancien_index"]
                        nouvel_index = dict_comp_mr[attribute_val_default_fill_first]["nouvel_index"]
                        qs_value = dict_comp_ml[attribute_val_default_layer_first]["qs_value"]

                        dict_comp_mr.pop(attribute_val_default_fill_first)

                        self.undo_modify_attribute(qs_actuel=qs_value,
                                                   numero=attribute_val_default_fill_first,
                                                   ancienne_valeur=val1,
                                                   nouvelle_valeur=val2,
                                                   ancien_index=ancien_index,
                                                   nouvel_index=nouvel_index,
                                                   dict_comp=dict_comp_mr,
                                                   type_attribut=self.tr("Groupe Remplissage"))

                        continue

                    if number in attribute_val_default_room:

                        dict_comp_mp[number] = {"numero": number,
                                                "valeur_originale": val1,
                                                "nouveau_texte": val2,
                                                "ancien_index": index1,
                                                "nouvel_index": index2,
                                                "qs_value": qs_value}

                        if number != attribute_val_default_room_last:
                            continue

                        val1 = dict_comp_mp[attribute_val_default_room_first]["valeur_originale"]
                        val2 = dict_comp_mp[attribute_val_default_room_first]["nouveau_texte"]
                        ancien_index = dict_comp_mp[attribute_val_default_room_first]["ancien_index"]
                        nouvel_index = dict_comp_mp[attribute_val_default_room_first]["nouvel_index"]
                        qs_value = dict_comp_ml[attribute_val_default_layer_first]["qs_value"]

                        dict_comp_mp.pop(attribute_val_default_room_first)

                        self.undo_modify_attribute(qs_actuel=qs_value,
                                                   numero=attribute_val_default_room_first,
                                                   ancienne_valeur=val1,
                                                   nouvelle_valeur=val2,
                                                   ancien_index=ancien_index,
                                                   nouvel_index=nouvel_index,
                                                   dict_comp=dict_comp_mp,
                                                   type_attribut=self.tr("Groupe Pièce"))

                        continue

                    self.undo_modify_attribute(qs_actuel=qs_value,
                                               numero=number,
                                               ancienne_valeur=val1,
                                               nouvelle_valeur=val2,
                                               ancien_index=index1,
                                               nouvel_index=index2,
                                               dict_comp=dict(),
                                               type_attribut="")

                    continue

                # ----------------------------------
                #  Creation
                # ----------------------------------

                elif number not in liste_attributs:

                    index_insertion = qstandarditem.get_attribute_insertion_index(number=number)

                    liste_insertion = list()
                    liste_actuelle: list = attributs_copier[number]

                    for qstandarditem_temp in liste_actuelle:

                        if not isinstance(qstandarditem_temp, MyQstandardItem):
                            continue

                        qstandarditem_nouveau = qstandarditem_temp.clone_creation()

                        if qstandarditem_temp.column() == col_cat_value:
                            qstandarditem_temp.clone_children(qs_original=qstandarditem_temp,
                                                              qs_destination=qstandarditem_nouveau)

                        liste_insertion.append(qstandarditem_nouveau)

                    qstandarditem.insertRow(index_insertion, liste_insertion)

                    self.change_made = True

                    if number in attribute_val_default_layer:
                        dict_comp_l[index_insertion] = liste_insertion
                        if number == attribute_val_default_layer_last:
                            self.undo_add_attribute(qs_parent=qstandarditem,
                                                    index_attribut=index_insertion,
                                                    liste_ele=list(),
                                                    dict_comp=dict_comp_l,
                                                    type_attribut=self.tr("Groupe Layer"))
                        continue

                    if number in attribute_val_default_fill:
                        dict_comp_r[index_insertion] = liste_insertion
                        if number == attribute_val_default_fill_last:
                            self.undo_add_attribute(qs_parent=qstandarditem,
                                                    index_attribut=index_insertion,
                                                    liste_ele=list(),
                                                    dict_comp=dict_comp_r,
                                                    type_attribut=self.tr("Groupe Remplissage"))
                        continue

                    if number in attribute_val_default_room:
                        dict_comp_p[index_insertion] = liste_insertion

                        if number == attribute_val_default_room_last:
                            self.undo_add_attribute(qs_parent=qstandarditem,
                                                    index_attribut=index_insertion,
                                                    liste_ele=list(),
                                                    dict_comp=dict_comp_p,
                                                    type_attribut=self.tr("Groupe Pièce"))
                        continue

                    else:

                        self.undo_add_attribute(qs_parent=qstandarditem,
                                                index_attribut=index_insertion,
                                                liste_ele=liste_insertion,
                                                dict_comp=dict())

        return True

    def attribut_coller_recherche(self, liste_selections_qstandarditem: list, message=False) -> bool:

        nb_selections = len(liste_selections_qstandarditem)

        nb_attribut_copier: int = self.clipboard_attribute.len_datas()
        nb_attribut_couper: int = self.clipboard_attribute_cut.len_datas()

        if nb_selections == 0 or nb_attribut_copier == 0:
            return False

        qstandarditem: MyQstandardItem = liste_selections_qstandarditem[0]

        if not isinstance(qstandarditem, MyQstandardItem):
            return False

        if isinstance(qstandarditem, Link):
            return False

        if isinstance(qstandarditem, Folder):

            if nb_attribut_copier != 1:
                return False

            if nb_attribut_couper != 0:
                return False

            liste_titres: list = self.clipboard_attribute.keys()

            for key in liste_titres:

                if "207" in key:
                    return True

            return False

        if len(liste_selections_qstandarditem) > 1 and nb_attribut_couper != 0:

            if not message:
                return False

            if nb_attribut_couper == 2:
                msg(titre=application_title,
                    message=self.tr("Impossible de couper/coller un attribut dans plusieurs éléments."),
                    icone_critique=True)
                return False

            msg(titre=application_title,
                message=self.tr("Impossible de couper/coller des attributs dans plusieurs éléments."),
                icone_critique=True)
            return False

        return True

    def attributs_coller_datas(self, clipboard_attribute: ClipboardDatas,
                               titre_actuel: str, attributs_copier: dict, id_ele="0"):

        nb_colonnes: int = self.cat_model.columnCount()

        liste_attributs_a: list = clipboard_attribute.get_datas_title(titre_actuel, id_ele)
        nb_items = len(liste_attributs_a)

        if nb_items == 0:
            return

        liste_attributs_a: list = liste_attributs_a[0]

        nb_items = len(liste_attributs_a)

        if titre_actuel == self.tr("Groupe Layer"):

            if nb_items != nb_colonnes * len(attribute_val_default_layer):
                print("onglet_hierarchie -- attributs_coller_action --> nb_items != nb_colonnes * 5")
                return

            index_1 = 0
            index_2 = 1

            for numero in attribute_val_default_layer:
                attributs_copier[numero] = liste_attributs_a[nb_colonnes * index_1:nb_colonnes * index_2]
                index_1 += 1
                index_2 += 1
            return

        if titre_actuel == self.tr("Groupe Remplissage"):

            if nb_items != nb_colonnes * len(attribute_val_default_fill):
                print("onglet_hierarchie -- attributs_coller_action --> nb_items != nb_colonnes * 5")
                return

            index_1 = 0
            index_2 = 1

            for numero in attribute_val_default_fill:
                attributs_copier[numero] = liste_attributs_a[nb_colonnes * index_1:nb_colonnes * index_2]
                index_1 += 1
                index_2 += 1
            return

        if titre_actuel == self.tr("Groupe Pièce"):

            if nb_items != nb_colonnes * len(attribute_val_default_room):
                print("onglet_hierarchie -- attributs_coller_action --> nb_items != nb_colonnes * 6")
                return

            index_1 = 0
            index_2 = 1

            for numero in attribute_val_default_room:
                attributs_copier[numero] = liste_attributs_a[nb_colonnes * index_1:nb_colonnes * index_2]
                index_1 += 1
                index_2 += 1
            return

        # if titre_actuel == self.tr("Groupe Hauteur"):

        #     if nb_items != nb_colonnes * len(attribute_val_default_ht):
        #         print("onglet_hierarchie -- attributs_coller_action --> nb_items != nb_colonnes * 8")
        #         return
        #
        #     index_1 = 0
        #     index_2 = 1
        #
        #     for numero in attribute_val_default_ht:
        #         attributs_copier[numero] = liste_attributs_a[nb_colonnes * index_1:nb_colonnes * index_2]
        #         index_1 += 1
        #         index_2 += 1
        #     return

        if " -- " not in titre_actuel:
            print("onglet_hierarchie -- attributs_coller_action --> titre non valide")
            return

        numero, _ = titre_actuel.split(sep=" -- ", maxsplit=1)
        datas = clipboard_attribute.get_datas_title(titre_actuel, id_ele)

        if len(datas) != 0:
            attributs_copier[numero] = datas[0]

    def attributs_update_description(self, qs_actuel: QStandardItem, liste_actuelle: list):

        if qs_actuel is None:
            return

        qs_parent = qs_actuel.parent()

        if qs_parent is None:
            qs_parent = self.cat_model.invisibleRootItem()

        current_row = qs_actuel.row()

        if len(liste_actuelle) == 0:
            return

        qs_valeur: QStandardItem = liste_actuelle[0]

        if not isinstance(qs_valeur, Attribute):
            return

        valeur_txt = qs_valeur.text()

        if not isinstance(valeur_txt, str):
            return

        qs_description = qs_parent.child(current_row, col_cat_desc)

        if not isinstance(qs_description, Info):
            return

        qs_description.setText(valeur_txt)

    def attribute_couper_coller_action(self):

        qs_cut_list = self.clipboard_attribute_cut.get_values_list()

        for qs_list in qs_cut_list:

            if not isinstance(qs_list, list):
                continue

            if len(qs_list) != 2:
                continue

            # liste_datas = [qstandarditem_parent, qstandarditem]

            qs_parent: MyQstandardItem = qs_list[0]
            qs_value: MyQstandardItem = qs_list[1]

            if not isinstance(qs_parent, (Material, Component)):
                continue

            if isinstance(qs_value, Attribute):

                index_row: int = qs_value.row()

                if index_row == -1:
                    continue

                qs_del = qs_parent.child(index_row, col_cat_value)

                if not isinstance(qs_del, Attribute) or qs_del != qs_value:
                    continue

                qs_parent.takeRow(index_row)

            elif isinstance(qs_value, list):

                for qs in qs_value:

                    index_row: int = qs.row()

                    if index_row == -1:
                        continue

                    qs_del = qs_parent.child(index_row, col_cat_value)

                    if not isinstance(qs_del, Attribute) or qs_del != qs:
                        continue

                    qs_parent.takeRow(index_row)

        # reset cut clipboard !

        self.clipboard_attribute_cut.clear()
        self.change_made = True

    @staticmethod
    def a___________________gestion_erreurs___________________():
        pass

    def erreur_selectionner_premiere(self):

        if not self.ui.search_error_bt.isChecked():
            return

        if self.cat_filter_2.rowCount() == 0:
            self.ui.search_error_bt.setChecked(False)
            self.ui.search_error_bt.clicked.emit()
            return

        qmodelindex = self.erreur_rechercher_formule(self.cat_filter_2, self.cat_filter_2.index(0, 0))

        if qmodelindex is None:
            return

        self.catalog_select_action([qmodelindex])

    def erreur_rechercher_formule(self, filtre_actuel: QSortFilterProxyModel, qmodelindex_parent: QModelIndex):

        parent_nb_enfants = filtre_actuel.rowCount(qmodelindex_parent)

        for index_row in range(parent_nb_enfants):

            qmodelindex = filtre_actuel.index(index_row, col_cat_value, qmodelindex_parent)

            if qmodelindex is None:
                continue

            if not qmodelindex.isValid():
                continue

            # test1 = qmodelindex_parent.data()
            # test2 = qmodelindex.data()

            formule_ok = qmodelindex.data(user_formule_ok)

            if formule_ok is not None:

                if formule_ok != "":

                    qmodelindex_select = qmodelindex.parent()

                    # test3 = qmodelindex_select.data()

                    qmodelindex_hierachie = self.cat_filter.mapFromSource(qmodelindex_select)

                    if qmodelindex_hierachie is None:
                        return None

                    if not qmodelindex_hierachie.isValid():
                        return None

                    # test4 = qmodelindex_hierachie.data()

                    return qmodelindex_hierachie

            nb_enfants = filtre_actuel.rowCount(qmodelindex)

            if nb_enfants != 0:
                return self.erreur_rechercher_formule(filtre_actuel, qmodelindex)

            return qmodelindex

    @staticmethod
    def a___________________gestion_renommer___________________():
        pass

    def renommer_item(self):

        if self.ui.attributes_detail.count() == 0:
            return

        qlistwidgetitem: QListWidgetItem = self.ui.attributes_detail.item(0)

        widget = self.ui.attributes_detail.itemWidget(qlistwidgetitem)

        if not isinstance(widget, AttributeCode) and not isinstance(widget, AttributeName):
            return

        widget.ui.value_attrib.selectAll()
        widget.ui.value_attrib.setFocus()

    @staticmethod
    def a___________________gestion_formule_parentheses______():
        pass

    def change_highlighter(self):

        self.allplan.formula_color = not self.allplan.formula_color
        self.formula_color_change_signal.emit()

    @staticmethod
    def a___________________gestion_retour___________________():
        pass

    def undo_add_ele(self, qs_parent: MyQstandardItem, qs_actuel: MyQstandardItem, index_ele: int,
                     liste_ele: list, coller=False):

        type_element = qs_actuel.data(user_data_type)
        titre_element = qs_actuel.text()

        if coller:
            a = self.tr("Coller")
            nom_action = f'{a} {type_element} : {titre_element}'

        else:
            a = self.tr("Ajout")
            nom_action = f'{a} {type_element} : {titre_element}'

        self.undo_list.ajouter_ele(nom_action=nom_action,
                                   qs_parent=qs_parent,
                                   qs_actuel=qs_actuel,
                                   index_ele=index_ele,
                                   liste_ele=liste_ele)

        self.redo_clear()
        self.undo_button_manage()

    def undo_cut_ele(self, qs_parent_actuel: MyQstandardItem, qs_parent_futur: MyQstandardItem,
                     qs_actuel: MyQstandardItem,
                     row_actuel: int, row_futur: int, liste_ele: list):

        type_element = qs_actuel.data(user_data_type)
        titre_element = qs_actuel.text()

        a = self.tr("Couper/Coller")
        nom_action = f'{a} {type_element} : {titre_element}'

        self.undo_list.couper_ele(nom_action=nom_action,
                                  qs_parent_actuel=qs_parent_actuel,
                                  qs_parent_futur=qs_parent_futur,
                                  qs_actuel=qs_actuel,
                                  row_actuel=row_actuel,
                                  row_futur=row_futur,
                                  liste_ele=liste_ele)

        self.redo_clear()
        self.undo_button_manage()

    def undo_del_ele(self, qs_parent: QStandardItem, qs_actuel: QStandardItem, index_ele: int,
                     liste_ele: list):

        type_element = qs_actuel.data(user_data_type)
        titre_element = qs_actuel.text()

        a = self.tr("Supprimer")

        self.undo_list.suppression_ele(nom_action=f'{a} {type_element} : '
                                                  f'{titre_element}',
                                       qs_parent=qs_parent,
                                       qs_actuel=qs_actuel,
                                       index_ele=index_ele,
                                       liste_ele=liste_ele)

        self.redo_clear()
        self.undo_button_manage()

    def undo_move_ele(self, qs_parent: QStandardItem, qs_actuel: QStandardItem, row_actuel: int,
                      row_futur: int):

        a = self.tr("Déplacement")

        self.undo_list.deplacer_ele(nom_action=f"{a} '{qs_actuel.text()}'",
                                    qs_parent=qs_parent,
                                    qs_actuel=qs_actuel,
                                    row_actuel=row_actuel,
                                    row_futur=row_futur)

        self.redo_clear()
        self.undo_button_manage()

    def undo_move_materials(self, qs_parent: QStandardItem, qs_new_list: list):

        self.undo_list.move_materials(nom_action=self.tr("Déplacement vers dossier"),
                                      qs_parent=qs_parent,
                                      qs_new_list=qs_new_list)

        self.redo_clear()
        self.undo_button_manage()

    def undo_library_synchro(self):

        if len(self.library_synchro_list) == 0:
            return

        self.undo_list.library_synchro(nom_action=self.tr("Synchronisation"),
                                       library_synchro_list=self.library_synchro_list)

        self.redo_clear()
        self.undo_button_manage()

    def undo_icon_changed(self, qs_actuel: QStandardItem, ancien_icone: str, nouvel_icone: str):

        a = self.tr("Changement icône")

        self.undo_list.modif_icone(nom_action=f"{a} : '{qs_actuel.text()}'",
                                   qs_actuel=qs_actuel,
                                   ancien_icone=ancien_icone,
                                   nouvel_icone=nouvel_icone)

        self.redo_clear()
        self.undo_button_manage()

    def undo_add_attribute(self, qs_parent: QStandardItem, index_attribut: int, liste_ele: list,
                           dict_comp: dict, type_attribut=""):

        qs_numero: QStandardItem = qs_parent.child(index_attribut, col_cat_number)

        if qs_numero is None:
            return

        numero = qs_numero.text()
        titre_actuel = qs_parent.text()

        if type_attribut != "":
            a = self.tr("Ajouter attribut")
            nom_action = f"[{titre_actuel}] {a} {type_attribut}"

        else:
            a = self.tr("Ajouter")
            nom_action = f"[{titre_actuel}] {a} @{numero}@"

        self.undo_list.ajouter_attribut(nom_action=nom_action,
                                        qs_parent=qs_parent,
                                        index_attribut=index_attribut,
                                        liste_ele=liste_ele,
                                        dict_comp=dict_comp,
                                        type_attribut=type_attribut)

        self.redo_clear()
        self.undo_button_manage()

    def undo_modify_attribute(self, qs_actuel: MyQstandardItem,
                              numero: str, ancienne_valeur: str, nouvelle_valeur: str, ancien_index="-1",
                              nouvel_index="-1", dict_comp=None, type_attribut=""):

        if dict_comp is None:
            dict_comp = {}

        if ancienne_valeur == nouvelle_valeur and ancien_index == nouvel_index:
            return

        # print(numero, ancienne_valeur, nouvelle_valeur, ancien_index, nouvel_index)

        if not isinstance(qs_actuel, MyQstandardItem):
            return

        qs_parent = qs_actuel.parent()

        if not isinstance(qs_parent, MyQstandardItem):
            qs_parent = self.cat_model.invisibleRootItem()

        titre_actuel = qs_actuel.text()
        index_ele = qs_actuel.row()

        nb_colonnes = self.cat_model.columnCount()

        # ------

        liste_ele = [qs_parent.child(index_ele, index_colonne) for index_colonne in range(nb_colonnes)
                     if qs_parent.child(index_ele, index_colonne) is not None]

        if len(liste_ele) != self.cat_model.columnCount():
            return

        if len(dict_comp) == 0:

            a = self.tr("modification")
            b = self.tr("Vide")

            nom_action = f"[{titre_actuel}] {a} @{numero}@"

            if ancienne_valeur == "":
                ancienne_valeur_tps = f"'{b}'"
            else:
                ancienne_valeur_tps = ancienne_valeur

            if nouvelle_valeur == "":
                nouvelle_valeur_tps = f"'{b}'"
            else:
                nouvelle_valeur_tps = nouvelle_valeur
            a = self.tr("modification attribut")
            tooltips = (f'{titre_actuel} : {a} {numero} \n'
                        f"     {ancienne_valeur_tps} --> {nouvelle_valeur_tps}")

        else:
            dict_comp: dict

            a = self.tr("modification")

            nom_action = f'[{titre_actuel}] {a} {type_attribut}'

            b = self.tr("modification attribut")
            tooltips = (f'{titre_actuel} : {b} {type_attribut} \n'
                        f"     {numero} --> {ancienne_valeur} --> {nouvelle_valeur}")

            for dict_datas in dict_comp.values():

                dict_datas: dict

                numero_comp = dict_datas["numero"]
                val_o_comp = dict_datas["valeur_originale"]
                val_f_comp = dict_datas["nouveau_texte"]

                if val_o_comp == val_f_comp:
                    continue

                b = self.tr("Vide")

                if val_o_comp == "":
                    val_o_comp = f"'{b}'"

                if val_f_comp == "":
                    val_f_comp = f"'{b}'"

                tooltips += f"\n     {numero_comp} --> {val_o_comp} --> {val_f_comp}"

        self.undo_list.modifier_attribut(nom_action=nom_action,
                                         tooltips=tooltips,
                                         qs_parent=qs_parent,
                                         qs_actuel=qs_actuel,
                                         index_ele=index_ele,
                                         liste_ele=liste_ele,
                                         ancienne_valeur=ancienne_valeur,
                                         nouvelle_valeur=nouvelle_valeur,
                                         ancien_index=ancien_index,
                                         nouvel_index=nouvel_index,
                                         dict_comp=dict_comp,
                                         type_attribut=type_attribut)

        self.redo_clear()
        self.undo_button_manage()

    def undo_del_attribute(self, qs_parent: QStandardItem, index_attribut: int, liste_ele: list,
                           dict_comp: dict, type_attribut: str):

        qs_numero: QStandardItem = liste_ele[col_cat_number]

        if qs_numero is None:
            return

        titre_actuel = qs_parent.text()
        numero = qs_numero.text()

        if type_attribut != "":
            a = self.tr("Supprimer attribut")
            nom_action = f'[{titre_actuel}] {a} {type_attribut}'

        else:
            a = self.tr("Supprimer")
            nom_action = f'[{titre_actuel}] {a} @{numero}@'

        self.undo_list.supprimer_attribut(nom_action=nom_action,
                                          qs_parent=qs_parent,
                                          index_attribut=index_attribut,
                                          liste_ele=liste_ele,
                                          dict_comp=dict_comp)

        self.redo_clear()
        self.undo_button_manage()

    def undo(self, action_actuelle: ActionInfo):

        type_action = action_actuelle.action_type

        data: dict = action_actuelle.data

        id_action: int = data["id_action"]

        # -------------------------
        # Ajouter -> supprimer ele
        # -------------------------

        if type_action == ajouter_ele:

            qs_parent: QStandardItem = data["qs_parent"]
            qs_actuel: QStandardItem = data["qs_actuel"]

            qm = self.cat_model.indexFromItem(qs_actuel)

            if not qm_check(qm):
                return

            index_ele = qm.row()

            ele_type = qm.data(user_data_type)

            self.material_is_deletable(qs=qs_actuel, delete=True)

            qs_parent.takeRow(index_ele)

            if ele_type == attribute_code:
                qs_selection = qs_parent

            else:

                last_item = qs_parent.rowCount() - 1
                first_item = 0

                if isinstance(qs_parent, MyQstandardItem):
                    attributes_list = qs_parent.get_attribute_numbers_list()
                    first_item = len(attributes_list)

                if index_ele < first_item:
                    index_ele = first_item
                elif index_ele > last_item:
                    index_ele = last_item

                qs_selection = qs_parent.child(index_ele, col_cat_value)

            if qs_selection is None:
                print("catalog -- undo -- qs_selection is None")
            else:
                self.catalog_select_action([qs_selection])

            self.undo_action_end(id_action)
            return

        # -------------------------
        # Couper
        # -------------------------

        if type_action == couper_ele:

            id_action = data["id_action"]
            qs_parent_actuel: QStandardItem = data["qs_parent_actuel"]
            qs_parent_futur: QStandardItem = data["qs_parent_futur"]
            row_actuel: int = data["row_actuel"]
            row_futur: int = data["row_futur"]
            liste_ele: list = data["liste_ele"]

            nb_enfants = qs_parent_futur.rowCount()

            if row_futur > nb_enfants:
                return

            qs_parent_futur.takeRow(row_futur)

            qs_parent_actuel.insertRow(row_actuel, liste_ele)

            self.catalog_select_action([qs_parent_actuel.child(row_actuel, col_cat_value)])

            self.undo_action_end(id_action)

            return

        # -------------------------
        # Supprimer -> Ajouter ele
        # -------------------------

        if type_action == supprimer_ele:

            id_action = data["id_action"]
            qs_parent: QStandardItem = data["qs_parent"]
            index_ele: int = data["index_ele"]
            liste_ele: list = data["liste_ele"]

            nb_enfants = qs_parent.rowCount()

            if index_ele > nb_enfants:
                index_ele = 0

            qs_parent.insertRow(index_ele, liste_ele)

            qs_actuel: MyQstandardItem = data["qs_actuel"]
            self.material_add(qs_actuel)

            self.catalog_select_action([qs_parent.child(index_ele, col_cat_value)])

            self.undo_action_end(id_action)

            return

        # -------------------------
        # Re-Placer de l'élément déplacer
        # -------------------------

        if type_action == deplacer_ele:
            qs_parent: QStandardItem = data["qs_parent"]
            row_actuel: int = data["row_actuel"]
            row_futur: list = data["row_futur"]

            liste_ele = qs_parent.takeRow(row_futur)
            qs_parent.insertRow(row_actuel, liste_ele)

            self.catalog_select_action([qs_parent.child(row_actuel, col_cat_value)])

            self.undo_action_end(id_action)

            return

        # -------------------------
        # Re-placer Material
        # -------------------------

        if type_action == deplacer_material:

            qs_parent = data["qs_parent"]
            qs_new_list = data["qs_new_list"]

            if not isinstance(qs_parent, Folder) or not isinstance(qs_new_list, list):
                return

            if len(qs_new_list) != qs_parent.columnCount():
                return

            qs_new_parent = qs_new_list[0]

            if not isinstance(qs_new_parent, Folder):
                return

            row_count = qs_new_parent.rowCount()

            attributes_list = qs_parent.get_attribute_numbers_list()
            attributes_count = len(attributes_list)

            for row_index in reversed(range(row_count)):

                qs_current = qs_new_parent.child(row_index, col_cat_value)

                if not isinstance(qs_current, Material):
                    continue

                children_qs_list = qs_new_parent.takeRow(row_index)

                if not isinstance(children_qs_list, list):
                    continue

                if len(children_qs_list) != qs_parent.columnCount():
                    continue

                qs_parent.insertRow(attributes_count, children_qs_list)

            folder_new_row_index = qs_new_parent.row()

            qs_parent.takeRow(folder_new_row_index)

            self.catalog_select_action([qs_parent])
            self.undo_action_end(id_action)

            return

        # -------------------------
        # Re-Modifier l'icône du dossier
        # -------------------------

        if type_action == modif_icone:
            qs_actuel: MyQstandardItem = data["qs_actuel"]
            ancien_icone = data["ancien_icone"]

            qs_actuel.icon_path = ancien_icone
            qs_actuel.setIcon(get_icon(ancien_icone))

            self.undo_action_end(id_action)

            current_element = self.get_current_qs()

            if current_element == qs_actuel:
                self.catalog_select_action([current_element])
            return

        # -------------------------
        # Supprimer l'attribut créé
        # -------------------------

        if type_action == ajouter_attr:

            qs_parent: QStandardItem = data["qs_parent"]
            index_attribut: int = data["index_attribut"]
            dict_comp: dict = data["dict_comp"]

            if len(dict_comp) != 0:

                for index_ele in reversed(dict_comp):
                    qs_parent.takeRow(index_ele)
            else:
                qs_parent.takeRow(index_attribut)

            self.catalog_select_action([qs_parent])
            self.undo_action_end(id_action)

            return

        # -------------------------
        # Re-Modifier l'attribut modifié
        # -------------------------

        if type_action == modifier_attr:

            qs_parent: MyQstandardItem = data["qs_parent"]
            liste_ele: list = data["liste_ele"]

            ancienne_valeur: str = data["ancienne_valeur"]
            nouvelle_valeur: str = data["nouvelle_valeur"]
            ancien_index: str = data["ancien_index"]
            nouvel_index: str = data["nouvel_index"]
            dict_comp: dict = data["dict_comp"]

            if dict_comp is None:
                dict_comp = dict()

            # Modification des attributs complémentaires

            if len(dict_comp) != 0:
                for dict_datas in dict_comp.values():

                    dict_datas: dict

                    numero_comp = dict_datas["numero"]
                    val_o_comp = dict_datas["valeur_originale"]
                    val_f_comp = dict_datas["nouveau_texte"]
                    ind_o_comp = dict_datas["ancien_index"]
                    ind_f_comp = dict_datas["nouvel_index"]

                    if val_o_comp == val_f_comp and ind_o_comp == ind_f_comp:
                        continue

                    recherche = qs_parent.get_attribute_line_by_number(numero_comp)

                    qs_val_comp = recherche[0]

                    if val_o_comp != val_f_comp:
                        if not isinstance(qs_val_comp, MyQstandardItem):
                            continue

                        qs_val_comp.setText(val_o_comp)

                    qs_ind_comp = recherche[1]

                    if ind_o_comp != ind_f_comp:

                        if not isinstance(qs_ind_comp, MyQstandardItem):
                            continue

                        qs_ind_comp.setText(ind_o_comp)

            qs_numero: QStandardItem = liste_ele[col_cat_number]

            if qs_numero is not None:

                numero = qs_numero.text()

                if numero == attribute_default_base and isinstance(qs_parent, Material):
                    self.material_code_renamed(code_before=nouvelle_valeur,
                                               code_after=ancienne_valeur)

                if numero == "207":

                    index_207: int = qs_parent.row()
                    qs_parent_207: QStandardItem = qs_parent.parent()

                    if qs_parent_207 is None:
                        qs_parent_207 = self.cat_model.invisibleRootItem()

                    qs_desc = qs_parent_207.child(index_207, col_cat_desc)

                    if isinstance(qs_desc, Info):

                        valeur_actuel = qs_desc.text()

                        if valeur_actuel == nouvelle_valeur and valeur_actuel != ancienne_valeur:
                            qs_desc.setText(ancienne_valeur)

            # Modification de l'attribut principal

            qs_val: QStandardItem = liste_ele[col_cat_value]

            if qs_val is not None:

                valeur_actuel = qs_val.text()

                if valeur_actuel == nouvelle_valeur and valeur_actuel != ancienne_valeur:
                    qs_val.setText(ancienne_valeur)

            qs_index: QStandardItem = liste_ele[col_cat_index]

            if qs_index is not None:

                index_actuel = qs_index.text()

                if index_actuel == nouvel_index and index_actuel != ancien_index:
                    qs_index.setText(ancien_index)

            self.undo_action_end(id_action)

            self.catalog_select_action([qs_parent])
            return

        # -------------------------
        # Création l'attribut supprimer
        # -------------------------

        if type_action == supprimer_attr:

            qs_parent: QStandardItem = data["qs_parent"]
            index_attribut: int = data["index_attribut"]
            liste_ele: list = data["liste_ele"]
            dict_comp: dict = data["dict_comp"]

            if len(dict_comp) != 0:

                qs_parent.insertRow(index_attribut, liste_ele)

                for index_ele, liste_ele in dict_comp.items():
                    qs_parent.insertRow(index_ele, liste_ele)
            else:

                qs_parent.insertRow(index_attribut, liste_ele)

            self.undo_action_end(id_action)

            self.catalog_select_action([qs_parent])

            return

        # -------------------------
        # Library synchonization
        # -------------------------

        if type_action == library_synchro_code:

            library_synchro_list = data["library_synchro_list"]

            if not isinstance(library_synchro_list, list):
                return

            qs_parent = QStandardItem()

            for datas in reversed(library_synchro_list):

                if not isinstance(datas, dict):
                    continue

                qs_parent = datas.get("qs_parent")

                if not isinstance(qs_parent, (Folder, Material, Component)):
                    continue

                is_creation = datas.get("creation", False)

                # ------------
                # Suppression
                # ------------

                if is_creation:

                    index_attribut = datas.get("index_attribut")

                    if not isinstance(index_attribut, int):
                        continue

                    if index_attribut < 0:
                        continue

                    qs_parent.takeRow(index_attribut)

                    continue

                # ------------
                # Update
                # ------------

                qs_value = datas.get("qs_value")

                if not isinstance(qs_value, Attribute):
                    continue

                value_before = datas.get("value_before")

                if not isinstance(value_before, str):
                    continue

                # ------------

                qs_index_value = datas.get("qs_index_value")

                if not isinstance(qs_index_value, Attribute):
                    continue

                index_value_before = datas.get("index_value_before")

                if not isinstance(index_value_before, str):
                    continue

                # ------------

                qs_value.setText(value_before)
                qs_index_value.setText(index_value_before)

                # ------------

                qs_desc = datas.get("qs_desc")

                if isinstance(qs_desc, Info):
                    qs_desc.setText(value_before)

            self.undo_action_end(id_action)

            if not isinstance(qs_parent, (Folder, Material, Component)):
                return

            self.catalog_select_action([qs_parent])

            return

            # ------------

        self.undo_action_end(id_action)
        return

    def undo_action_end(self, nom_action: int):

        action = self.undo_list.dict_actions.get(nom_action, None)

        if action is None:
            return

        self.redo_list.dict_actions[nom_action] = action
        self.undo_list.supprimer_action(nom_action)

        self.undo_button_manage()
        self.redo_button_manage()

    def undo_button_manage(self):
        self.ui.undo_bt.setEnabled(len(self.undo_list.dict_actions) != 0)
        self.ui.undo_list_bt.setEnabled(len(self.undo_list.dict_actions) != 0)

    def get_special_number(self, qs_parent: MyQstandardItem, number: str) -> Tuple[str, dict]:
        """
        Rechercher si numéro d'attribut est un numéro spécial.
        :param qs_parent:
        :param number:
        :return: type de d'attribut , dict {index_ele : liste_ele}
        """

        if number in attribute_val_default_layer:
            return "Layer", self.creation_liste_complementaire(qs_parent=qs_parent,
                                                               datas_dict=attribute_val_default_layer)

        if number in attribute_val_default_fill:
            return "Remplissage", self.creation_liste_complementaire(qs_parent=qs_parent,
                                                                     datas_dict=attribute_val_default_fill)

        if number in attribute_val_default_room:
            return "Pièce", self.creation_liste_complementaire(qs_parent=qs_parent,
                                                               datas_dict=attribute_val_default_room)

        # if number in attribute_val_default_ht:
        #     return "Hauteur", self.creation_liste_complementaire(qs_parent=qs_parent,
        #                                                          datas_dict=attribute_val_default_ht)

        return "", dict()

    @staticmethod
    def creation_liste_complementaire(qs_parent: MyQstandardItem, datas_dict: dict) -> dict:

        dict_complementaires = dict()

        for numero_rechercher in datas_dict:

            qs_list = qs_parent.get_attribute_line_by_number(number=numero_rechercher)

            qs_val = qs_list[0]

            if not isinstance(qs_val, Attribute):
                continue

            index_ele = qs_val.row() + 1

            liste_ele = [qs_parent.child(index_ele, index_colonne)
                         for index_colonne in range(qs_parent.columnCount())
                         if qs_parent.child(index_ele, index_colonne) is not None]

            dict_complementaires[index_ele] = liste_ele

        return dict_complementaires

    @staticmethod
    def a___________________gestion_revenir___________________():
        pass

    def redo(self, action_actuelle):

        type_action = action_actuelle.action_type

        data: dict = action_actuelle.data

        id_action: int = data["id_action"]

        if type_action == ajouter_ele:
            qs_parent: QStandardItem = data["qs_parent"]
            liste_ele: list = data["liste_ele"]
            index_ele = data["index_ele"]

            qs_parent.insertRow(index_ele, liste_ele)

            qs_actuel: MyQstandardItem = data["qs_actuel"]

            self.material_add(qs_actuel)

            self.catalog_select_action([qs_parent.child(index_ele, col_cat_value)])

            self.redo_action_end(id_action)

            return

        # -------------------------
        # Création de l'élément supprimer
        # -------------------------

        if type_action == couper_ele:

            id_action = data["id_action"]
            qs_parent_futur: QStandardItem = data["qs_parent_actuel"]
            qs_parent_actuel: QStandardItem = data["qs_parent_futur"]
            row_futur: int = data["row_actuel"]
            row_actuel: int = data["row_futur"]
            liste_ele: list = data["liste_ele"]

            nb_enfants = qs_parent_futur.rowCount()

            if row_futur > nb_enfants:
                return

            qs_parent_futur.takeRow(row_futur)

            qs_parent_actuel.insertRow(row_actuel, liste_ele)

            self.catalog_select_action([qs_parent_actuel.child(row_actuel, col_cat_value)])

            self.redo_action_end(id_action)

            return

        # -------------------------
        # Supprimer
        # -------------------------

        if type_action == supprimer_ele:
            id_action = data["id_action"]
            qs_parent: QStandardItem = data["qs_parent"]
            index_ele: int = data["index_ele"]

            if index_ele >= qs_parent.rowCount():
                index_ele = 0

            qs_actuel: MyQstandardItem = data["qs_actuel"]
            self.material_is_deletable(qs=qs_actuel, delete=True)

            qs_parent.takeRow(index_ele)

            self.catalog_select_action([qs_parent.child(index_ele, col_cat_value)])

            self.redo_action_end(id_action)

            return

        # -------------------------
        # Re-placer élément
        # -------------------------

        if type_action == deplacer_ele:
            qs_parent: QStandardItem = data["qs_parent"]
            row_actuel: int = data["row_actuel"]
            row_futur: list = data["row_futur"]

            liste_ele = qs_parent.takeRow(row_futur)
            qs_parent.insertRow(row_actuel, liste_ele)

            self.catalog_select_action([qs_parent.child(row_actuel, col_cat_value)])

            self.redo_action_end(id_action)

            return

        # -------------------------
        # Re-placer Material
        # -------------------------

        if type_action == deplacer_material:

            qs_parent = data["qs_parent"]
            qs_new_list = data["qs_new_list"]

            if not isinstance(qs_parent, Folder) or not isinstance(qs_new_list, list):
                return

            if len(qs_new_list) != qs_parent.columnCount():
                return

            qs_folder_new = qs_new_list[0]

            if not isinstance(qs_folder_new, Folder):
                return

            attributes_list = qs_folder_new.get_attribute_numbers_list()
            attributes_count = len(attributes_list)

            parent_child_count = qs_parent.rowCount()

            for row_index in reversed(range(parent_child_count)):

                child_qs_current = qs_parent.child(row_index, 0)

                if not isinstance(child_qs_current, Material):
                    continue

                material_qs_list = qs_parent.takeRow(row_index)

                if len(material_qs_list) != qs_parent.columnCount():
                    continue

                qs_folder_new.insertRow(attributes_count, material_qs_list)

            qs_parent.appendRow(qs_new_list)

            self.catalog_expand_action(expanded_list=[qs_folder_new])
            self.catalog_select_action(selected_list=[qs_folder_new])

            self.redo_action_end(id_action)

            return

        # -------------------------
        # Modifier icône
        # -------------------------

        if type_action == modif_icone:
            qs_actuel: MyQstandardItem = data["qs_actuel"]
            nouvel_icone = data["nouvel_icone"]

            qs_actuel.icon_path = nouvel_icone
            qs_actuel.setIcon(get_icon(nouvel_icone))

            self.catalog_select_action([qs_actuel])

            self.redo_action_end(id_action)

            return

        if type_action == ajouter_attr:

            qs_parent: QStandardItem = data["qs_parent"]
            index_attribut: int = data["index_attribut"]
            liste_ele: list = data["liste_ele"]
            dict_comp: dict = data["dict_comp"]

            if len(dict_comp) != 0:
                for index_ele, liste_ele in dict_comp.items():
                    qs_parent.insertRow(index_ele, liste_ele)
            else:

                qs_parent.insertRow(index_attribut, liste_ele)

            self.catalog_select_action([qs_parent])

            self.redo_action_end(id_action)

            return

        if type_action == modifier_attr:

            qs_parent: QStandardItem = data["qs_parent"]
            dict_comp: dict = data["dict_comp"]

            if qs_parent is None:
                return

            if dict_comp is None:
                dict_comp = dict()

            # Modification des attributs complémentaires

            if len(dict_comp) != 0:
                for dict_datas in dict_comp.values():

                    dict_datas: dict

                    numero_comp = dict_datas["numero"]
                    val_o_comp = dict_datas["valeur_originale"]
                    val_f_comp = dict_datas["nouveau_texte"]
                    ind_o_comp = dict_datas["ancien_index"]
                    ind_f_comp = dict_datas["nouvel_index"]

                    if val_o_comp == val_f_comp and ind_o_comp == ind_f_comp:
                        continue

                    recherche = qs_parent.recherche_numero(numero_comp)

                    qs_val_comp = recherche[0]

                    if val_o_comp != val_f_comp:
                        if not isinstance(qs_val_comp, MyQstandardItem):
                            continue

                        qs_val_comp.setText(val_f_comp)

                    qs_ind_comp = recherche[1]

                    if ind_o_comp != ind_f_comp:

                        if not isinstance(qs_ind_comp, MyQstandardItem):
                            continue

                        qs_ind_comp.setText(ind_f_comp)

            # Modification de l'attribut principal

            liste_ele: list = data["liste_ele"]

            ancienne_valeur: str = data["ancienne_valeur"]
            nouvelle_valeur: str = data["nouvelle_valeur"]
            ancien_index: str = data["ancien_index"]
            nouvel_index: str = data["nouvel_index"]

            qs_numero: QStandardItem = liste_ele[col_cat_number]

            if qs_numero is not None:

                numero = qs_numero.text()

                if numero == attribute_default_base and isinstance(qs_parent, Material):
                    self.material_code_renamed(code_before=ancienne_valeur,
                                               code_after=nouvelle_valeur)

                if numero == "207":

                    index_207: int = qs_parent.row()
                    qs_parent_207: QStandardItem = qs_parent.parent()

                    if qs_parent_207 is None:
                        qs_parent_207 = self.cat_model.invisibleRootItem()

                    qs_desc = qs_parent_207.child(index_207, col_cat_desc)

                    if isinstance(qs_desc, Info):

                        valeur_actuel = qs_desc.text()

                        if valeur_actuel == ancienne_valeur and valeur_actuel != nouvelle_valeur:
                            qs_desc.setText(nouvelle_valeur)

            qs_val: QStandardItem = liste_ele[col_cat_value]

            if qs_val is not None:
                valeur_actuel = qs_val.text()

                if valeur_actuel == ancienne_valeur and valeur_actuel != nouvelle_valeur:
                    qs_val.setText(nouvelle_valeur)

            qs_index: QStandardItem = liste_ele[col_cat_index]

            if qs_index is not None:
                index_actuel = qs_index.text()

                if index_actuel == ancien_index and index_actuel != nouvel_index:
                    qs_index.setText(nouvel_index)

            self.catalog_select_action([qs_parent])

            self.redo_action_end(id_action)
            return

        if type_action == supprimer_attr:
            qs_parent: QStandardItem = data["qs_parent"]
            index_attribut: int = data["index_attribut"]

            qs_parent.takeRow(index_attribut)

            self.catalog_select_action([qs_parent])

            self.redo_action_end(id_action)

            return

        # -------------------------
        # Description Update
        # -------------------------

        if type_action == library_synchro_code:

            qs_parent = QStandardItem()

            library_synchro_list = data["library_synchro_list"]

            if not isinstance(library_synchro_list, list):
                return

            for datas in library_synchro_list:

                if not isinstance(datas, dict):
                    continue

                is_creation = datas.get("creation", False)

                # ------------
                # Création
                # ------------

                if is_creation:

                    qs_parent = datas.get("qs_parent")

                    if not isinstance(qs_parent, (Material, Component)):
                        continue

                    index_attribut = datas.get("index_attribut")

                    if not isinstance(index_attribut, int):
                        continue

                    if index_attribut < 0:
                        continue

                    liste_ele = datas.get("liste_ele")

                    if not isinstance(liste_ele, list):
                        continue

                    qs_parent.appendRow(liste_ele)

                    continue

                # ------------
                # Update
                # ------------

                if not isinstance(datas, dict):
                    continue

                qs_value = datas.get("qs_value")

                if not isinstance(qs_value, Attribute):
                    continue

                value_after = datas.get("value_after")

                if not isinstance(value_after, str):
                    continue

                # ------------

                qs_index_value = datas.get("qs_index_value")

                if not isinstance(qs_index_value, Attribute):
                    continue

                index_value_after = datas.get("index_value_after")

                if not isinstance(index_value_after, str):
                    continue

                # ------------

                qs_value.setText(value_after)

                qs_index_value.setText(index_value_after)

                # ------------

                qs_desc = datas.get("qs_desc")

                if isinstance(qs_desc, Info):
                    qs_desc.setText(value_after)

            self.redo_action_end(id_action)

            if not isinstance(qs_parent, (Folder, Material, Component)):
                return

            self.catalog_select_action([qs_parent])
            return

    def redo_action_end(self, nom_action: int):

        action = self.redo_list.dict_actions.get(nom_action, None)

        if action is None:
            return

        self.undo_list.dict_actions[nom_action] = action
        self.redo_list.supprimer_action(nom_action)

        self.undo_button_manage()
        self.redo_button_manage()

    def redo_clear(self):

        self.redo_list.clear()
        self.redo_button_manage()

    def redo_button_manage(self):
        self.ui.redo_bt.setEnabled(len(self.redo_list.dict_actions) != 0)
        self.ui.redo_list_bt.setEnabled(len(self.redo_list.dict_actions) != 0)

    @staticmethod
    def a___________________library_update_description___________________():
        pass

    def library_synchro(self, code: str, number: str, value: str, index_value: str, item_type: str,
                        creation: bool) -> int:

        search_code = self.cat_model.findItems(code, Qt.MatchExactly | Qt.MatchRecursive, col_cat_value)

        synchro_count = 0

        if len(search_code) == 0:
            return synchro_count

        for qs in search_code:

            qs: MyQstandardItem

            ele_type_curent = qs.data(user_data_type)

            if item_type != ele_type_curent:
                continue

            results = qs.get_attribute_line_by_number(number=number)

            if not isinstance(results, list):
                continue

            if len(results) < col_cat_desc:

                if not creation:
                    continue

                insertion_index = qs.get_attribute_insertion_index(number=number)

                if not isinstance(insertion_index, int):
                    continue

                if insertion_index < 0:
                    continue

                if index_value != "-1":
                    qs_list = self.allplan.creation.attribute_line(value=index_value, number=number)
                else:
                    qs_list = self.allplan.creation.attribute_line(value=value, number=number)

                qs.insertRow(insertion_index, qs_list)

                self.library_synchro_list.append({"qs_parent": qs,
                                                  "index_attribut": insertion_index,
                                                  "liste_ele": qs_list,
                                                  "creation": True})

                synchro_count += 1

                continue

            # ------------------------------

            qs_attribute_value = results[col_cat_value]

            if not isinstance(qs_attribute_value, Attribute):
                continue

            attribute_value = qs_attribute_value.text()

            if not isinstance(attribute_value, str):
                continue

            if attribute_value == value:
                continue

            # ------------------------------

            qs_index_value = results[col_cat_index]

            if not isinstance(qs_index_value, Attribute):
                continue

            index_value_before = qs_index_value.text()

            if not isinstance(index_value_before, str):
                continue

            # ------------------------------

            if number == "207":

                qs_parent = qs.parent()

                if not isinstance(qs_parent, MyQstandardItem):
                    continue

                qs_desc = qs_parent.child(qs.row(), col_cat_desc)

                if not isinstance(qs_desc, Info):
                    continue

                qs_desc.setText(value)

                index_value_before = "-1"

            else:
                qs_desc = None

                # ------------------------------

            if index_value_before != index_value:
                qs_index_value.setText(index_value)

            qs_attribute_value.setText(value)

            synchro_count += 1

            self.library_synchro_list.append({"qs_parent": qs,
                                              "qs_value": qs_attribute_value,
                                              "qs_desc": qs_desc,
                                              "qs_index_value": qs_index_value,
                                              "value_before": attribute_value,
                                              "value_after": value,
                                              "index_value_before": index_value_before,
                                              "index_value_after": index_value,
                                              "creation": False})

        return synchro_count

    def library_synchro_end(self):
        self.catalog_modif_manage()

        selection_list = self.ui.hierarchy.selectionModel().selectedRows()

        if len(selection_list) == 0:
            return

        self.catalog_select_action(selected_list=selection_list, scrollto=False)

    @staticmethod
    def a___________________backup_restore___________________():
        pass

    def backup_restore_action(self, backup_path: str, backup_index: str) -> str:

        if not os.path.exists(backup_path):
            print("catalog_manage -- backup_restore_action -- not os.path.exists(backup_path")
            return f"{backup_path} don't exist"

        backup_time = os.path.getmtime(backup_path)

        # ------------------------
        # Swap catalog
        # ------------------------

        try:

            new_path = f"{backup_path}.bak"

            if os.path.exists(new_path):
                os.remove(new_path)

            os.rename(self.catalog_path, new_path)

            os.rename(backup_path, self.catalog_path)

            os.rename(new_path, backup_path)

        except Exception as error:
            return f"error swap catalog: {error}"

        # ------------------------
        # Swap display
        # ------------------------

        if not os.path.exists(self.catalog_settings_folder):
            print(f"catalog_manage -- backup_restore_action -- not os.path.exists(self.catalog_settings_folder)")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        if not os.path.exists(self.catalog_setting_display_file):
            print(f"catalog_manage -- backup_restore_action -- not os.path.exists(self.catalog_setting_display_file)")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        if backup_index == "00":
            backup_display = f"{self.catalog_settings_folder}backup\\{self.catalog_name}_display.xml"
        else:
            backup_display = f"{self.catalog_settings_folder}backup\\{self.catalog_name}_display - {backup_index}.xml"

        if not os.path.exists(backup_display):
            print(f"catalog_manage -- backup_restore_action -- not os.path.exists(backup_display)")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        try:

            backup_display_time = os.path.getmtime(backup_display)

            datetime1 = datetime.fromtimestamp(backup_time)
            datetime2 = datetime.fromtimestamp(backup_display_time)

            time_difference = abs(datetime1 - datetime2).total_seconds()

            if time_difference > 10:
                print(f"catalog_manage -- backup_restore_action -- time_difference > 10")
                self.catalog_load_start(catalog_path=self.catalog_path)
                return ""

        except Exception as error:
            print(f"catalog_manage -- backup_restore_action -- error time difference : {error}")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        try:

            new_path = f"{backup_display}.bak"

            if os.path.exists(new_path):
                os.remove(new_path)

            os.rename(self.catalog_setting_display_file, new_path)

            os.rename(backup_display, self.catalog_setting_display_file)

            os.rename(new_path, backup_display)

            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

        except Exception as error:
            print(f"catalog_manage -- backup_restore_action -- error swap display : {error}")
            self.catalog_load_start(catalog_path=self.catalog_path)
            return ""

    @staticmethod
    def a___________________end___________________():
        pass


class CatalogLoad(QObject):
    loading_completed = pyqtSignal(QStandardItemModel, list, list)
    errors_signal = pyqtSignal(list)

    def __init__(self, allplan, file_path: str, bdd_title: str):
        super().__init__()

        # ---------------------------------------
        # LOADING PARENTS
        # ---------------------------------------

        self.allplan: AllplanDatas = allplan

        self.allplan.creation.attributes_datas.clear()

        self.creation = self.allplan.creation

        # ---------------------------------------
        # LOADING VARIABLES
        # ---------------------------------------
        self.root = None

        self.region = ""

        self.expanded_list = list()
        self.selected_list = list()

        self.link_used_count = dict()
        self.dict_liens_node = dict()

        self.material_list = list()
        self.material_upper_list = list()
        self.link_list = list()
        self.material_with_link_list = list()

        self.file_path = file_path
        self.img_path_dict = dict()

        self.find_list = list()

        self.model_cat = QStandardItemModel()

        self.model_cat.setHorizontalHeaderLabels([bdd_title, self.tr("Description"), "num_attrib"])

        self.errors_list = list()

        self.link_orphan = list()

        # ---------------------------------------
        # LOADING Translation
        # ---------------------------------------

        self.error_material_exist = self.tr("Détection Doublons dans le dossier")
        self.error_renamed = self.tr("a été renommé")

    def run(self):

        self.model_cat.invisibleRootItem().setData(folder_code, user_data_type)

        tps = time.perf_counter()

        try:

            tree = etree.parse(self.file_path)
            self.root = tree.getroot()

            self.region = self.root.get("Region", self.allplan.langue)

            if self.region == "GB":
                self.region = "EN"

        except Exception as error:
            print(f"catalog_manage -- CatalogLoad -- analyse_display -- {error}")

            self.errors_signal.emit([f"{error}"])
            self.loading_completed.emit(self.model_cat,
                                        self.expanded_list,
                                        self.selected_list)
            return False

        # -------------------------------------------------
        # init affichage
        # -------------------------------------------------

        catalog_folder = find_folder_path(self.file_path)
        catalog_name = find_filename(self.file_path)

        if not catalog_name or not catalog_folder:
            self.loading_completed.emit(self.model_cat,
                                        self.expanded_list,
                                        self.selected_list)
            print(f"catalog_manage -- CatalogLoad -- analyse_display -- not catalog_name or not catalog_folder")
            return

        root_display = self.display_load(catalog_name=catalog_name, catalog_folder=catalog_folder)

        # -------------------------------------------------
        # chargement hierarchie
        # -------------------------------------------------

        self.model_cat.beginResetModel()

        self.catalog_load(self.model_cat.invisibleRootItem(), self.root, root_display)

        if len(self.link_orphan) != 0:
            self.model_cat.appendRow(self.link_orphan)

        self.model_cat.endResetModel()

        # self.catalogue_charger_liens_manquants()
        #
        # if len(self.errors_list) != 0:
        #     self.errors_signal.emit(self.errors_list)

        self.loading_completed.emit(self.model_cat,
                                    self.expanded_list,
                                    self.selected_list)

        print(f"Catalog_load : {time.perf_counter() - tps}s")

    @staticmethod
    def display_load(catalog_name: str, catalog_folder: str):

        catalog_setting_folder = get_catalog_setting_folder(catalog_folder=catalog_folder)

        if not catalog_setting_folder:
            print(f"catalog_manage -- CatalogLoad --  display_load -- not catalog_setting_folder")
            return None

        catalog_setting_display_file = get_catalog_setting_display_file(catalog_settings_folder=catalog_setting_folder,
                                                                        catalog_name=catalog_name)

        if not catalog_setting_display_file:
            print(f"catalog_manage -- CatalogLoad --  display_load -- not catalog_setting_display_file")
            return None

        if not os.path.exists(catalog_setting_display_file):
            print(f"catalog_manage -- CatalogLoad --  display_load -- not os.path.exists(catalog_setting_display_file)")
            return None

        try:
            tree_display = etree.parse(catalog_setting_display_file)
            return tree_display.getroot()

        except Exception as error:
            print(f"catalog_manage -- CatalogLoad --  display_load -- {error}")
            return None

    def catalog_load(self, qs_parent: QStandardItem, element: etree._Element, element_display: etree._Element):

        for child in element:

            tag = child.tag

            if not isinstance(tag, str):
                print("catalog_manage -- CatalogLoad -- catalog_load -- not isinstance(tag, str)")
                continue

            # -----------------------------------------------
            # Links
            # -----------------------------------------------

            if tag == "Links":
                self.links_load(child)
                continue

            # -----------------------------------------------
            # Node
            # -----------------------------------------------

            if tag == "Node":

                name = child.get('name')

                if name is None:
                    print("catalog_manage -- CatalogLoad -- catalog_load -- name is None")
                    continue

                if name.startswith("------------------- ") and name.endswith(" ------------------- "):
                    continue

                description = child.get('comment', "")

                if name.endswith(f" -- {description}"):
                    name = name.replace(f" -- {description}", "")

                if element_display is None:

                    qs_list = self.creation.folder_line(value=name, description=description)
                    qs_current = qs_list[0]
                    current_display = None

                else:

                    search_child_display = catalog_xml_find_all(element=element_display,
                                                                tag="Node",
                                                                parameter="name",
                                                                value=name)

                    # search_child_display = element_display.findall(f'Node[@name="{name}"]')

                    search_count = len(search_child_display)

                    if search_count == 0:
                        qs_list = self.creation.folder_line(value=name, description=description)
                        qs_current = qs_list[0]
                        current_display = element_display

                        self.catalog_load(qs_current, child, current_display)
                        qs_parent.appendRow(qs_list)

                        continue

                    if search_count == 1:
                        current_display = search_child_display[0]

                    else:
                        current_display = None

                        for element in search_child_display:
                            if element not in self.find_list:
                                current_display = element
                                break

                        if current_display is None:
                            print(f"catalog_manage -- CatalogLoad -- catalog_load -- current_display is None--> "
                                  f"{tag} - {name}")
                            return element_display

                        self.find_list.append(current_display)

                    img_path = current_display.get("icon", current_display.get("icone_dossier", ""))

                    if img_path == "":
                        qs_list = self.creation.folder_line(value=name, description=description)

                    else:

                        if img_path in self.img_path_dict:
                            icon_path = self.img_path_dict[img_path]

                        elif img_path == "folder.png":
                            icon_path = folder_icon
                            self.img_path_dict[img_path] = icon_path

                        else:

                            icon_path = self.find_img(img_path)
                            self.img_path_dict[img_path] = icon_path

                        self.allplan.icon_list.append(icon_path)

                        qs_list = self.creation.folder_line(value=name,
                                                            description=description,
                                                            icon_path=icon_path)

                    qs_current = qs_list[0]

                    if current_display.get("expanded", current_display.get("deplier")) == "True":
                        self.expanded_list.append(qs_current)

                    if current_display.get("selected") == "True":
                        self.selected_list.append(qs_current)

                self.catalog_load(qs_current, child, current_display)

                qs_parent.appendRow(qs_list)

                continue

            # -----------------------------------------------
            # Group and Position
            # -----------------------------------------------

            if tag == "Group" or tag == "Position":
                self.children_load(child, element_display, qs_parent, tag)
                continue

            # -----------------------------------------------
            # Link
            # -----------------------------------------------

            if tag == "Link":

                name = child.get('name')

                if name is None:
                    print("catalog_manage -- CatalogLoad -- catalog_load -- name is None")
                    continue

                material_element = self.root.find(f'.//Group//GroupDef//Attribute[@value="{name}"]')

                description = ""

                if material_element is not None:

                    material_parent_elemnent = material_element.getparent()

                    if material_parent_elemnent is not None:

                        material_element = material_parent_elemnent.find(f'Attribute[@id="207"]')

                        if material_element is not None:
                            description = material_element.get("value", "")

                self.link_list.append(name)
                self.material_with_link_list.append(qs_parent.text().upper())

                qs_list = self.creation.link_line(value=name, description=description)
                qs_parent.appendRow(qs_list)

                self.display_parameters_check(element_display=element_display, qs_current=qs_list[0], tag=tag)

    @staticmethod
    def find_img(current_path: str):

        if current_path is None:
            print("catalog_manage -- CatalogLoad -- current_path -- current_path is None")
            return ""

        if os.path.exists(current_path):
            return current_path

        img_name = current_path.replace(".png", "")

        current_path = f"{icons_path}{datas_icons.get(img_name, img_name)}.png"

        if os.path.exists(current_path):
            return current_path

        print("catalog_manage -- CatalogLoad -- current_path -- img not found")
        return ""

    def children_load(self, child, element_display, qs_parent: QStandardItem, tag: str):

        presence_layer = False
        presence_remplissage = False
        presence_piece = False
        # presence_ht = False

        liste_defaut = list()
        datas_attribut_layer = dict(attribute_val_default_layer)
        datas_attribut_remp = dict(attribute_val_default_fill)
        datas_attribut_piece = dict(attribute_val_default_room)
        # datas_attribut_ht = dict(attribut_val_defaut_ht)

        liste_autres = list()

        liste_attributs = list()

        name = child.get("name", "")
        description = ""

        # ----------------------------
        # search attributes
        # ----------------------------

        attributes = child.findall(f'{tag}Def/Attribute')

        if len(attributes) == 0:
            print("catalog_manage -- CatalogLoad --  children_load -- len(attributes) == 0")
            return None

        for attribute in attributes:

            number = attribute.get("id")
            value = attribute.get("value", "")

            if number is None:
                print("catalog_manage -- CatalogLoad --  children_load -- number is None")
                return None

            if number in liste_attributs:
                print("catalog_manage -- CatalogLoad --  children_load -- number in liste_attributs")
                continue

            liste_attributs.append(number)

            # -----------------------------------------
            # Attribute 83
            # -----------------------------------------

            if number == attribute_default_base:
                name = value
                continue

            # -----------------------------------------
            # Attribute 207
            # -----------------------------------------

            if number == "207":
                description = value
                continue

            # -----------------------------------------
            # Attribute 202
            # -----------------------------------------

            if number == "202":
                liste_defaut.append([number, self.allplan.convert_unit(value)])
                continue

            # -----------------------------------------
            # Attribute 335
            # -----------------------------------------

            if number == "335":
                self.allplan.surface_all_list.append(value)

                if value not in self.allplan.surface_list:
                    self.allplan.surface_list.append(value)

                liste_autres.append([number, value])
                continue

            # -----------------------------------------
            # Attribute 120  - 209 - 110
            # -----------------------------------------

            if number in attribut_val_defaut_defaut:
                liste_defaut.append([number, value])
                continue

            # -----------------------------------------
            # Attribute 141 - 349 - 346 - 345 - 347
            # -----------------------------------------

            if number in attribute_val_default_layer:
                presence_layer = True
                datas_attribut_layer[number] = value
                continue

            # -----------------------------------------
            # Attribute 118 - 111 - 252 - 336 - 600
            # -----------------------------------------

            if number in attribute_val_default_fill:
                presence_remplissage = True
                datas_attribut_remp[number] = value
                continue

            # -----------------------------------------
            # Attribute 231 - 235 - 232 - 266 - 233 - 264
            # -----------------------------------------

            if number in attribute_val_default_room:
                presence_piece = True

                if number == "232":
                    datas_attribut_piece[number] = self.allplan.traduire_valeur_232(value_current=value,
                                                                                    region=self.region)

                elif number == "233":
                    datas_attribut_piece[number] = self.allplan.traduire_valeur_233(value_current=value,
                                                                                    region=self.region)

                elif number == "235":
                    datas_attribut_piece[number] = self.allplan.traduire_valeur_235(value_current=value,
                                                                                    region=self.region)

                else:
                    datas_attribut_piece[number] = value

                continue

            # -----------------------------------------
            # Attribute 112 - 113 - 114 - 115 - 169 - 171 - 1978 - 1979
            # -----------------------------------------

            # if number in attribut_val_defaut_ht:
            #     presence_ht = True
            #     datas_attribut_ht[number] = value
            #     continue

            # -----------------------------------------
            # Attribute 76 - 96 - 180 - 267
            # -----------------------------------------

            if number in formula_list_attributes:

                if self.allplan.version_allplan_current != "2022":
                    if len(re.findall(pattern=formula_piece_pattern, string=value)):
                        value = re.sub(pattern=formula_piece_pattern,
                                       repl=lambda m: formula_piece_dict.get(m.group(0)),
                                       string=value,
                                       flags=re.IGNORECASE)

                if self.region == self.allplan.langue:
                    value = self.allplan.formula_replace_all_name(formula=value)

                liste_autres.append([number, value])
                continue

            # -----------------------------------------
            # Attribute > 1999 & < 12000
            # -----------------------------------------

            try:
                number_int = int(number)

                if 1999 < number_int < 12000:

                    datas_attribute = self.allplan.attributes_dict.get(number, dict())

                    type_attribut = datas_attribute.get(code_attr_option, "")

                    if type_attribut not in [code_attr_formule_str, code_attr_formule_int, code_attr_formule_float]:
                        liste_autres.append([number, value])
                        continue

                    valeur_formule = datas_attribute.get(code_attr_value, "")

                    if self.allplan.version_allplan_current != "2022":
                        if len(re.findall(pattern=formula_piece_pattern, string=valeur_formule)):
                            valeur_formule = re.sub(pattern=formula_piece_pattern,
                                                    repl=lambda m: formula_piece_dict.get(m.group(0)),
                                                    string=valeur_formule,
                                                    flags=re.IGNORECASE)

                    liste_autres.append([number, valeur_formule])
                    continue

            except ValueError:
                pass

            # -----------------------------------------
            # Attribute Other
            # -----------------------------------------

            liste_autres.append([number, value])
            continue

        liste_defaut.sort(key=lambda x: int(x[0]))
        liste_autres.sort(key=lambda x: int(x[0]))

        # ==================================================================== #
        # QStandardItem Creation (Material / Component
        # ==================================================================== #

        if name == "":
            print("catalog_manage -- CatalogLoad --  attributes_add -- name est vide")
            return None

        if tag == "Group":

            material_renamed = name.upper() in self.material_upper_list

            if material_renamed:
                original_name = name

                name = find_new_title(name, self.material_upper_list)

                self.errors_list.append(f"{self.error_material_exist} '{qs_parent.text()}' : "
                                        f"'{original_name}' -->  {name}")

            qs_list = self.creation.material_line(value=name,
                                                  description=description,
                                                  used_by_links=self.link_used_count.get(name, 0))

            qs_current: QStandardItem = qs_list[0]

            self.material_upper_list.append(name.upper())
            self.material_list.append(name)

            if material_renamed:
                self.selected_list.append(qs_current)
                self.expanded_list.append(qs_current)

        elif tag == "Position":

            qs_list = self.creation.component_line(value=name,
                                                   description=description)

            qs_current: QStandardItem = qs_list[0]

        else:

            return None

        if element_display is not None:
            current_display = self.display_parameters_check(element_display, qs_current, tag)
        else:
            current_display = None

        # ==================================================================== #
        # Attribute Creation
        # ==================================================================== #

        # -----------------------------------------
        # Attribute 120  - 209 - 110
        # -----------------------------------------

        for number, value in liste_defaut:
            qs_current.appendRow(self.creation.attribute_line(value=value, number=number))

        # -----------------------------------------
        # Attribute 118 - 111 - 252 - 336 - 600
        # -----------------------------------------

        if presence_remplissage:

            type_remplissage = datas_attribut_remp.get("118", "0")

            if type_remplissage == "1":
                model_enumeration = self.allplan.model_haching
            elif type_remplissage == "2":
                model_enumeration = self.allplan.model_pattern
            elif type_remplissage == "3":
                model_enumeration = self.allplan.model_color
            elif type_remplissage == "5":
                model_enumeration = self.allplan.model_style
            elif type_remplissage == "6":
                model_enumeration = self.allplan.model_none
            else:
                model_enumeration = self.allplan.model_none
                datas_attribut_remp["111"] = "-1"
                datas_attribut_remp["252"] = "-1"
                datas_attribut_remp["336"] = ""
                datas_attribut_remp["600"] = "0"

            for number, value in datas_attribut_remp.items():

                if number == "111":
                    qs_current.appendRow(self.creation.attribute_line(value=value,
                                                                      number=number,
                                                                      model_enumeration=model_enumeration))
                    continue

                qs_current.appendRow(self.creation.attribute_line(value=value, number=number))

        # -----------------------------------------
        # Attribute 141 - 349 - 346 - 345 - 347
        # -----------------------------------------

        if presence_layer:
            for number, value in datas_attribut_layer.items():
                qs_current.appendRow(self.creation.attribute_line(value=value, number=number))
        # -----------------------------------------
        # Attribute 231 - 235 - 232 - 266 - 233 - 264
        # -----------------------------------------

        if presence_piece:

            for number, value in datas_attribut_piece.items():
                qs_current.appendRow(self.creation.attribute_line(value=value, number=number))

        # -----------------------------------------
        # Attributes Other
        # -----------------------------------------

        if len(liste_autres) != 0:
            for number, value in liste_autres:
                qs_current.appendRow(self.creation.attribute_line(value=value, number=number, formula_convert=False))

        if tag == "Group":
            self.catalog_load(qs_current, child, current_display)

        qs_parent.appendRow(qs_list)

        return

    def display_parameters_check(self, element_display, qs_current: QStandardItem, tag: str):

        if element_display is None:
            return None

        name = qs_current.text()

        search_child_display = catalog_xml_find_all(element=element_display,
                                                    tag=tag,
                                                    parameter="name",
                                                    value=name)

        search_count = len(search_child_display)

        child_display = None

        if search_count == 0:

            if tag != "Link":
                print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- search_child_display is None 0--> "
                      f"{tag} - {name}")

                return element_display

            search_child_display = catalog_xml_find_all(element=element_display,
                                                        tag="link",
                                                        parameter="name",
                                                        value=name)

            # search_child_display = element_display.findall(f'link[@name="{name}"]')

            search_count = len(search_child_display)

            if search_count == 0:
                print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- search_child_display is None 1--> "
                      f"{tag} - {name}")

                return element_display

            if search_count == 1:
                child_display = search_child_display[0]

            else:

                for element in search_child_display:
                    if element not in self.find_list:
                        child_display = element
                        break

                if child_display is None:
                    print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- "
                          f"search_child_display is None 2--> {tag} - {name}")
                    return element_display

                self.find_list.append(child_display)

        if search_count == 1:
            child_display = search_child_display[0]
        else:

            for element in search_child_display:
                if element not in self.find_list:
                    child_display = element
                    break

            if child_display is None:
                print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- search_child_display is None 2--> "
                      f"{tag} - {name}")
                return element_display

            self.find_list.append(child_display)

        name_display = child_display.get("name")

        if name_display is None:
            print(f"catalog_manage -- CatalogLoad -- display_parameters_check -- name_display is None")
            return element_display

        if tag == "Group":

            if child_display.get("expanded", child_display.get("deplier")) == "True":
                self.expanded_list.append(qs_current)

        if child_display.get("selected") == "True":
            self.selected_list.append(qs_current)

        return child_display

    def links_load(self, element):

        if "2022" in self.allplan.version_allplan_current:
            line_1 = self.tr("Ce catalogue utilise des liens et ne sont pas compatible avec Allplan 2022")
            line_2 = self.tr("Allplan 2022 refusera d'ouvrir ce catalogue.")

            msg(titre=application_title,
                message=f"{line_1}\n{line_2}",
                icone_critique=True)

        qs_folder_list = self.creation.folder_line(value=self.tr("Lien"), description="")

        qs_folder: Folder = qs_folder_list[0]

        link_orphan_find = False

        for child in element:

            name = child.get("name")

            if not isinstance(name, str):
                continue

            if name.upper() in self.material_with_link_list:
                continue

            search_link = catalog_xml_find_all(element=self.root,
                                               tag=".//Link",
                                               parameter="name",
                                               value=name)

            # search_link = self.root.findall(f'.//Link[@name="{name}"]')

            self.link_used_count[name] = len(search_link)

            # search_material = self.root.findall(f'.//Group//GroupDef//Attribute[@value="{name}"]')

            search_material = catalog_xml_find_all(element=self.root,
                                                   tag=".//Group//GroupDef//Attribute",
                                                   parameter="value",
                                                   value=name)

            results = [item.get("id") == "83" for item in search_material]

            if True not in results:
                link_orphan_find = True
                # used_by_links = self.root.findall(f'.//Link[@name="{name}"]')

                used_by_links = catalog_xml_find_all(element=self.root,
                                                     tag=".//Link",
                                                     parameter="name",
                                                     value=name)

                qs_material_list = self.creation.material_line(value=name,
                                                               description="",
                                                               used_by_links=used_by_links,
                                                               tooltips=True)

                qs_current: Material = qs_material_list[0]

                component_list = child.findall("Position")

                for component_child in component_list:
                    self.children_load(child=component_child,
                                       element_display=None,
                                       qs_parent=qs_current,
                                       tag="Position")

                qs_folder.appendRow(qs_material_list)

        if link_orphan_find:
            self.link_orphan = qs_folder_list

    @staticmethod
    def a___________________end___________________():
        pass


class CatalogSave(QObject):

    def __init__(self, asc, catalog, allplan, catalog_path="", catalog_setting_display_file=""):

        super().__init__()

        self.ui: Ui_MainWindow = asc.ui
        self.filtre: QSortFilterProxyModel = self.ui.hierarchy.model()

        self.allplan: AllplanDatas = allplan

        self.catalog: CatalogDatas = catalog

        self.model = self.catalog.cat_model

        self.qs_selection_list = self.catalog.get_qs_selection_list()

        self.qs_expanded_list = list()
        self.catalog.save_expand_qs_in_list_of(qs_parent=self.model.invisibleRootItem(),
                                               expanded_list=self.qs_expanded_list)

        self.link_list = list()

        # Informations path catalog

        self.catalog_path = self.catalog.catalog_path

        self.catalog_folder = self.catalog.catalog_folder
        self.catalog_name = self.catalog.catalog_name

        self.catalog_setting_display_file = self.catalog.catalog_setting_display_file

        self.define_paths(catalog_path=catalog_path, catalog_setting_display_file=catalog_setting_display_file)

        self.material_dict = dict()

        if not self.backup_catalogue():
            return

        self.sauvegarde_catalogue()

    def define_paths(self, catalog_path: str, catalog_setting_display_file: str):

        if not isinstance(catalog_path, str) or not isinstance(catalog_setting_display_file, str):
            return

        if catalog_path == "" or catalog_setting_display_file == "":
            return

        catalog_folder = find_folder_path(file_path=catalog_path)

        if catalog_folder == "":
            return

        catalog_name = find_filename(file_path=catalog_path)

        if catalog_name == "":
            return

        self.catalog_path = catalog_path

        self.catalog_folder = catalog_folder
        self.catalog_name = catalog_name

        self.catalog_setting_display_file = catalog_setting_display_file

    def backup_catalogue(self):

        catalog_folder_backup = f"{self.catalog_folder}backup\\"

        if self.catalog_folder == "" or self.catalog_name == "":
            return False

        if not make_backup(chemin_dossier=self.catalog_folder, fichier=self.catalog_name, extension=".xml",
                           dossier_sauvegarde=catalog_folder_backup, nouveau=False):
            return False

        nom_fichier = f"{self.catalog_name}_display"

        catalog_setting_folder = get_catalog_setting_folder(catalog_folder=self.catalog_folder)
        catalog_setting_folder_backup = f"{catalog_setting_folder}backup\\"

        if catalog_setting_folder == "" or nom_fichier == "":
            return False

        if not make_backup(chemin_dossier=catalog_setting_folder, fichier=nom_fichier, extension=".xml",
                           dossier_sauvegarde=catalog_setting_folder_backup, nouveau=False):
            return False

        return True

    def sauvegarde_catalogue(self):

        region = catalog_xml_region(self.allplan.langue)
        # version_xml = catalog_xml_version(self.allplan.version_allplan_current)
        version_xml = "1.0"
        date_modif = catalog_xml_date(self.allplan.langue)

        a = self.tr("Dernier enregistrement")

        root = etree.Element('AllplanCatalog',
                             Region=region,
                             version=version_xml)

        root.set("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation",
                 "../Xsd/AllplanCatalog.xsd")

        root_expand = etree.Element('Smart-Catalog')

        etree.SubElement(root, 'Node', name=f"------------------- {a} : {date_modif} ------------------- ")
        etree.SubElement(root_expand, 'Node', name=f"------------------- {a} : {date_modif} ------------------- ")

        self.sauvegarde_hierarchie(self.model.invisibleRootItem(), root, root_expand)

        if len(self.link_list) != 0:
            self.save_links(root)

        a = self.tr("Une erreur est survenue.")

        tps = time.perf_counter()

        # ------------------------------------------------
        # -------------------- Save catalog --------------
        # ------------------------------------------------

        try:

            catalogue_tree = etree.ElementTree(root)
            catalogue_tree.write(self.catalog_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

        except Exception as erreur:
            msg(titre=application_title,
                message=f'{a} : {self.catalog_path}',
                icone_critique=True,
                details=f"{erreur}")
            return False

        # ------------------------------------------------
        # -------------------- Save display --------------
        # ------------------------------------------------
        try:

            expand_tree = etree.ElementTree(root_expand)
            expand_tree.write(self.catalog_setting_display_file,
                              pretty_print=True,
                              xml_declaration=True,
                              encoding="UTF-8")

            print(f"catalogue save : {time.perf_counter() - tps}s")

            return True

        except Exception as erreur:

            msg(titre=application_title,
                message=f"{a} : {self.catalog_setting_display_file}",
                icone_avertissement=True,
                details=f"{erreur}")
            return False

    def save_links(self, root: etree._Element):

        self.link_list.sort()

        links = etree.Element("Links")
        root.insert(0, links)

        for material_name in self.link_list:

            linkdef = etree.Element("LinkDef", name=material_name)

            self.save_sub_links(material_name=material_name, linkdef=linkdef, sub_link_list=list())

            if len(linkdef) == 0:
                continue

            links.append(linkdef)

    def save_sub_links(self, material_name: str, linkdef: etree._Element, sub_link_list: list):

        qs_material: MyQstandardItem = self.material_dict.get(material_name, None)

        if not isinstance(qs_material, Material):
            print("catalog_manage -- CatalogSave -- save_sub_link -- not isinstance(qs_material, Material)")
            return

        material_name = qs_material.text()

        if material_name in sub_link_list:
            print("catalog_manage -- CatalogSave -- save_sub_link -- material_name in sub_link_list")
            return

        sub_link_list.append(material_name)

        if not qs_material.hasChildren():
            return

        for index_child in range(qs_material.rowCount()):

            qs_child: MyQstandardItem = qs_material.child(index_child, col_cat_value)

            if isinstance(qs_child, Component):
                self.new_component(item=qs_child, group=linkdef, affichage=None, selected=None)
                continue

            if isinstance(qs_child, Link):
                self.save_sub_links(material_name=qs_child.text(), linkdef=linkdef, sub_link_list=sub_link_list)
                continue

    def sauvegarde_hierarchie(self, item_parent: MyQstandardItem, racine: etree._Element, affichage: etree._Element):

        for index_row in range(item_parent.rowCount()):

            item = item_parent.child(index_row, col_cat_value)
            qs_desc = item_parent.child(index_row, col_cat_desc)

            if isinstance(item, Attribute):
                continue

            if not isinstance(qs_desc, Info):
                continue

            deplier = item in self.qs_expanded_list
            selected = item in self.qs_selection_list

            if isinstance(item, Folder):

                icone_dossier = item.icon_path
                node, node_aff = self.new_folder(item, racine, affichage, deplier, selected, icone_dossier,
                                                 qs_desc.text())

                if not item.hasChildren():
                    continue

                self.sauvegarde_hierarchie(item, node, node_aff)
                continue

            if isinstance(item, Material):
                group, node_aff = self.new_material(item, racine, affichage, deplier, selected)

                if not item.hasChildren():
                    continue

                self.sauvegarde_hierarchie(item, group, node_aff)
                continue

            elif isinstance(item, Component):
                self.new_component(item, racine, affichage, selected)
                continue

            elif isinstance(item, Link):
                self.new_link(item, racine, affichage, selected)
                continue

    @staticmethod
    def new_folder(item: QStandardItem, racine: etree._Element, affichage: etree._Element,
                   deplier: bool, selected: bool, icone_dossier=folder_icon, description=""):

        titre = item.text()
        if description == "":
            node = etree.SubElement(racine, "Node", name=titre)
        else:
            node = etree.SubElement(racine, "Node", name=f"{titre} -- {description}", comment=description)

        datas = dict()

        if deplier:
            datas["expanded"] = "True"

        if selected:
            datas["selected"] = "True"

        if icone_dossier.startswith(":/Images/") and icone_dossier != folder_icon:
            datas["icon"] = icone_dossier.replace(":/Images/", "")

        elif icons_old_path in icone_dossier:
            icone_name = icone_dossier.replace(icons_old_path, "")

            if icone_name in datas_icons:
                icone_name_tmp = datas_icons[icone_dossier]

                if os.path.exists(f"{icons_path}{icone_name_tmp}.png"):
                    datas["icon"] = icone_name_tmp
                else:
                    datas["icon"] = icone_dossier

            else:
                datas["icon"] = icone_dossier

        elif icons_path in icone_dossier:
            icone_dossier = icone_dossier.replace(icons_path, "")

            if icone_dossier in datas_icons:
                icone_dossier = datas_icons[icone_dossier]

            datas["icon"] = icone_dossier

        node_aff = etree.SubElement(affichage, "Node", name=titre, **datas)

        return node, node_aff

    def new_material(self, item: MyQstandardItem, node: etree._Element, affichage: etree._Element,
                     deplier: bool, selected: bool):

        material_name = item.text()

        if material_name in self.material_dict:
            material_name = find_new_title(base_title=material_name, titles_list=material_upper_list)
            print("catalog_manage -- CatalogSave -- creation_ouvrage -- Material already exists !!!")

        self.material_dict[material_name] = item

        # -----------

        group = etree.SubElement(node, "Group", name=material_name)

        group_def = etree.SubElement(group, 'GroupDef')

        self.new_attribute(item=item, definition=group_def)

        # -----------

        datas = dict()

        if deplier:
            datas["expanded"] = "True"

        if selected:
            datas["selected"] = "True"

        node_aff = etree.SubElement(affichage, "Group", name=material_name, **datas)

        return group, node_aff

    def new_component(self, item: MyQstandardItem, group: etree._Element, affichage: etree._Element,
                      selected: bool):

        component_name = item.text()

        position = etree.SubElement(group, "Position", name=component_name)

        position_def = etree.SubElement(position, 'PositionDef')

        self.new_attribute(item=item, definition=position_def)

        if affichage is None:
            return

        if selected:
            etree.SubElement(affichage, "Position", name=component_name, selected="True")
        else:
            etree.SubElement(affichage, "Position", name=component_name)

        return

    def new_link(self, item: MyQstandardItem, group: etree._Element, affichage: etree._Element, selected: bool):

        link_name = item.text()

        if link_name not in self.link_list:
            self.link_list.append(link_name)

        etree.SubElement(group, "Link", name=link_name)

        if affichage is None:
            return

        if selected:
            etree.SubElement(affichage, "Link", name=link_name, selected="True")
        else:
            etree.SubElement(affichage, "Link", name=link_name)

        return

    def new_attribute(self, item: MyQstandardItem, definition: etree._Element):

        # titre = item.text()

        etree.SubElement(definition, 'Attribute', id=attribute_default_base, value=item.text())

        nb_enfants = item.rowCount()
        plume = True
        trait = True
        couleur = True

        attributes_list = list()

        for index_row in range(nb_enfants):

            qstandarditem_enfant_valeur: QStandardItem = item.child(index_row, col_cat_value)

            if not isinstance(qstandarditem_enfant_valeur, Attribute):
                return

            qstandarditem_enfant_numero: QStandardItem = item.child(index_row, col_cat_number)
            valeur = qstandarditem_enfant_valeur.text()
            numero = qstandarditem_enfant_numero.text()

            if numero in liste_attributs_with_no_val_no_save and valeur == "":
                continue

            if numero in attributes_list:
                continue

            if numero == "349":
                plume, trait, couleur = self.layout_manage(valeur)

            if (numero == "346" and not plume) or (numero == "345" and not trait) or (numero == "347" and not couleur):
                continue

            type_ele2: str = self.allplan.find_datas_by_number(number=numero, key=code_attr_option)

            if type_ele2 == code_attr_combo_int:
                qstandarditem_enfant_combo: QStandardItem = item.child(index_row, col_cat_index)
                valeur = qstandarditem_enfant_combo.text()

                if not isinstance(valeur, str):
                    continue

                if valeur.startswith("0"):
                    try:

                        valeur_int = int(valeur)

                    except Exception:
                        continue

                    valeur = f"{valeur_int}"

                etree.SubElement(definition, 'Attribute', id=numero, value=valeur)
                attributes_list.append(numero)
                continue

            if type_ele2 in [code_attr_formule_str, code_attr_formule_int, code_attr_formule_float]:

                if "\n" in valeur:
                    valeur = valeur.replace("\n", "")

                try:
                    numero_int = int(numero)

                    if 1999 < numero_int < 12000:
                        valeur = "1"

                    else:

                        valeur = self.allplan.convertir_formule(valeur)

                except ValueError:
                    pass

                etree.SubElement(definition, 'Attribute', id=numero, value=valeur)
                attributes_list.append(numero)
                continue

            etree.SubElement(definition, 'Attribute', id=numero, value=valeur)
            attributes_list.append(numero)
        return

    @staticmethod
    def layout_manage(numero_style: str):

        plume = True
        trait = True
        couleur = True

        if numero_style == "1":
            plume = False
            return plume, trait, couleur

        if numero_style == "2":
            trait = False
            return plume, trait, couleur

        if numero_style == "3":
            plume = False
            trait = False
            return plume, trait, couleur

        if numero_style == "4":
            couleur = False
            return plume, trait, couleur

        if numero_style == "5":
            plume = False
            couleur = False
            return plume, trait, couleur

        if numero_style == "6":
            trait = False
            couleur = False
            return plume, trait, couleur

        if numero_style == "7":
            plume = False
            trait = False
            couleur = False
            return plume, trait, couleur

        return plume, trait, couleur

    @staticmethod
    def a___________________end___________________():
        pass


class SpecialFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.search_number = ""
        self.search_type = ""

    def set_custom_filter(self, search_number: str, search_type: str) -> None:

        if not isinstance(search_number, str) or not isinstance(search_type, str):
            self.search_number = ""
            self.search_type = ""
            return

        self.search_type = search_type
        self.search_number = search_number

    def clear_custom_filter(self) -> None:
        self.search_number = ""
        self.search_type = ""

    def active_custom_filter(self) -> bool:
        return self.search_number != "" or self.search_type != ""

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex):

        if self.filterRegExp().isEmpty():
            return True

        model = self.sourceModel()

        if model is None:
            return False

        # ----------
        # Value
        # ----------

        qm_value = model.index(source_row, self.filterKeyColumn(), source_parent)

        if not isinstance(qm_value, QModelIndex):
            return False

        current_value = qm_value.data(self.filterRole())

        if not isinstance(current_value, str):
            return False

        reg_exp = self.filterRegExp()

        valid_text = reg_exp.indexIn(current_value) >= 0

        if self.search_number == "" and self.search_type == "":
            return valid_text

        if not valid_text:
            # print(f"False - None - None --> Value : {current_value} isn't valid ({reg_exp})")
            return False

        # ----------
        # Type
        # ----------

        if self.search_type != "":

            qm_type = model.index(source_row, col_cat_value, source_parent)

            if not isinstance(qm_type, QModelIndex):
                return False

            current_type = qm_type.data(user_data_type)

            # If attribute -> get parent_type
            if current_type == attribute_code:
                qm_type = qm_type.parent()

                if not isinstance(qm_type, QModelIndex):
                    return False

                current_type = qm_type.data(user_data_type)

            regex_type = QRegExp(self.search_type, Qt.CaseInsensitive)

            if regex_type.indexIn(current_type) < 0:
                # print(f"True - False - None --> Value : {current_value} is valid ({reg_exp}) but "
                #       f"type : {current_type} isn't valid {self.search_type}")
                return False

        # else:
        #     current_type = ""

        # ----------
        # Number
        # ----------

        if self.search_number == "":
            return True

        qm_number = model.index(source_row, col_cat_number, source_parent)

        if not isinstance(qm_number, QModelIndex):
            return False

        current_number = qm_number.data()

        valid_number = current_number == self.search_number

        # if not valid_number:
        #     print(f"True - True - False --> Value : {current_value} is valid ({reg_exp}) and "
        #           f"number : {current_number} isn't valid ({self.search_number})")
        #
        # else:
        #
        #     print(f"True - True - True --> Value : {current_value} is valid ({reg_exp}) and "
        #           f"number : {current_number} is valid ({self.search_number})")

        return valid_number

    @staticmethod
    def a___________________end___________________():
        pass
