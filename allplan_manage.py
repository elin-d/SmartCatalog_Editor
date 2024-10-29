#!/usr/bin/python3
# -*- coding: utf-8 -*
import glob
import os.path
import sqlite3
from pathlib import Path

from lxml import etree

from hierarchy_qs import *
from main_datas import *
from tools import afficher_message as msg, read_file_to_list
from tools import qstandarditem_font, get_look_qs, read_zt_file, convert_list_attribute_number
from tools import settings_get, settings_read, get_value_is_valid, settings_list, format_float_value
from tools import validation_fichier_xml, qm_check, registry_find_value


class AllplanDatas(QObject):
    autocompletion_refresh_signal = pyqtSignal()

    def __init__(self, langue: str):
        super().__init__()

        self.creation = Creation(self)

        # -------------

        self.version_allplan_current = str()
        self.allplan_paths = None

        self.versions_list = list()
        self.version_datas = dict()

        # -------------

        self.icon_list = list()
        self.recent_icons_list = list()

        self.langue = langue

        # -------------
        # Dafalt Paths
        # -------------

        self.etc_default_folder = str()
        self.etc_xml_defalut_folder = str()

        self.catalog_default_folder = str()
        self.catlog_default_file_path = str()

        self.asw_folder = str()

        # ------------- 18358 ----

        self.allplan_18358_dict = dict()

        # -------------
        # File Paths
        # -------------

        self.unit_file_path = f"{asc_settings_path}{unit_list_file}.ini"

        # -------------
        # Current Paths
        # -------------

        self.catalog_user_path = str()
        self.user_attributes_xml_path = str()

        # -------------
        # Function datas
        # -------------

        self.functions_excel_dict = dict()
        self.functions_python_dict = dict()
        self.functions_vbs_dict = dict()

        # ---------------------------------------
        # brackets
        # ---------------------------------------

        self.formula_color = settings_get(app_setting_file, "brackets_color_on")

        self.piece_remplace = dict()

        self.tooltips_remplace = dict()

        self.fonction_replace = dict()

        # -------------
        # models
        # -------------

        self.model_ifc = QStandardItemModel()
        self.model_layers_view = QStandardItemModel()
        self.model_layers = QStandardItemModel()

        self.model_line = QStandardItemModel()
        self.model_pen = QStandardItemModel()
        self.model_color = QStandardItemModel()
        self.model_haching = QStandardItemModel()
        self.model_pattern = QStandardItemModel()
        self.model_none = QStandardItemModel()
        self.model_none.appendRow([QStandardItem("-1"), QStandardItem("")])

        self.model_style = QStandardItemModel()
        self.model_style_view = QStandardItemModel()

        self.model_units_default = QStandardItemModel()
        self.model_units = QStandardItemModel()

        self.model_231 = QStandardItemModel()

        self.model_232 = QStandardItemModel()

        self.model_233 = QStandardItemModel()

        self.model_235 = QStandardItemModel()

        self.model_339 = QStandardItemModel()

        # self.model_18313 = QStandardItemModel()
        self.model_18358 = QStandardItemModel()

        self.surface_list = list()
        self.surface_all_list = list()
        self.surface_recent_list = list()

        self.attribute_name_list = list()
        self.conversions_dict = dict()
        self.attribute_group_list = list()

        self.attribute_model = QStandardItemModel()

        self.model_autocompletion = QStandardItemModel()

        self.model_defaults = QStandardItemModel()

        self.attributes_dict = dict()

        self.aim_dict = dict()
        self.aim_get_attributes()

        self.formula_dict = dict()

        self.pattern = str()

        self.enumeration_translations = dict()

        # -------------
        # favoris
        # -------------
        self.material_favorite_list = list()
        self.component_favorite_list = list()
        self.formula_favorite_list = list()

        # -------------
        # groupe
        # -------------

        self.group_list = dict()

        self.group_save_dict = dict()

        self.chargement_versions()
        self.chargements_attributs_fixes()

    def allplan_retranslate(self):

        self.piece_remplace = {"MT_Boden": QCoreApplication.translate("Allplan", "Fonction_Surface_sol"),
                               "Obj_Floor": QCoreApplication.translate("Allplan", "Fonction_Surface_sol"),
                               "MT_Decke": QCoreApplication.translate("Allplan", "Fonction_Surface_Plafond"),
                               "Obj_Ceiling": QCoreApplication.translate("Allplan", "Fonction_Surface_Plafond"),
                               "MT_Seite": QCoreApplication.translate("Allplan", "Fonction_Surface_mur"),
                               "Obj_VSurface": QCoreApplication.translate("Allplan", "Fonction_Surface_mur"),
                               "MT_Leiste": QCoreApplication.translate("Allplan", "Fonction_Surface_plinthe"),
                               "Obj_Baseboard": QCoreApplication.translate("Allplan", "Fonction_Surface_plinthe"),
                               "MT_Material": QCoreApplication.translate("Allplan",
                                                                         "Fonction_Matériaux_Supplémentaires"),
                               "Obj_Material": QCoreApplication.translate("Allplan",
                                                                          "Fonction_Matériaux_Supplémentaires")}

        self.tooltips_remplace = {"=": " = ",
                                  "+": " + ",
                                  "-": " - ",
                                  "*": " * ",
                                  "/": " / ",
                                  ">": " > ",
                                  ">=": " >= ",
                                  "<": " < ",
                                  "<=": " <= ",
                                  "&": " " + QCoreApplication.translate("Allplan", "et") + " ",
                                  "|": " " + QCoreApplication.translate("Allplan", "ou") + " ",
                                  "(": " ( ",
                                  ")": " ) ",
                                  ";": " ; ",
                                  "!": " " + QCoreApplication.translate("Allplan", "non") + " "}

        self.fonction_replace = {"ABS": '<i>' +
                                        QCoreApplication.translate("Allplan", "Valeur absolue") +
                                        '</i> (',

                                 "SQRT": '<i>' +
                                         QCoreApplication.translate("Allplan", "Racine carrée") +
                                         '</i> (',

                                 "SQR": '<i>' +
                                        QCoreApplication.translate("Allplan", "Racine carrée") +
                                        '</i> (',

                                 "NINT": '<i>' +
                                         QCoreApplication.translate("Allplan", "Arrondi entier plus proche") +
                                         '</i> (',

                                 "INT": '<i>' +
                                        QCoreApplication.translate("Allplan", "Arrondi entier inférieur") +
                                        '</i> (',

                                 "CEIL": '<i>' +
                                         QCoreApplication.translate("Allplan", "Arrondi entier supérieur") +
                                         '</i> (',

                                 "VALUE": '<i>' +
                                          QCoreApplication.translate("Allplan", "Valeur du texte") +
                                          '</i> (',

                                 "ROUND": '<i>' +
                                          QCoreApplication.translate("Allplan", "Arrondi décimal") +
                                          '</i> ('}

    @staticmethod
    def a___________________allplan_chargement_donnees______():
        pass

    def get_all_registry_path(self, registry_path: str) -> None:

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path)

            datas = winreg.QueryInfoKey(key)

        except Exception as error:
            print(f"allplan_manage -- AllplanDatas -- get_all_registry_path -- error 1 : {error}")
            return

        except FileNotFoundError as error:
            print(f"allplan_manage -- AllplanDatas -- get_all_registry_path -- error 2 : {error}")
            return

        if len(datas) != 3:
            print("allplan_manage -- AllplanDatas -- get_all_registry_path -- len(datas) != 3")
            return

        datas_count = datas[0]

        if not isinstance(datas_count, int):
            print("allplan_manage -- AllplanDatas -- get_all_registry_path -- not isinstance(datas_count, int)")
            return

        if datas_count == 0:
            return

        for i in range(datas_count):

            try:
                name = winreg.EnumKey(key, i)

                new_path = f"{registry_path}\\{name}"

                if name != "InstallRoot":
                    self.get_all_registry_path(registry_path=new_path)
                    continue

                if not registry_path.endswith(".0"):
                    return

                allplan_version, allplan_version_name = self.registry_version_extractor(registry_path)

                if allplan_version == "":
                    return

                new_version = AllplanPaths(allplan_version=allplan_version,
                                           allplan_version_name=allplan_version_name,
                                           installroot_path=new_path)

                if new_version.bad_config:
                    print("allplan_manage -- AllplanDatas -- get_all_registry_path -- new_version.bad_config")
                    continue

                self.version_datas[allplan_version_name] = new_version
                return

            except Exception as error:
                print(f"allplan_manage -- AllplanDatas -- get_all_registry_path -- error 3 : {error}")
                continue

            except FileNotFoundError as error:
                print(f"allplan_manage -- AllplanDatas -- get_all_registry_path -- error 4 : {error}")
                continue

        return

    def registry_version_extractor(self, text: str) -> tuple:

        if not isinstance(text, str):
            print("allplan_manage -- AllplanDatas -- registry_version_extractor -- not isinstance(text, str)")
            return "", ""

        match = re.search(r'\\(\d+)\.0', text)

        if not match:
            print("allplan_manage -- AllplanDatas -- registry_version_extractor -- not match")
            return "", ""

        text_version = match.group(1)

        try:
            version_int = int(text_version)

            if version_int != 99 and version_int < first_allplan_version_int:
                return "", ""

        except Exception as error:
            print(f"allplan_manage -- AllplanDatas -- registry_version_extractor -- error : {error}")
            return "", ""

        if "verification" not in text.lower():

            if text_version not in self.versions_list:
                return text_version, text_version

            for i in range(10):
                if f"{text_version} ({i})" in self.versions_list:
                    return text_version, f"{text_version} ({i})"

            print(f"allplan_manage -- AllplanDatas -- registry_version_extractor -- match new name version error")
            return "", ""

        if f"{text_version}_verif" not in self.versions_list:
            return text_version, f"{text_version}_verif"

        for i in range(10):
            if f"{text_version}_verif ({i})" in self.versions_list:
                return text_version, f"{text_version}_verif ({i})"

            print(f"allplan_manage -- AllplanDatas -- registry_version_extractor -- match new name version verif error")
            return "", ""

        print(f"allplan_manage -- AllplanDatas -- registry_version_extractor -- no match version")
        return "", ""

    def find_allplan_version_by_prj_path(self, file_path: str) -> str:

        if not isinstance(file_path, str):
            return ""

        if not os.path.exists(file_path):
            return ""

        for version_name, version_obj in self.version_datas.items():

            if not isinstance(version_obj, AllplanPaths):
                continue

            prj_path = version_obj.prj_path

            if prj_path.lower() in file_path.lower():
                return version_name

        return ""

    @staticmethod
    def a___________________allplan_loading_datas______():
        pass

    def chargement_versions(self):

        self.get_all_registry_path(registry_path="SOFTWARE\\NEMETSCHEK")

        self.versions_list = list(self.version_datas.keys())

        if len(self.versions_list) == 0:
            print("recherche_donnees_allplan -- Aucune version d'Allplan trouvée - liste versions vide")

            msg(titre=application_title,
                message=self.tr("Aucune version d'Allplan n'a pu être trouvée."),
                icone_critique=True)

            sys.exit()

        self.versions_list.sort(reverse=True)

        # todo à revoir

        for version_obj in reversed(self.version_datas.values()):

            if not isinstance(version_obj, AllplanPaths):
                continue

            etc_cat_path = version_obj.etc_cat_path

            if self.langue == "FR" and os.path.exists(f"{etc_cat_path}CMI.xml"):
                cat_path = f"{etc_cat_path}CMI.xml"

            elif os.path.exists(f'{etc_cat_path}Allplan_{self.langue}.xml'):

                cat_path = f'{etc_cat_path}Allplan_{self.langue}.xml'

            else:

                cat_path = f'{etc_cat_path}Allplan.xml'

            if os.path.exists(cat_path) and version_obj.allplan_version == "99" and len(self.versions_list) == 1:
                self.etc_default_folder = version_obj.etc_path
                self.etc_xml_defalut_folder = version_obj.etc_xml_path
                self.catalog_default_folder = version_obj.std_cat_path
                self.catlog_default_file_path = cat_path
                break

            elif os.path.exists(cat_path) and version_obj.allplan_version != "99":
                self.etc_default_folder = version_obj.etc_path
                self.etc_xml_defalut_folder = version_obj.etc_xml_path
                self.catalog_default_folder = version_obj.std_cat_path
                self.catlog_default_file_path = cat_path
                break

    def load_all_paths(self) -> bool:
        """
        Permet de récupérer les chemins d'allplan
        : return: Retourne False si le chargement a échoué sinon True
        """

        allplan_paths = self.version_datas.get(self.version_allplan_current, None)

        if not isinstance(allplan_paths, AllplanPaths):
            print("allplan_manage -- load_all_paths -- not isinstance(allplan_paths, AllplanVersion)")
            return False

        self.allplan_paths = allplan_paths

        self.etc_default_folder = self.allplan_paths.etc_path
        self.etc_xml_defalut_folder = self.allplan_paths.etc_xml_path
        self.catalog_default_folder = self.allplan_paths.std_cat_path

        self.asw_folder = str()

        asw_folder = f"{self.catalog_user_path}asw\\"

        if os.path.exists(asw_folder):
            self.asw_folder = asw_folder
        else:
            asw_folder = self.allplan_paths.std_asw_path

            if os.path.exists(asw_folder):
                self.asw_folder = asw_folder

        print("allplan_manage -- chargement_chemins --------------------\n"
              f"dossier_etc ==> {self.allplan_paths.etc_path}\n"
              f"dossier_etc_xml ==> {self.allplan_paths.etc_xml_path}\n"
              f"dossier_etc_cat ==> {self.allplan_paths.std_cat_path}\n"
              f"dossier_std ==> {self.allplan_paths.std_path}\n"
              f"dossier_std_xml ==> {self.allplan_paths.std_xml_path}\n"
              f"dossier_std_cat ==> {self.allplan_paths.std_cat_path}\n"
              f"dossier_prj ==> {self.allplan_paths.prj_path}\n"
              f"dossier_prg ==> {self.allplan_paths.prg_path}\n"
              f"dossier_asw ==> {self.asw_folder}\n"
              f"-------------------------------------")

        return True

    def verification_version(self, version_allplan: str, choisir=True) -> str:

        if version_allplan is None:
            return self.choisir_version_defaut(choisir)

        if version_allplan == "":
            print(f"allplan_definir_version -- le nom de la version est vide")
            return self.choisir_version_defaut(choisir)

        try:

            version_int = int(version_allplan)

            if version_int != 99 and version_int < first_allplan_version_int:
                return self.choisir_version_defaut(choisir)

        except Exception:
            return self.choisir_version_defaut(choisir)

        if version_allplan not in self.versions_list:
            return self.choisir_version_defaut(choisir)

        return version_allplan

    def choisir_version_defaut(self, choisir: bool) -> str:

        if len(self.versions_list) == 0:

            if choisir:
                self.version_allplan_current = ""

            return ""

        if choisir:
            self.version_allplan_current = self.versions_list[-1]

        return self.version_allplan_current

    @staticmethod
    def a___________________model_attributs______():
        pass

    def chargements_attributs_fixes(self):

        # ---------------------------------------
        # CHARGEMENT données application
        # ---------------------------------------

        self.favorite_loading()
        self.allplan_color_loading()

    def allplan_loading(self):

        self.model_defaults.clear()

        self.load_all_paths()

        self.creation.attributes_datas.clear()
        self.creation.formula_datas.clear()

        # ---------------------------------------
        # CHARGEMENT model hachurages / Motifs / Style de lignes
        # ---------------------------------------

        self.allplan_layer_loading()
        self.allplan_pen_loading()
        self.allplan_line_loading()

        self.allplan_pattern_loading()
        self.allplan_haching_loading()
        self.allplan_style_loading()

        # ---------------------------------------
        # CHARGEMENT CHEMIN FICHIERS ATTRIBUTS
        # ---------------------------------------

        self.allplan_ifc_loading()
        self.allplan_group_loading()

        self.allplan_unit_loading()

        self.allplan_231_loading()
        self.allplan_232_loading()
        self.allplan_233_loading()
        self.allplan_235_loading()
        self.allplan_339_loading()
        # self.allplan_18313_loading()
        self.allplan_18358_loading()

        self.allplan_attributes_loading()

        self.get_excel_functions()
        self.get_python_functions()
        self.get_vbs_functions()

        self.allplan_obj_names_loading()

        self.autocompletion_pattern_creation()
        self.autocompletion_loading()

    def allplan_attributes_loading(self):

        if not isinstance(self.allplan_paths, AllplanPaths):
            return

        # ------------------
        # Variables clear
        # ------------------

        self.attribute_name_list = list()
        self.conversions_dict = dict()

        self.attribute_model.clear()
        self.attribute_model.setHorizontalHeaderLabels([self.tr('Numéro'), self.tr('Nom'), "", ""])

        self.attributes_dict = dict()

        language_ext_list = [f"_{extension.lower()}.xml" for extension in language_extension_3.keys()]

        language_ext_list.insert(1, ".xml")

        # ------------------
        # ETC attributes - search
        # ------------------

        files_list = glob.glob(f'{self.allplan_paths.etc_xml_path}*AttributeDefinitionCollection*.xml')

        if len(files_list) == 0:
            return

        file_names_list = ["LocalLayoutAttributeDefinition"]

        suffix_list = [f"_{extension.lower()}" for extension in language_extension_3.keys()]
        suffix_list.insert(0, self.allplan_paths.etc_xml_path)
        suffix_list.insert(1, ".xml")

        for file_name in files_list:
            for suffix in suffix_list:
                file_name = file_name.replace(suffix, "")

            if file_name not in file_names_list:
                file_names_list.append(file_name)

        if len(file_names_list) == 0:
            return

        file_names_list.sort()

        # ------------------
        # ETC attributes load
        # ------------------

        for nom_fichier in file_names_list:

            if self.langue in dict_langues:

                extension = dict_langues[self.langue]
                chemin_fichier = f"{self.allplan_paths.etc_xml_path}{nom_fichier}{extension}"

                if os.path.exists(chemin_fichier):
                    self.allplan_attribute_xml_to_model(chemin_fichier)
                    continue

            for extension in language_ext_list:

                chemin_fichier = f"{self.allplan_paths.etc_xml_path}{nom_fichier}{extension}"

                if os.path.exists(chemin_fichier):
                    self.allplan_attribute_xml_to_model(chemin_fichier)
                    break

        # ------------------
        # User attributes load
        # ------------------

        if os.path.exists(self.user_attributes_xml_path):
            self.allplan_attribute_xml_to_model(self.user_attributes_xml_path)

        # ------------------
        # STD attributes - search
        # ------------------

        if not os.path.exists(self.allplan_paths.std_xml_path):
            return

        files_list = glob.glob(f'{self.allplan_paths.std_xml_path}AttributeDefinitionCollection*.xml')

        if len(files_list) == 0:
            return

        file_names_list = list()
        suffix_list[0] = self.allplan_paths.std_xml_path

        for file_name in files_list:

            for suffix in suffix_list:
                file_name = file_name.replace(suffix, "")

            if file_name not in file_names_list and file_name != "AttributeDefinitionCollectionLocal":
                file_names_list.append(file_name)

        if len(file_names_list) == 0:
            return

        # ------------------
        # STD attributes - load
        # ------------------

        for file_name in file_names_list:

            file_path = f"{self.allplan_paths.std_xml_path}{file_name}.xml"

            if os.path.exists(file_path):
                self.allplan_attribute_xml_to_model(file_path)
                continue

            if self.langue in dict_langues:

                extension = dict_langues[self.langue]
                file_path = f"{self.allplan_paths.std_xml_path}{file_name}{extension}"

                if os.path.exists(file_path):
                    self.allplan_attribute_xml_to_model(file_path)
                    continue

            for extension in language_ext_list:

                file_path = f"{self.allplan_paths.std_xml_path}{file_name}{extension}"

                if os.path.exists(file_path):
                    self.allplan_attribute_xml_to_model(file_path)
                    break

    def autocompletion_pattern_creation(self):

        print("gestion_allplan -- creation_pattern")

        self.attribute_name_list.sort(key=len, reverse=True)
        self.pattern = ""r'\b({})\b'.format('|'.join(self.attribute_name_list))

    def autocompletion_loading(self):

        self.model_autocompletion.clear()

        print("gestion_allplan -- chargement_autocompletion")

        liste_base = [['_IF_(', '_IF_('], ['_ELSE_', '_ELSE_'], ['_ELSE_(', '_ELSE_('], ['_ELSE__IF_(', '_ELSE__IF_(']]

        liste_fonc = [['ABS(', 'ABS('], ['SQRT(', 'SQRT('], ['SQR(', 'SQR('], ['PI', 'PI'], ['LN(', 'LN('],
                      ['LOG(', 'LOG('], ['RCP(', 'RCP('], ['EXP(', 'EXP('], ['SGN(', 'SGN('],
                      ['SIN(', 'SIN('], ['COS(', 'COS('], ['TAN(', 'TAN('],
                      ['ACOS(', 'ACOS('], ['ASIN(', 'ASIN('], ['ATAN(', 'ATAN('],
                      ['COSH(', 'COSH('], ['SINH(', 'SINH('], ['TANH(', 'TANH('],

                      ['NINT(', 'NINT('], ['INT(', 'INT('], ['CEIL(', 'CEIL('],

                      ['GRA(', 'GRA('], ['RAD(', 'RAD('], ['GON(', 'GON('], ['RAG(', 'RAG('],
                      ['AVG(', 'AVG('], ['MIN(', 'MIN('], ['MAX(', 'MAX('],

                      ['FLAG(', 'FLAG('], ['ROUND(', 'ROUND('], ['ELE(', 'ELE('], ['VALUE(', 'VALUE('],
                      ['MID(', 'MID('], ['FORMAT(', 'FORMAT('],

                      ['PARENT(', 'PARENT('], ['CHILD(', 'CHILD('], ['GROUP(', 'GROUP('],

                      ['Obj_Floor(', self.tr('Revêtement de sol')],
                      ['Obj_Ceiling(', self.tr('Surface Plafond')],
                      ['Obj_VSurface(', self.tr('Surface mur')],
                      ['Obj_Baseboard(', self.tr('Plinthe')],
                      ['Obj_Material(', self.tr('Matériaux supplémentaires')],

                      ['Obj_WindowOpening(', 'Obj_WindowOpening('],
                      ['Obj_FrenchWindowOpening(', 'Obj_FrenchWindowOpening('],
                      ['Obj_Roof_Opening(', 'Obj_Roof_Opening('],
                      ['Obj_DoorOpening(', 'Obj_DoorOpening('],
                      ['Obj_Niche(', 'Obj_Niche('],
                      ['Obj_Wall(', 'Obj_Wall('],
                      ['Obj_Room(', 'Obj_Room('],
                      ['Obj_Column(', 'Obj_Column('],
                      ['Obj_WindowSmartSymbol(', 'Obj_WindowSmartSymbol('],
                      ['Obj_DoorSmartSymbol(', 'Obj_DoorSmartSymbol('],
                      ['Obj_RoofWindow(', 'Obj_RoofWindow('],
                      ['Obj_Window(', 'Obj_Window('],
                      ['Obj_Door(', 'Obj_Door('],
                      ['Obj_Roof(', 'Obj_Roof('],
                      ['Obj_RoofLayer(', 'Obj_RoofLayer('],

                      ['TOPOLOGY(', 'TOPOLOGY('],

                      ['PARENTPRECAST(', 'PARENTPRECAST('],
                      ['IMPRRE(', 'PARENTPRECAST('],
                      ['FIXTURECOUNT(', 'FIXTURECOUNT('],
                      ['PARENTPRECAST(', 'PARENTPRECAST('],

                      ['@OBJ@', '@OBJ@'], ['@VOB@', '@VOB@'],

                      [self.tr("SOMME"), self.tr("SOMME")]]

        liste_attributs = list()
        liste_favoris_ouvrage = list()
        liste_favoris_composant = list()
        liste_favoris_formule = list()

        for index_model in range(self.attribute_model.rowCount()):
            number: str = self.attribute_model.index(index_model, col_attr_number).data()
            name = self.attribute_model.index(index_model, col_attr_name).data()

            if number is None or name is None:
                print("gestion_allplan -- chargement_autocompletion -- erreur dans model -> "
                      "numero is None & nom is None")
                continue

            numero_formater = f"@{number}@"

            if number in self.formula_favorite_list:

                liste_favoris_formule.append([name, numero_formater])
                liste_favoris_formule.append([numero_formater, name])

            elif number in self.material_favorite_list:

                liste_favoris_ouvrage.append([name, numero_formater])
                liste_favoris_ouvrage.append([numero_formater, name])

            elif number in self.component_favorite_list:

                liste_favoris_composant.append([name, numero_formater])
                liste_favoris_composant.append([numero_formater, name])

            else:

                liste_attributs.append([name, numero_formater])
                liste_attributs.append([numero_formater, name])

        liste_attributs = sorted(liste_attributs, key=lambda x: len(x[0]))
        liste_favoris_ouvrage = sorted(liste_favoris_ouvrage, key=lambda x: len(x[0]))
        liste_favoris_composant = sorted(liste_favoris_composant, key=lambda x: len(x[0]))
        liste_favoris_formule = sorted(liste_favoris_formule, key=lambda x: len(x[0]))

        liste_final = (liste_base + liste_favoris_formule + liste_favoris_ouvrage + liste_favoris_composant +
                       liste_fonc + liste_attributs)

        for sous_liste in liste_final:
            qs = QStandardItem(sous_liste[0])
            get_look_qs(qs)

            qs2 = QStandardItem(sous_liste[1])
            get_look_qs(qs2)

            self.model_autocompletion.appendRow([qs, qs2])

        # ---------------

        function_txt = self.tr("Fonction Excel")
        argument_txt = self.tr("Argument")
        detail_txt = self.tr("Détail de la fonction")

        for function_name, function_data in self.functions_excel_dict.items():

            if not isinstance(function_name, str) and not isinstance(function_data, dict):
                continue

            function_args = function_data.get("args", "")
            function_detail = function_data.get("content", "")

            tooltip = ("<p style='white-space:pre'>"
                       f"{function_txt} : <b>{function_name}</b><br>"
                       f"{argument_txt} : <b>{function_args}</b><br>"
                       f"{detail_txt} : <br><br><b>{function_detail}</b>")

            qs = QStandardItem(f"x: {function_name}(")
            qs.setToolTip(tooltip)
            get_look_qs(qs)

            qs2 = QStandardItem(f"x: {function_name}(")
            qs2.setToolTip(tooltip)
            get_look_qs(qs2)

            self.model_autocompletion.appendRow([qs, qs2])

        # ---------------

        function_txt = self.tr("Fonction Python")

        for function_name, function_data in self.functions_python_dict.items():

            if not isinstance(function_name, str) and not isinstance(function_data, dict):
                continue

            function_args = function_data.get("args", "")
            function_detail = function_data.get("content", "")

            tooltip = ("<p style='white-space:pre'>"
                       f"{function_txt} : <b>{function_name}</b><br>"
                       f"{argument_txt} : <b>{function_args}</b><br>"
                       f"{detail_txt} : <br><br><b>{function_detail}</b>")

            qs = QStandardItem(f"p: {function_name}(")
            qs.setToolTip(tooltip)
            get_look_qs(qs)

            qs2 = QStandardItem(f"p: {function_name}(")
            qs2.setToolTip(tooltip)
            get_look_qs(qs2)

            self.model_autocompletion.appendRow([qs, qs2])

        # ---------------

        function_txt = self.tr("Fonction VBS")

        for function_name, function_data in self.functions_vbs_dict.items():

            if not isinstance(function_name, str) and not isinstance(function_data, dict):
                continue

            function_args = function_data.get("args", "")
            function_detail = function_data.get("content", "")

            tooltip = ("<p style='white-space:pre'>"
                       f"{function_txt} : <b>{function_name}</b><br>"
                       f"{argument_txt} : <b>{function_args}</b><br>"
                       f"{detail_txt} : <br><br><b>{function_detail}</b>")

            qs = QStandardItem(f"v: {function_name}(")
            qs.setToolTip(tooltip)
            get_look_qs(qs)

            qs2 = QStandardItem(f"v: {function_name}(")
            qs2.setToolTip(tooltip)
            get_look_qs(qs2)

            self.model_autocompletion.appendRow([qs, qs2])

        self.model_autocompletion.setHorizontalHeaderLabels(["", ""])

    def allplan_data_clear(self):

        print("gestion_allplan -- nettoyage_datas")

        self.attribute_name_list = list()
        self.conversions_dict = dict()

        self.attribute_model.clear()
        self.attribute_model.setHorizontalHeaderLabels([self.tr('Numéro'), self.tr('Nom'), "", ""])

        self.attributes_dict = dict()

        self.pattern = str()

    @staticmethod
    def a___________________chargement_fichiers______():
        pass

    def allplan_group_loading(self):

        self.group_list = {"ATTR_PRG_BEREICH_BENUTZER": self.tr("Attribut utilisateur"),
                           "ATTR_PRG_BEREICH_MENGEN": self.tr("Architecture - quantités"),
                           "ATTR_PRG_BEREICH_ALLGEMEIN": self.tr("Généralité"),
                           "ATTR_PRG_BEREICH_ARCHALLG": self.tr("Architecture générale"),
                           "ATTR_PRG_BEREICH_PLANHISTORY": self.tr("Index de plan"),
                           "ATTR_PRG_BEREICH_RAUMTECH": "Inconnu 0",
                           "ATTR_PRG_BEREICH_DIN277": self.tr("DIN 277, surface habitable, BauNVO"),
                           "ATTR_PRG_BEREICH_TEILBILD": self.tr("Calque"),
                           "ATTR_PRG_BEREICH_ING": self.tr("Ingénierie"),
                           "ATTR_PRG_BEREICH_ALLFA": "Alfa sync",
                           "ATTR_PRG_BEREICH_ARCHINT": "Architecture interne",
                           "ATTR_PRG_BEREICH_LANDBAU": self.tr("Aménagement du paysage"),
                           "ATTR_PRG_BEREICH_STADT": self.tr("Urbanisme"),
                           "ATTR_PRG_BEREICH_WAERME": self.tr("Isolation thermique"),
                           "ATTR_PRG_BEREICH_PLAN": self.tr("Plan"),
                           "ATTR_PRG_BEREICH_ARCHSPEZ": self.tr("Architecture - spéciale"),
                           "ATTR_PRG_BEREICH_PROJEKT": self.tr("Projet"),
                           "ATTR_PRG_BEREICH_DGM": self.tr("Modeleur de terrain 3D"),
                           "ATTR_PRG_BEREICH_DACHHAUT": self.tr("Architecture - couverture toit"),
                           "ATTR_PRG_BEREICH_INTVERL": self.tr("Répartitions intelligentes"),
                           "ATTR_PRG_BEREICH_EINBAUTEIL": self.tr("Inserts"),
                           "ATTR_PRG_BEREICH_FERTIGTEIL_D": self.tr("Éléments de structure préfa divers"),
                           "ATTR_PRG_BEREICH_TGA_HEIZUNG": self.tr("Fluides-Chauffage"),
                           "ATTR_PRG_BEREICH_TGA_LUEFTUNG": self.tr("Fluides-Ventilation"),
                           "ATTR_PRG_BEREICH_TGA_ELEKTRO": self.tr("Fluides-Electricité"),
                           "ATTR_PRG_BEREICH_TGA_SANITAER": self.tr("Fluides-Sanitaire"),
                           "ATTR_PRG_BEREICH_TGA_EXTRAS": self.tr("Fluides-Supplément"),
                           "ATTR_PRG_BEREICH_INT_OBJMAN": self.tr("Gestionnaire objets"),
                           "ATTR_PRG_BEREICH_INT_KATASTER": self.tr("Cadastre des conduites"),
                           "ATTR_PRG_BEREICH_ADDIN_MODULE": self.tr("Module d'extensions internes"),
                           "ATTR_PRG_BEREICH_MATERIAL": self.tr("Attributs matériau"),
                           "ATTR_PRG_BEREICH_IFC": "IFC",
                           "ATTR_PRG_BEREICH_IBD": self.tr("IBD Ouvrages"),
                           "ATTR_PRG_BEREICH_WETO": "Weto",
                           "ATTR_PRG_BEREICH_FIDES": self.tr("Allplan Suisse"),
                           "ATTR_PRG_BEREICH_INTERNATIONAL": self.tr("Allplan International"),
                           "ATTR_PRG_BEREICH_AUSTRIA": self.tr("Attributs de construction AT"),
                           "ATTR_PRG_BEREICH_VORLAGE": self.tr("Projets modèles"),
                           "ATTR_PRG_BEREICH_NAMINGSYSTEM": "Allplan Exchange",
                           "ATTR_PRG_BEREICH_SENDPACKAGE": "Inconnu 1",
                           "ATTR_PRG_BEREICH_USER_LAYOUT": "Inconnu 2",
                           "ATTR_PRG_BEREICH_WIDO": self.tr("Portes, Fenêtre"),
                           "ATTR_PRG_BEREICH_STEEL": self.tr("Construction métallique"),
                           "ATTR_PRG_BEREICH_NEVARIS": "Nevaris",
                           "ATTR_PRG_BEREICH_KLASSIFIZIERUNG": self.tr("Classification"),
                           "ATTR_PRG_BEREICH_PROFILE": self.tr("Profils"),
                           "ATTR_PRG_BEREICH_FERTIGTEIL_STANDARD": self.tr("Éléments de structure préfa spéci. 1"),
                           "ATTR_PRG_BEREICH_FERTIGTEIL_USER": self.tr("Éléments de structure préfa spéci. 2"),
                           "ATTR_PRG_BEREICH_IBDING": self.tr("IBD Ingénierie"),
                           "ATTR_PRG_BEREICH_BRIDGE": "Bridge",
                           "ATTR_PRG_BEREICH_?": "Inconnu3",
                           "ATTR_PRG_BEREICH_BAUGRUB": self.tr("Génie civil"),
                           "ATTR_PRG_BEREICH_CLASH_DETECTION": self.tr("Contrôle du chevauchement")}

    def allplan_ifc_loading(self):
        """
        Permet de charger le model de type d'IFC
        :return:
        """

        dict_traductions = {self.tr("Indéfini"): "",
                            "IfcBeam": "Ifc - Poutre",
                            "IfcChimney": "Ifc - Cheminée",
                            "IfcColumn": "Ifc - Poteau",
                            "IfcCovering": "Ifc - Finition - Revêtements",
                            "IfcCurtainWall": "Ifc - Mur non porteur",
                            "IfcDoor": "Ifc - Porte - Porte-fenêtre",
                            "IfcElementAssembly": "Ifc - Élément assemblé",
                            "IfcFooting": "Ifc - Semelle - Fondation",
                            "IfcFurniture": "Ifc - Ameublement",
                            "IfcMember": "Ifc - Élément structurel",
                            "IfcPile": "Ifc - Élément structurel mince",
                            "IfcRailing": "Ifc - garde-corps",
                            "IfcRamp": "Ifc - Voie inclinée - plancher",
                            "IfcRoof": "Ifc - Élément toiture",
                            "IfcShadingDevice": "Ifc - Protection solaire ou lumière",
                            "IfcSlab": "Ifc - Dalle - Plancher",
                            "IfcStair": "Ifc - Escalier",
                            "IfcWall": "Ifc - Mur",
                            "IfcWindow": "Ifc - Fenêtre",
                            "IfcActuator": "",
                            "IfcAirTerminal": "",
                            "IfcAirTerminalBox": "",
                            "IfcAirToAirHeatRecovery": "",
                            "IfcAlarm": "",
                            "IfcAnnotation": "",
                            "IfcAssembly": "",
                            "IfcBoiler": "",
                            "IfcBuildingElementPart": "",
                            "IfcBuildingElementProxy": "",
                            "IfcBuildingStorey": "",
                            "IfcCableCarrierFitting": "",
                            "IfcCableCarrierSegment": "",
                            "IfcCableSegment": "",
                            "IfcChiller": "",
                            "IfcCoil": "",
                            "IfcCompressor": "",
                            "IfcCondenser": "",
                            "IfcController": "",
                            "IfcCooledBeam": "",
                            "IfcCoolingTower": "",
                            "IfcDamper": "",
                            "IfcDiscreteAccessory": "",
                            "IfcDistributionChamberElement": "",
                            "IfcDistributionControlElement": "",
                            "IfcDistributionElement": "",
                            "IfcDistributionFlowElement": "",
                            "IfcDuctFitting": "",
                            "IfcDuctSegment": "",
                            "IfcDuctSilencer": "",
                            "IfcElectricAppliance": "",
                            "IfcElectricFlowStorageDevice": "",
                            "IfcElectricGenerator": "",
                            "IfcElectricHeater": "",
                            "IfcElectricMotor": "",
                            "IfcElectricTimeControl": "",
                            "IfcEnergyConversionDevice": "",
                            "IfcEvaporativeCooler": "",
                            "IfcEvaporator": "",
                            "IfcFan": "",
                            "IfcFastener": "",
                            "IfcFilter": "",
                            "IfcFireSuppressionTerminal": "",
                            "IfcFloor": "",
                            "IfcFlowController": "",
                            "IfcFlowFitting": "",
                            "IfcFlowInstrument": "",
                            "IfcFlowMeter": "",
                            "IfcFlowMovingDevice": "",
                            "IfcFlowSegment": "",
                            "IfcFlowSegmentStorageDevice": "",
                            "IfcFlowStorageDevice": "",
                            "IfcFlowTerminal": "",
                            "IfcFlowTreatmentDevice": "",
                            "IfcFurnishingElement": "",
                            "IfcGasTerminal": "",
                            "IfcGrid": "",
                            "IfcGroup": "",
                            "IfcHeatExchanger": "",
                            "IfcHumidifier": "",
                            "IfcJunctionBox": "",
                            "IfcLamp": "",
                            "IfcLightFixture": "",
                            "IfcMechanicalFastener": "",
                            "IfcMotorConnection": "",
                            "IfcOpeningElement": "",
                            "IfcOutlet": "",
                            "IfcPipeFitting": "",
                            "IfcPipeSegment": "",
                            "IfcProtectiveDevice": "",
                            "IfcPump": "",
                            "IfcReinforcingBar": "",
                            "IfcReinforcingMesh": "",
                            "IfcSanitaryTerminal": "",
                            "IfcSensor": "",
                            "IfcSite": "",
                            "IfcSpace": "",
                            "IfcSpaceHeater": "",
                            "IfcStackTerminal": "",
                            "IfcSwitchingDevice": "",
                            "IfcSystem": "",
                            "IfcSystemFurnitureElement": "",
                            "IfcTank": "",
                            "IfcTransformer": "",
                            "IfcTransportElement": "",
                            "IfcTubeBundle": "",
                            "IfcUnitaryEquipment": "",
                            "IfcValve": "",
                            "IfcWallStandardCase": "",
                            "IfcWasteTerminal": ""}

        self.model_ifc.clear()

        translation_dict_684 = dict()

        for key, traduction in dict_traductions.items():

            index_element = self.model_ifc.rowCount()

            valeur = QStandardItem(key)

            if traduction != "" and self.langue == "FR":
                valeur.setData(traduction, Qt.ToolTipRole)

            self.model_ifc.appendRow([QStandardItem(f"{index_element}"), valeur])

            translation_dict_684[f"{index_element}"] = valeur

        self.enumeration_translations["684"] = translation_dict_684

    def allplan_layer_loading(self):
        """
        Permet de charger les layers d'Allplan
        : return: None
        """

        if not isinstance(self.allplan_paths, AllplanPaths):
            print("allplan_manage -- allplan_layer_loading -- not isinstance(self.allplan_paths, AllplanPaths)")
            return

        self.model_layers_view.clear()
        self.model_layers.clear()

        layer_file_path = f"{self.catalog_user_path}layerdef.dat"

        # Recherche dans le dossier utilisateur
        if not os.path.exists(layer_file_path):

            layer_file_path = f"{self.allplan_paths.std_path}layerdef.dat"

            # Recherche dans le dossier STD
            if not os.path.exists(layer_file_path):

                layer_file_path = f"{self.allplan_paths.etc_path}layerbas.dat"

                # Recherche dans le dossier ETC
                if not os.path.exists(layer_file_path):
                    print("allplan_manage -- allplan_layer_loading -- not os.path.exists(layer_file_path)")
                    return

        font = qstandarditem_font()
        groupe_font = qstandarditem_font(italic=True)
        layer_font = qstandarditem_font(bold=True)

        translation_dict = dict()

        lines_list = read_file_to_list(file_path=layer_file_path)

        self.model_layers_view.clear()
        self.model_layers.clear()

        qs_group_name = qs_sub_group_name = None
        self.model_layers.appendRow([QStandardItem("0"), QStandardItem(self.tr("STANDARD"))])

        translation_dict["0"] = self.tr("STANDARD")

        root_model_view = self.model_layers_view.invisibleRootItem()

        standard_item_nom = QStandardItem(get_icon(layer_icon), self.tr("STANDARD"))
        standard_item_nom.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        standard_item_nom.setFont(layer_font)

        standard_item_numero = QStandardItem("0")
        standard_item_numero.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        standard_item_numero.setFont(layer_font)

        root_model_view.appendRow([standard_item_nom, standard_item_numero, QStandardItem("")])

        if len(lines_list) == 0:
            print(f"allplan_manage -- allplan_layer_loading -- file is empty")
            return

        if not lines_list[0].startswith("g@"):
            print(f"allplan_manage -- allplan_layer_loading -- not lines_list[0].startswith(g@)")
            return

        try:

            # Parcours l'ensemble des lignes
            for line in lines_list:

                if line.startswith("g@"):
                    group_name = line.replace("g@", "").replace("@", "").strip()

                    qs_group_name = QStandardItem(get_icon(folder_icon), group_name)
                    qs_group_name.setFlags(Qt.ItemIsEnabled)
                    qs_group_name.setFont(font)

                    qs_group_number = QStandardItem("")
                    qs_group_number.setFlags(Qt.ItemIsEnabled)
                    qs_group_number.setFont(font)

                    qs_group_id = QStandardItem("")
                    qs_group_id.setFlags(Qt.ItemIsEnabled)
                    qs_group_id.setFont(font)

                    # print(f"{nom_groupe}")
                    root_model_view.appendRow([qs_group_name, qs_group_number, qs_group_id])
                    continue

                if line.startswith("b@"):
                    sub_group_name = line.replace("b@", "").replace("@", "").strip()

                    qs_sub_group_name = QStandardItem(get_icon(folder_icon), sub_group_name)
                    qs_sub_group_name.setFlags(Qt.ItemIsEnabled)
                    qs_sub_group_name.setFont(groupe_font)

                    qs_sub_group_number = QStandardItem("")
                    qs_sub_group_number.setFlags(Qt.ItemIsEnabled)
                    qs_sub_group_number.setFont(groupe_font)

                    qs_sub_group_id = QStandardItem("")
                    qs_sub_group_id.setFlags(Qt.ItemIsEnabled)
                    qs_sub_group_id.setFont(groupe_font)

                    if qs_group_name is not None:
                        # print(f"    {nom_groupe_2}")
                        qs_group_name.appendRow([qs_sub_group_name, qs_sub_group_number, qs_sub_group_id])

                    continue

                # Vérification / exclure les titres et garder seulement les layers (contient plus de 4 @)
                if line.count("@") > 4:

                    # Création d'une liste des différents éléments de la ligne (numero, layer, ...)
                    datas = line.split("@")

                    # Vérification que la liste contient bien au moins 3 éléments
                    if len(datas) > 3:
                        # Définition de la ligne sur laquelle écrire dans le model des layers
                        layer_number = datas[3].strip()
                        layer_name = datas[1].strip()
                        layer_id = datas[2].strip()

                        # Ajout des données dans le model layers
                        self.model_layers.appendRow(
                            [QStandardItem(layer_number), QStandardItem(layer_name), QStandardItem(layer_id)])

                        translation_dict[layer_number] = layer_name

                        # Ajout des données dans le model layers view
                        qs_layer_name = QStandardItem(get_icon(layer_icon), layer_name)
                        qs_layer_name.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                        qs_layer_name.setFont(layer_font)

                        qs_layer_number = QStandardItem(layer_number)
                        qs_layer_number.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                        qs_layer_number.setFont(layer_font)

                        qs_layer_id = QStandardItem(layer_id)
                        qs_layer_id.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                        qs_layer_id.setFont(layer_font)

                        if qs_sub_group_name is not None:
                            # print(f"        {nom_layer} : {numero_layer} : {code_layer}")
                            qs_sub_group_name.appendRow([qs_layer_name, qs_layer_number, qs_layer_id])

        except Exception as error:
            print(f"allplan_manage -- allplan_layer_loading -- erreur --> {error}")
            return

        self.enumeration_translations["141"] = translation_dict

    def allplan_line_loading(self):
        """
        Permet de lire le fichier des types de lignes ou type de plumes
        : return: QStandardItemModel avec les keys et valeurs
        : rtype: QStandardItemModel
        """

        if not isinstance(self.allplan_paths, AllplanPaths):
            print("allplan_manage -- allplan_line_loading -- not isinstance(self.allplan_paths, AllplanPaths)")
            return

        self.model_line.clear()
        self.model_line.appendRow([QStandardItem("-1"), QStandardItem("")])

        size_icon = 200

        line_file_path = f"{self.catalog_user_path}linetype.dat"

        if not os.path.exists(line_file_path):

            line_file_path = f"{self.allplan_paths.std_path}linetype.dat"

            # Recherche dans le dossier STD
            if not os.path.exists(line_file_path):

                line_file_path = f"{self.allplan_paths.etc_path}linetype.dat"

                # Recherche dans le dossier ETC
                if not os.path.exists(line_file_path):
                    print("allplan_manage -- allplan_line_loading -- not os.path.exists(line_file_path)")
                    return

        lines_list = read_file_to_list(file_path=line_file_path)

        try:

            if len(lines_list) != 0:

                for ligne in lines_list:
                    ligne: str

                    if "//" in ligne or ligne == "":
                        continue

                    if len(ligne) <= 2:
                        continue

                    if ligne.startswith(".L"):
                        pixmap = QPixmap(size_icon, 20)
                        pixmap.fill(Qt.white)
                        brush = QBrush(Qt.black)

                        pen = QPen(brush, 1, Qt.SolidLine)
                        painter = QPainter(pixmap)
                        painter.setPen(pen)
                        painter.drawLine(0, 10, size_icon, 10)
                        painter.end()

                        self.model_line.appendRow([QStandardItem("1"), QStandardItem(QIcon(pixmap), "01")])

                        continue

                    line_id = ligne[:2].strip()

                    line_pattern = ligne[2:-3]

                    pattern_list = line_pattern.split(" ")

                    pattern_final_list = list()

                    if line_id != "90" and line_id != "91" and line_id != "92" and line_id != "97" and \
                            line_id != "98" and line_id != "99":

                        for pattern in pattern_list:

                            pattern = pattern.strip()

                            if pattern == "" or pattern == "0":
                                continue

                            try:

                                valeur = round(float(pattern.strip()) / 2)

                            except ValueError as error:
                                print(f"allplan_manage -- allplan_line_loading --  erreur : {error}")
                                continue

                            pattern_final_list.append(valeur)

                    if len(pattern_final_list) > 0:
                        # print(f"{numero_ligne} : {liste_pattern_final}")

                        pixmap = QPixmap(size_icon, 20)
                        pixmap.fill(Qt.white)
                        brush = QBrush(Qt.black)

                        pen = QPen(brush, 1, Qt.SolidLine)
                        pen.setStyle(Qt.CustomDashLine)
                        pen.setDashPattern(pattern_final_list)

                        painter = QPainter(pixmap)
                        painter.setPen(pen)
                        painter.drawLine(0, 10, size_icon, 10)
                        painter.end()

                        self.model_line.appendRow([QStandardItem(f"{line_id}"),
                                                   QStandardItem(QIcon(pixmap), line_id.zfill(2))])

            # ----------------
            # Ligne 90
            # ----------------

            pixmap = QPixmap(size_icon, 20)
            pixmap.fill(Qt.white)
            brush = QBrush(Qt.black)

            pen = QPen(brush, 1, Qt.SolidLine)
            pen.setStyle(Qt.DashLine)

            painter = QPainter(pixmap)
            painter.setPen(pen)
            painter.drawLine(0, 8, size_icon, 8)

            pen2 = QPen(brush, 1, Qt.SolidLine)
            painter.setPen(pen2)
            painter.drawLine(0, 12, size_icon, 12)

            painter.end()

            self.model_line.appendRow([QStandardItem("90"), QStandardItem(QIcon(pixmap), "90")])

            # ----------------
            # Ligne 91
            # ----------------

            pixmap = QPixmap(size_icon, 20)
            pixmap.fill(Qt.white)
            brush = QBrush(Qt.black)

            pen = QPen(brush, 1, Qt.SolidLine)
            painter = QPainter(pixmap)
            painter.setPen(pen)
            painter.drawLine(0, 10, size_icon, 10)

            painter.drawLine(int(size_icon / 4) + 2, 6, int(size_icon / 4) - 2, 14)
            painter.drawLine(int(size_icon / 4) + 5, 6, int(size_icon / 4) + 1, 14)

            painter.drawLine(int(size_icon / 2) + 2, 6, int(size_icon / 2) - 2, 14)
            painter.drawLine(int(size_icon / 2) + 5, 6, int(size_icon / 2) + 1, 14)

            painter.drawLine(int(size_icon / 4 * 3) + 2, 6, int(size_icon / 4 * 3) - 2, 14)
            painter.drawLine(int(size_icon / 4 * 3) + 5, 6, int(size_icon / 4 * 3) + 1, 14)

            painter.end()

            self.model_line.appendRow([QStandardItem("91"), QStandardItem(QIcon(pixmap), "91")])

            # ----------------
            # Ligne 92
            # ----------------

            pixmap = QPixmap(size_icon, 20)
            pixmap.fill(Qt.white)
            brush = QBrush(Qt.black)

            pen = QPen(brush, 1, Qt.SolidLine)
            pen.setStyle(Qt.DashDotLine)

            painter = QPainter(pixmap)

            painter.setPen(pen)
            painter.drawLine(0, 10, size_icon, 10)

            pen2 = QPen(brush, 1, Qt.SolidLine)
            painter.setPen(pen2)

            painter.drawLine(int(size_icon / 4) + 2, 6, int(size_icon / 4) - 2, 14)
            painter.drawLine(int(size_icon / 4) + 5, 6, int(size_icon / 4) + 1, 14)

            painter.drawLine(int(size_icon / 2) + 2, 6, int(size_icon / 2) - 2, 14)
            painter.drawLine(int(size_icon / 2) + 5, 6, int(size_icon / 2) + 1, 14)

            painter.drawLine(int(size_icon / 4 * 3) + 2, 6, int(size_icon / 4 * 3) - 2, 14)
            painter.drawLine(int(size_icon / 4 * 3) + 5, 6, int(size_icon / 4 * 3) + 1, 14)

            painter.end()

            self.model_line.appendRow([QStandardItem("92"), QStandardItem(QIcon(pixmap), "92")])

            # ----------------
            # Ligne 97
            # ----------------

            pixmap = QPixmap(size_icon, 20)
            pixmap.fill(Qt.white)
            brush = QBrush(Qt.black)

            pen = QPen(brush, 1, Qt.SolidLine)

            painter = QPainter(pixmap)

            painter.setPen(pen)
            painter.drawLine(0, 10, 23, 10)
            painter.drawLine(31, 10, 59, 10)
            painter.drawLine(67, 10, 96, 10)
            painter.drawLine(104, 10, 133, 10)
            painter.drawLine(141, 10, 169, 10)
            painter.drawLine(177, 10, 200, 10)

            painter.drawLine(23, 14, 31, 6)
            painter.drawLine(23, 6, 31, 14)

            painter.drawLine(59, 14, 67, 6)
            painter.drawLine(59, 6, 67, 14)

            painter.drawLine(96, 14, 104, 6)
            painter.drawLine(96, 6, 104, 14)

            painter.drawLine(133, 14, 141, 6)
            painter.drawLine(133, 6, 141, 14)

            painter.drawLine(169, 14, 177, 8)
            painter.drawLine(169, 6, 177, 14)

            painter.end()

            self.model_line.appendRow([QStandardItem("97"), QStandardItem(QIcon(pixmap), "97")])

            # ----------------
            # Ligne 98
            # ----------------

            pixmap = QPixmap(size_icon, 20)
            pixmap.fill(Qt.white)
            brush = QBrush(Qt.black)

            pen = QPen(brush, 1, Qt.SolidLine)

            painter = QPainter(pixmap)

            painter.setPen(pen)
            painter.drawLine(0, 10, 200, 10)

            painter.drawLine(46, 14, 54, 6)
            painter.drawLine(46, 6, 54, 14)

            painter.drawLine(96, 14, 104, 6)
            painter.drawLine(96, 6, 104, 14)

            painter.drawLine(146, 14, 154, 6)
            painter.drawLine(146, 6, 154, 14)

            painter.end()

            self.model_line.appendRow([QStandardItem("98"), QStandardItem(QIcon(pixmap), "98")])

            # ----------------
            # Ligne 99
            # ----------------

            pixmap = QPixmap(size_icon, 20)
            pixmap.fill(Qt.white)
            brush = QBrush(Qt.black)

            pen = QPen(brush, 1, Qt.SolidLine)
            painter = QPainter(pixmap)

            painter.setPen(pen)
            painter.drawLine(0, 10, 200, 10)

            painter.drawLine(23, 14, 31, 6)
            painter.drawLine(23, 6, 31, 14)

            painter.drawLine(59, 14, 67, 6)
            painter.drawLine(59, 6, 67, 14)

            painter.drawLine(96, 14, 104, 6)
            painter.drawLine(96, 6, 104, 14)

            painter.drawLine(133, 14, 141, 6)
            painter.drawLine(133, 6, 141, 14)

            painter.drawLine(169, 14, 177, 8)
            painter.drawLine(169, 6, 177, 14)

            painter.end()

            self.model_line.appendRow([QStandardItem("99"), QStandardItem(QIcon(pixmap), "99")])

        except Exception as error:
            print(f"allplan_manage -- allplan_line_loading --  erreur : {error}")
            return

    def allplan_pen_loading(self):
        """
        Permet de lire le fichier des types de lignes ou type de plumes
        : return: QStandardItemModel avec les keys et valeurs
        : rtype: QStandardItemModel
        """

        if not isinstance(self.allplan_paths, AllplanPaths):
            print("allplan_manage -- allplan_pen_loading -- not isinstance(self.allplan_paths, AllplanPaths)")
            return

        self.model_pen.clear()
        self.model_pen.appendRow([QStandardItem("-1"), QStandardItem("")])

        size_icon = 200

        pen_file_path = f"{self.catalog_user_path}linethick.dat"

        if not os.path.exists(pen_file_path):

            pen_file_path = f"{self.allplan_paths.std_path}linethick.def"

            if not os.path.exists(pen_file_path):

                pen_file_path = f"{self.allplan_paths.etc_path}linethick.def"

                if not os.path.exists(pen_file_path):
                    print("allplan_manage -- allplan_pen_loading -- not os.path.exists(pen_file_path)")
                    return

        lines_list = read_file_to_list(file_path=pen_file_path)

        if len(lines_list) == 0:
            return

        try:

            for ligne in lines_list:
                ligne: str
                if "/" in ligne or ligne == "":
                    continue

                if len(ligne) <= 2:
                    continue

                numero_ligne = ligne[:2].strip()
                epaisseur = ligne[2:6].strip()

                if ligne.startswith(".L"):
                    continue

                millimetre = ""
                apercu = 0

                if epaisseur != "":

                    try:
                        millimetre = f"{int(epaisseur) / 100:.2f}"
                        apercu = int(int(epaisseur) / 10)
                    except ValueError:
                        pass

                if millimetre == "" or apercu == 0:
                    continue

                pixmap = QPixmap(size_icon, 20)
                pixmap.fill(Qt.white)
                brush = QBrush(Qt.black)

                pen = QPen(brush, apercu, Qt.SolidLine)

                painter = QPainter(pixmap)
                painter.setPen(pen)
                painter.drawLine(0, 10, size_icon, 10)
                painter.end()

                standarditem = QStandardItem(QIcon(pixmap), millimetre)
                self.model_pen.appendRow([QStandardItem(f"{numero_ligne}"), standarditem])

        except Exception as error:
            print(f"allplan_manage -- allplan_pen_loading --  erreur : {error}")
            return

    def allplan_color_loading(self):
        """
        Permet de charger les couleurs d'allplan
        : return: model des couleurs d'allplan
        :rtype: QStandardItemModel
        """

        self.model_color.clear()

        self.model_color.appendRow([QStandardItem("-1"), QStandardItem("")])

        liste_qcolor = ['#ffffff', '#000000', '#ffff00', '#00ffff', '#00ff00', '#ff00ff', '#ff0000', '#0000ff',
                        '#ff8000', '#f0f0b4', '#dcff64', '#c8c832', '#c89632', '#c86432', '#966432', '#821eb4',
                        '#2d2d2d', '#3b3b3b', '#494949', '#575757', '#656565', '#737373', '#808080', '#8f8f8f',
                        '#a0a0a0', '#ababab', '#c0c0c0', '#c7c7c7', '#d5d5d5', '#e3e3e3', '#f1f1f1', '#fafafa',
                        '#505000', '#6e6e00', '#808000', '#b3b300', '#c6c600', '#d9d900', '#ecec00', '#f5f500',
                        '#ffff1c', '#ffff38', '#ffff54', '#ffff70', '#ffff8c', '#ffffa8', '#ffffc4', '#ffffe0',
                        '#005050', '#006e6e', '#008080', '#00b3b3', '#00c6c6', '#00d9d9', '#00ecec', '#00f5f5',
                        '#1cffff', '#38ffff', '#36ffff', '#70ffff', '#8cffff', '#a8ffff', '#c4ffff', '#e0ffff',
                        '#005000', '#006e00', '#008000', '#00b300', '#00c600', '#00d900', '#00ec00', '#00f500',
                        '#1cff1c', '#38ff38', '#54ff54', '#70ff70', '#8cff8c', '#a8ffa8', '#c4ffc4', '#e0ffe0',
                        '#500050', '#6e006e', '#800080', '#b300b3', '#c600c6', '#d900d9', '#ec00ec', '#f500f5',
                        '#ff1cff', '#ff38ff', '#ff54ff', '#ff70ff', '#ff8cff', '#ffa8ff', '#ffc4ff', '#ffe0ff',
                        '#500000', '#6e0000', '#800000', '#9f0000', '#b20000', '#c50000', '#d80000', '#f50000',
                        '#ff1c1c', '#ff3838', '#ff5454', '#ff7070', '#ff8c8c', '#ffa8a8', '#ffc4c4', '#ffe0e0',
                        '#000050', '#00006e', '#000080', '#0000b3', '#0000c6', '#0000d9', '#0000ec', '#0000f5',
                        '#1c1cff', '#3838ff', '#5454ff', '#7070ff', '#8c8cff', '#a8a8ff', '#c4c4ff', '#e0e0ff',
                        '#783c14', '#874614', '#965014', '#a55a14', '#b46414', '#c36e14', '#d27814', '#e18214',
                        '#f0911e', '#f09628', '#f09b32', '#f0a03c', '#f0a546', '#f0aa50', '#f0af5a', '#f0b464',
                        '#a0a08c', '#aaaa91', '#b4b496', '#bebe9b', '#c8c8a0', '#d2d2a5', '#dcdcaa', '#e6e6af',
                        '#f0f0bd', '#f0f0c6', '#f0f0cf', '#f0f0d8', '#f0f0e1', '#f0f0ea', '#f0f0f3', '#f0f0fc',
                        '#64873c', '#739641', '#82a546', '#91b44b', '#a4c350', '#afd255', '#bee15a', '#cdf05f',
                        '#e0ff6e', '#e4ff78', '#e8ff82', '#ecff8c', '#f0ff96', '#f4ffa0', '#f8ffaa', '#fcffb4',
                        '#787832', '#828232', '#8c8c32', '#969632', '#a0a032', '#aaaa32', '#b4b432', '#bebe32',
                        '#cdce41', '#d2d450', '#d7da5f', '#dce06e', '#e1e67d', '#e6ec8c', '#ebf29b', '#f0f8aa',
                        '#504632', '#5f5032', '#6e5a32', '#7d6432', '#8c6e32', '#9b7832', '#aa8232', '#b98c32',
                        '#cd9b32', '#d2a046', '#d7a550', '#dcaa5a', '#e1af64', '#e6b46e', '#ebb978', '#f0be82',
                        '#50140a', '#5f1e0f', '#6e2814', '#7d3219', '#8c3c1e', '#9b4623', '#aa5028', '#b95a2d',
                        '#ce6e3c', '#d47846', '#da8250', '#e08c5a', '#e69664', '#eca06e', '#f2aa78', '#f8b482',
                        '#46140a', '#501e0f', '#5a2814', '#643219', '#6e3c1e', '#784623', '#825028', '#8c5a2d',
                        '#9b7143', '#a07e54', '#a58b65', '#aa9876', '#afa587', '#b4b298', '#b9bfa9', '#beccba',
                        '#0f1e3c', '#1e1e4b', '#2d1e5a', '#3c1e69', '#4b1e78', '#5a1e87', '#691e96', '#781ea5',
                        '#8c32bd', '#9646c6', '#a05acf', '#aa6ed8', '#b482e1', '#be96ea', '#c8aaf3', '#d2befc']

        for numero_ligne, hex_color in enumerate(liste_qcolor):
            color = QColor(hex_color)
            pixmap = QPixmap(200, 10)
            pixmap.fill(color)

            standarditem = QStandardItem(QIcon(pixmap), f"{numero_ligne}")
            standarditem.setToolTip(f"rgb= {color.red()} , {color.green()}, {color.blue()}, hex= {hex_color}")

            self.model_color.appendRow([QStandardItem(f"{numero_ligne}"), standarditem])

        return

    def allplan_haching_loading(self):
        """
        Permet de charger la liste des hachurages
        :return: None
        """

        self.model_haching.clear()

        self.allplan_zt_loading(model_current=self.model_haching, file_name="zts")

    def allplan_pattern_loading(self):
        """
        Permet de charger la liste des motifs
        : return: None
        """

        self.model_pattern.clear()
        self.allplan_zt_loading(model_current=self.model_pattern, file_name="zt")

    def allplan_zt_loading(self, model_current: QStandardItemModel, file_name: str):

        if not isinstance(self.allplan_paths, AllplanPaths):
            return

        extension = language_extension_3.get(self.langue, "eng")
        file_name_index = f"{file_name}000.{extension}"

        # ------------------------------------------
        # -------------- get numbers and titles ----
        # ------------------------------------------

        title_datas = dict()

        self.allplan_zt_search(folder_path=self.allplan_paths.etc_path,
                               file_name=file_name,
                               file_name_index=file_name_index,
                               title_datas=title_datas)

        if not self.allplan_zt_search(folder_path=self.catalog_user_path,
                                      file_name=file_name,
                                      file_name_index=file_name_index,
                                      title_datas=title_datas):
            self.allplan_zt_search(folder_path=self.allplan_paths.std_path,
                                   file_name=file_name,
                                   file_name_index=file_name_index,
                                   title_datas=title_datas)

        # ------------------------------------------
        # -------------- model  --------------------
        # ------------------------------------------

        model_current.appendRow([QStandardItem("-1"), QStandardItem("")])

        if len(title_datas) == 0:
            print(f"allplan_manage -- allplan_zt_search -- len(title_datas) == 0")
            return

        numbers_list = list(title_datas.keys())
        numbers_list.sort(key=int)

        for number in numbers_list:

            if not isinstance(number, str):
                continue

            name = title_datas.get(number)

            if not isinstance(name, str):
                continue

            name = name.zfill(3)

            model_current.appendRow([QStandardItem(number), QStandardItem(name)])

        return

    @staticmethod
    def allplan_zt_search(folder_path: str, file_name: str, file_name_index: str, title_datas: dict) -> bool:
        try:
            files_list = glob.glob(f"{folder_path}{file_name}[0-9][0-9][0-9].000")

            # ------------------------------------------
            # -------------- files name ------------
            # ------------------------------------------

            for zt_path in files_list:

                number = Path(zt_path).resolve().stem.lower().replace(file_name, "")

                if not isinstance(number, str):
                    continue

                if len(number) != 3:
                    continue

                try:
                    number_int = int(number)

                except Exception:
                    continue

                number = f"{number_int}"

                if number not in title_datas:
                    title_datas[number] = number

            # ------------------------------------------
            # -------------- find titles ------------
            # ------------------------------------------

            file_path = f"{folder_path}{file_name_index}"

            if read_zt_file(file_path=file_path, title_datas=title_datas):
                return True

            for country in ["eng", "fra", "deu", "ita", "spa", "hrv", "rum", "rus"]:

                file_path = f"{folder_path}{file_name}000.{country}"

                if read_zt_file(file_path=file_path, title_datas=title_datas):
                    return True

        except Exception as error:
            print(f"allplan_manage -- allplan_zt_search -- error : {error}")

        return False

    def allplan_style_loading(self):
        """
        Permet de charger la liste des styles de surfaces
        : return: None
        """

        self.model_style.clear()
        self.model_style_view.clear()

        groupe_font = qstandarditem_font(italic=True)
        item_font = qstandarditem_font(bold=True)

        qs_nom = QStandardItem(get_icon(none_icon), self.tr("Aucun"))
        qs_nom.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        qs_nom.setFont(item_font)

        qs_numero = QStandardItem("-1")
        qs_numero.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        qs_numero.setFont(item_font)

        self.model_style_view.appendRow([qs_nom, qs_numero])
        self.model_style.appendRow([QStandardItem("-1"), QStandardItem("")])

        lines_list = read_file_to_list(file_path=self.allplan_style_get_path())

        if len(lines_list) == 0:
            print("allplan_manage -- allplan_style_loading --  file is empty")
            return

        numero = ""
        groupe = self.model_style_view
        dict_groupes = dict()

        try:

            for line in reversed(lines_list):

                line = line.strip()

                if line.startswith("<grp><nr>"):
                    line = line.replace("<grp><nr>", "").replace("</wname></grp>", "")

                    if "</nr><wname>" in line:
                        numero_groupe, nom_groupe = line.split("</nr><wname>", maxsplit=1)

                        qs_grp = QStandardItem(get_icon(folder_icon), nom_groupe)
                        qs_grp.setFlags(Qt.ItemIsEnabled)
                        qs_grp.setFont(groupe_font)

                        dict_groupes[numero_groupe] = qs_grp
                        continue
                    continue

                if "<nr>" in line:

                    if "<grp>" in line:

                        line = line.replace("<nr>", "").replace("</grp>", "").replace(" ", "")

                        if "</nr><grp>" not in line:
                            print(f"gestion_allplan -- chargement_styles -- erreur : </nr><grp> not in ligne")
                            continue

                        numero, index_grp = line.split("</nr><grp>", maxsplit=1)

                        if index_grp not in dict_groupes:
                            print(f"gestion_allplan -- chargement_styles -- erreur : index_grp not in dict_groupes")
                            continue

                        groupe = dict_groupes[index_grp]

                        if not isinstance(groupe, QStandardItem):
                            print(
                                f"gestion_allplan -- chargement_styles -- erreur : not "
                                f"isinstance(groupe, QStandardItem)")

                        continue

                    numero = line.replace("<nr>", "").replace("</nr>", "")

                if "<wname>" in line:
                    nom = line.replace("<wname>", "").replace("</wname>", "")

                    qs_nom = QStandardItem(get_icon(style_icon), nom)
                    qs_nom.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    qs_nom.setFont(item_font)

                    qs_numero = QStandardItem(numero)
                    qs_numero.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    qs_numero.setFont(item_font)

                    groupe.appendRow([qs_nom, qs_numero])
                    self.model_style.appendRow([QStandardItem(numero), QStandardItem(nom)])

                    continue

                if "<fs>" in line:
                    numero = ""
                    groupe = self.model_style_view

            for qs_grp in dict_groupes.values():

                qs_grp: QStandardItem

                if qs_grp.rowCount() == 0:
                    continue

                qs_num = QStandardItem("")
                qs_num.setFlags(Qt.ItemIsEnabled)
                self.model_style_view.appendRow([qs_grp, qs_num])

        except Exception as error:
            print(f"allplan_manage -- allplan_style_loading --  erreur : {error}")
            return

    def allplan_style_get_path(self) -> str:

        style_path = f"{self.catalog_user_path}facestyle.sty"

        if os.path.exists(style_path):
            return style_path

        if not isinstance(self.allplan_paths, AllplanPaths):
            return ""

        style_path = f"{self.allplan_paths.std_path}facestyle.sty"

        if os.path.exists(style_path):
            return style_path

        extension = language_extension_3.get(self.langue, "eng")
        style_path = f"{self.allplan_paths.etc_path}facestyle_{extension}.{extension}"

        if os.path.exists(style_path):
            return style_path

        for extension in language_extension_3.values():
            style_path = f"{self.allplan_paths.etc_path}facestyle_{extension}.{extension}"
            if os.path.exists(style_path):
                return style_path

        return ""

    def allplan_unit_loading(self):
        """

        :return:
        """

        self.model_units_default.clear()
        self.model_units.clear()

        translation_dict_120 = dict()
        translation_dict_202 = dict()

        liste_defaut = ["m³", "m²", "m", self.tr("Qt"), self.tr("kg")]

        for index_unite, unite in enumerate(liste_defaut):
            self.model_units_default.appendRow([QStandardItem(f"{index_unite}"), QStandardItem(unite)])
            self.model_units.appendRow([QStandardItem(f"{index_unite}"), QStandardItem(unite)])

            translation_dict_120[f"{index_unite}"] = unite
            translation_dict_202[f"{index_unite}"] = unite

        liste_unites = settings_list(unit_list_file)

        for index_unite, unite in enumerate(liste_unites):

            if unite in liste_defaut:
                continue

            self.model_units.appendRow([QStandardItem(f"{index_unite}"), QStandardItem(unite)])

            translation_dict_202[f"{index_unite}"] = unite

        self.enumeration_translations["120"] = translation_dict_120
        self.enumeration_translations["202"] = translation_dict_202

    def allplan_obj_names_loading(self):

        translation_dict_obj = dict()

        if not os.path.exists(self.allplan_paths.std_obj000):
            return

        lines_list = read_file_to_list(file_path=self.allplan_paths.std_obj000)

        try:

            for line_index, line_text in enumerate(lines_list):

                if line_index < 2:
                    continue

                element = line_text[12:]
                element = element.strip().split(" ", 1)

                if len(element) < 2:
                    continue

                number = element[0]

                if not isinstance(number, str):
                    continue

                if number == "":
                    continue

                try:
                    int(element[0])
                except Exception:
                    continue

                description = element[1]

                if not isinstance(description, str):
                    continue

                if description == "":
                    continue

                if number in translation_dict_obj:
                    continue

                translation_dict_obj[number] = description

        except Exception:
            pass

        self.enumeration_translations["13"] = translation_dict_obj
        self.enumeration_translations["OBJ"] = translation_dict_obj

    @staticmethod
    def allplan_asw_loading(asw_file_path: str):
        """
        Permet la lecture des fichiers asw
        : param chemin_fichier_asw: chemin complet du fichier asw à lire
        : return: liste des éléments formatés
        : rtype: list
        """

        if not os.path.exists(asw_file_path):
            return list()

        return read_file_to_list(file_path=asw_file_path, duplicates=False, list_sorted=True)

    def allplan_attribute_xml_to_model(self, attribute_file_path: str):
        """
        Permet de charger un fichier xml des attributs d'allplan dans le model des attributs
        : param fichier_attributs_allplan: Chemin complet du fichier d'attribut Allplan à charger
        : return: None
        """

        print(f"allplan_manage -- allplan_attribute_xml_to_model --> {attribute_file_path}")

        tree = validation_fichier_xml(attribute_file_path)

        if tree is None:
            print(f"allplan_manage -- allplan_attribute_xml_to_model -- xml erreur -> {attribute_file_path}")
            return False

        # Parcours l'ensemble des lignes contenant : AttributeDefinition
        for attribut_def_xml in tree.findall('AttributeDefinition'):

            attribut_def_xml: etree._Element

            # ---------------------------------------
            # Numéro attribut
            # ---------------------------------------

            xml_attribut_numero = attribut_def_xml.find(code_xml_number)

            if get_value_is_valid(xml_attribut_numero):

                attribute_number: str = xml_attribut_numero.text

            else:

                print("allplan_manage -- allplan_attribute_xml_to_model --  xml_attribut_numero is None")

                continue

            # ========================================================
            try:
                numero = int(attribute_number)

                user = 1999 < numero < 12000
                import_number = 55000 <= numero < 99000

            except ValueError:
                continue

            # ========================================================

            if attribute_number in self.attributes_dict:
                continue

            # ---------------------------------------
            # UID
            # ---------------------------------------

            xml_attribut_uid = attribut_def_xml.find(code_xml_uid)

            if get_value_is_valid(xml_attribut_uid):

                attribute_uid = xml_attribut_uid.text

            else:

                print("allplan_manage -- allplan_attribute_xml_to_model -- xml_attribut_uid is None")

                continue

            # ---------------------------------------
            # attribut nom
            # ---------------------------------------

            xml_attribut_nom = attribut_def_xml.find(code_xml_text)

            if get_value_is_valid(xml_attribut_nom):

                attribute_name = xml_attribut_nom.text

            else:

                print("allplan_manage -- allplan_attribute_xml_to_model -- xml_attribut_nom is None")

                continue

            # ---------------------------------------
            # Type attribut
            # ---------------------------------------

            xml_attribut_type = attribut_def_xml.find(code_xml_datatype)

            if get_value_is_valid(xml_attribut_type):

                attribut_type = xml_attribut_type.text

            else:

                print("allplan_manage -- allplan_attribute_xml_to_model -- xml_attribut_type is None")

                continue

            # ---------------------------------------
            # Groupe attribut
            # ---------------------------------------

            xml_attribut_group = attribut_def_xml.find(code_xml_group)

            if get_value_is_valid(xml_attribut_group):

                attribute_group = self.get_group_by_number(group_index=xml_attribut_group.text, number=attribute_number)

            else:

                print("allplan_manage -- allplan_attribute_xml_to_model -- xml_attribut_type is None")

                continue

            # ---------------------------------------
            # Minimum attribut
            # ---------------------------------------

            xml_attribut_min = attribut_def_xml.find(code_xml_min)

            if get_value_is_valid(xml_attribut_min):
                attribut_min = xml_attribut_min.text

            else:

                attribut_min = ""

            # ---------------------------------------
            # Minimum attribut
            # ---------------------------------------

            xml_attribut_max = attribut_def_xml.find(code_xml_max)

            if get_value_is_valid(xml_attribut_max):
                attribut_max = xml_attribut_max.text

            else:

                attribut_max = ""

            # ---------------------------------------
            # Modify attribut
            # ---------------------------------------

            xml_attribut_modify = attribut_def_xml.find(code_xml_modify)

            if get_value_is_valid(xml_attribut_modify):
                attribut_modify = xml_attribut_modify.text

            else:

                attribut_modify = "false"

            # ---------------------------------------
            # Visible attribut
            # ---------------------------------------

            xml_attribut_visible = attribut_def_xml.find(code_xml_visible)

            if get_value_is_valid(xml_attribut_visible):
                attribut_visible = xml_attribut_visible.text

            else:

                attribut_visible = "false"

            # ---------------------------------------
            # 110 - Priorité
            # ---------------------------------------
            if attribute_number == "110":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribut_val_defaut_defaut.get("110"),
                                           datatype="I",
                                           option=code_attr_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)
                continue

            # ---------------------------------------
            # 111 - Type de hachurage
            # ---------------------------------------
            if attribute_number == "111":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_fill.get("111"),
                                           datatype="E",
                                           option=code_attr_combo_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)
                continue

            # ---------------------------------------
            # 118 - Identificateur de remplissage
            # ---------------------------------------
            if attribute_number == "118":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_fill.get("118"),
                                           datatype="I",
                                           option=code_attr_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)
                continue

            # ---------------------------------------
            # 120 == Grandeur
            # ---------------------------------------
            if attribute_number == "120":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribut_val_defaut_defaut.get("120"),
                                           datatype="I",
                                           option=code_attr_combo_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_units_default)
                continue

            # ---------------------------------------
            # 141 == Layer
            # ---------------------------------------
            if attribute_number == "141":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_layer.get("141"),
                                           datatype="I",
                                           option=code_attr_combo_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_layers)
                continue

            # ---------------------------------------
            # 202 == Unité
            # ---------------------------------------
            if attribute_number == "202":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribut_val_defaut_defaut.get("202"),
                                           datatype="C",
                                           option=code_attr_combo_str_edit,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_units)
                continue

            # ---------------------------------------
            # 231 - Pourtout de la salle enumaration
            # ---------------------------------------
            if attribute_number == "231":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_room.get("231"),
                                           datatype="C",
                                           option=code_attr_combo_str_edit,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_231)
                continue

            # ---------------------------------------
            # 232 - Type de surface 277
            # ---------------------------------------
            if attribute_number == "232":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=self.traduire_valeur_232(default=True),
                                           datatype="C",
                                           option=code_attr_combo_str_edit,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_232)
                continue

            # ---------------------------------------
            # 233 - Type de surface habitable
            # ---------------------------------------
            if attribute_number == "233":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=self.traduire_valeur_233(default=True),
                                           datatype="C",
                                           option=code_attr_combo_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_233)
                continue

            # ---------------------------------------
            # 235 - Type d'utilisation din 277
            # ---------------------------------------
            if attribute_number == "235":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=self.traduire_valeur_235(default=True),
                                           datatype="C",
                                           option=code_attr_combo_str_edit,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_235)
                continue

            # ---------------------------------------
            # 264 - Facteur_surf_habitable_pièce
            # ---------------------------------------
            if attribute_number == "264":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_room.get("264"),
                                           datatype="R",
                                           option=code_attr_dbl,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)
                continue

            # ---------------------------------------
            # 266 - Facteur_DIN277
            # ---------------------------------------
            if attribute_number == "266":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_room.get("266"),
                                           datatype="R",
                                           option=code_attr_dbl,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)
                continue

            # ---------------------------------------
            # 339 - Intéraction entre les éléments
            # ---------------------------------------
            if attribute_number == "339":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value="0",
                                           datatype="C",
                                           option=code_attr_combo_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_339)
                continue

            # ---------------------------------------
            # 345 - Type de traits
            # ---------------------------------------
            if attribute_number == "345":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_layer.get("345"),
                                           datatype="E",
                                           option=code_attr_combo_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_line)
                continue

            # ---------------------------------------
            # 346 - Type de plumes
            # ---------------------------------------
            if attribute_number == "346":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_layer.get("346"),
                                           datatype="E",
                                           option=code_attr_combo_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_pen)
                continue

            # ---------------------------------------
            # 347 - Type de couleur
            # ---------------------------------------
            if attribute_number == "347" or attribute_number == "252":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_layer.get("347"),
                                           datatype="E",
                                           option=code_attr_combo_int,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_color)
                continue

            # ---------------------------------------
            # 349 - du_layer
            # ---------------------------------------
            if attribute_number == "349":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_layer.get("349"),
                                           datatype="I",
                                           option=code_attr_combo_str_edit,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)
                continue

            # ---------------------------------------
            # 600 - Hachurage dans vue en plan
            # ---------------------------------------
            if attribute_number == "600":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribute_val_default_fill.get("600"),
                                           datatype="I",
                                           option=code_attr_chk,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)
                continue

            # ---------------------------------------
            # 684 - IFC
            # ---------------------------------------
            if attribute_number == "684":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=self.tr("Indéfini"),
                                           datatype="C",
                                           option=code_attr_combo_str_edit,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=self.model_ifc)

                continue

            # ---------------------------------------
            # 18313 - Attribute set Category
            # ---------------------------------------
            if attribute_number == "18313":
                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value="",
                                           datatype="C",
                                           option=code_attr_str,
                                           unit="",
                                           uid=attribute_uid,
                                           user=False,
                                           import_number=False,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)

                continue

            # ---------------------------------------
            # 18358 - Attribute set object
            # ---------------------------------------
            if attribute_number == "18358":

                if self.model_18358.rowCount() <= 1:

                    self.allplan_attribute_add(number=attribute_number,
                                               name=attribute_name,
                                               group=attribute_group,
                                               value="",
                                               datatype="C",
                                               option=code_attr_str,
                                               unit="",
                                               uid=attribute_uid,
                                               user=False,
                                               import_number=False,
                                               modify=attribut_modify,
                                               visible=attribut_visible,
                                               min_val=attribut_min,
                                               max_val=attribut_max,
                                               enumeration=self.model_18358)

                else:

                    self.allplan_attribute_add(number=attribute_number,
                                               name=attribute_name,
                                               group=attribute_group,
                                               value="",
                                               datatype="C",
                                               option=code_attr_combo_str_edit,
                                               unit="",
                                               uid=attribute_uid,
                                               user=False,
                                               import_number=False,
                                               modify=attribut_modify,
                                               visible=attribut_visible,
                                               min_val=attribut_min,
                                               max_val=attribut_max,
                                               enumeration=self.model_18358)

                continue

            xml_attribut_textbox = attribut_def_xml.find('TextBox')
            xml_attribut_unit = attribut_def_xml.find('Unit')
            attribut_unite = ""

            if get_value_is_valid(xml_attribut_unit):
                attribut_unite = xml_attribut_unit.text

            # ---------------------------------------
            # Si l'attribut est une "TextBox"
            # ---------------------------------------
            if xml_attribut_textbox is not None and attribute_number not in formula_list_attributes:

                if attribut_type == "R":
                    attribut_option = code_attr_dbl

                    if "2022" in self.version_allplan_current or "2023" in self.version_allplan_current:
                        attribut_valeur = "0,000"
                    else:
                        attribut_valeur = "0.000"

                elif attribut_type == "I":
                    attribut_option = code_attr_int
                    attribut_valeur = "1"

                elif attribut_type == "D":
                    attribut_option = code_attr_date
                    attribut_valeur = QDate.currentDate().toString("dd/MM/yyyy")

                else:
                    attribut_option = code_attr_str
                    attribut_valeur = ""

                if attribute_name.startswith("Date"):
                    attribut_valeur = QDate.currentDate().toString("dd/MM/yyyy")

                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribut_valeur,
                                           datatype=attribut_type,
                                           option=attribut_option,
                                           unit=attribut_unite,
                                           uid=attribute_uid,
                                           user=user,
                                           import_number=import_number,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)

                continue

            xml_attribut_checkbox = attribut_def_xml.find('CheckBox')

            # ---------------------------------------
            # Si l'attribut est une "CheckBox"
            # ---------------------------------------
            if xml_attribut_checkbox is not None:
                attribut_valeur = "0"

                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribut_valeur,
                                           datatype=attribut_type,
                                           option=code_attr_chk,
                                           unit=attribut_unite,
                                           uid=attribute_uid,
                                           user=user,
                                           import_number=import_number,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)

                continue

            xml_attribut_formule = attribut_def_xml.find('Formula')

            # ---------------------------------------
            # Si l'attribut est une "Formule"
            # ---------------------------------------
            if xml_attribut_formule is not None or attribute_number in formula_list_attributes:

                if attribut_type == "R":
                    attribut_option = code_attr_formule_float

                elif attribut_type == "I":
                    attribut_option = code_attr_formule_int

                else:
                    attribut_option = code_attr_formule_str

                if attribute_number == "96":
                    attribut_valeur = "@83@"
                else:
                    attribut_valeur = "1"

                # ------

                if user:

                    valeur_formule = xml_attribut_formule.text

                    if valeur_formule is not None:
                        attribut_valeur = valeur_formule

                # ------

                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribut_valeur,
                                           datatype=attribut_type,
                                           option=attribut_option,
                                           unit=attribut_unite,
                                           uid=attribute_uid,
                                           user=user,
                                           import_number=import_number,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max)
                continue

            # ---------------------------------------
            # Si l'attribut est une "ComboBox"
            # ---------------------------------------

            xml_attribut_combobox = attribut_def_xml.find('ComboBox')

            # Si l'attribut est une "ComboBox éditable"
            if xml_attribut_combobox is not None:

                attribut_valeur = ""

                if attribut_type == "C":
                    attribut_option = code_attr_combo_str_edit

                elif attribut_type == "R":
                    attribut_option = code_attr_combo_float_edit

                elif attribut_type == "I":
                    attribut_option = code_attr_combo_int_edit

                else:
                    attribut_option = code_attr_combo_str_edit

                model = QStandardItemModel()

                # -------------------------
                # Lecture des item à ajouter dans le model de la Combobox
                # -------------------------

                value_list = list()

                for enumeration in xml_attribut_combobox:

                    xml_attribut_key = enumeration.find('Key')

                    # Recherche de la key
                    if get_value_is_valid(xml_attribut_key):

                        # Mise en mémoire de la key et de sa valeur
                        key_enum = xml_attribut_key.text
                        xml_val_enum = enumeration.find('Value')

                        if get_value_is_valid(xml_val_enum):
                            value = xml_val_enum.text
                        else:
                            value = ""

                        standarditem = QStandardItem(value)

                        value_list.append(value)

                        if model.rowCount() == 0:
                            attribut_valeur = key_enum

                        # Ajout de la key et de sa valeur dans le model de la combobox
                        model.appendRow([QStandardItem(key_enum), standarditem])

                # -------------------------
                # Lecture du fichier ASW
                # -------------------------

                # Définition du chemin dans lequel est stockée la liste des valeurs possibles
                chemin_fichier_attribut_asw = f"{self.asw_folder}attrib_{attribute_number}.asw"

                liste_attributs_fichier = self.allplan_asw_loading(chemin_fichier_attribut_asw)

                # Vérification que le chemin existe
                if len(liste_attributs_fichier) > 0:

                    # parcourir les différentes ligne
                    for valeur_attribut in liste_attributs_fichier:

                        if valeur_attribut is None:
                            valeur_attribut = ""

                        if model.rowCount() == 0:
                            attribut_valeur = valeur_attribut

                        if valeur_attribut.strip() in value_list:
                            continue

                        value_list.append(valeur_attribut.strip())

                        row_count = model.rowCount()

                        # Ajout de l'index dans la colonne 0
                        model.appendRow([QStandardItem(f"{row_count}"), QStandardItem(valeur_attribut)])

                # -------------------------

                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribut_valeur,
                                           datatype=attribut_type,
                                           option=attribut_option,
                                           unit=attribut_unite,
                                           uid=attribute_uid,
                                           user=user,
                                           import_number=import_number,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=model)
                continue

            # ---------------------------------------
            # Si l'attribut est une "Enumeration"
            # ---------------------------------------

            xml_attribut_enumaration = attribut_def_xml.find('Enumeration')

            # Si l'attribut est une "ComboBox non modifiable"
            if xml_attribut_enumaration is not None:

                model = QStandardItemModel()
                attribut_valeur = ""

                translation_dict = dict()

                # Parcours les choix possible de la combobox non modifiable
                for enumeration in xml_attribut_enumaration:

                    xml_attribut_key = enumeration.find('Key')

                    # Recherche des key pour cette enumeration
                    if get_value_is_valid(xml_attribut_key):

                        # Définition de la key et de sa valeur
                        key_enum = xml_attribut_key.text
                        xml_val_enum = enumeration.find('Value')

                        if get_value_is_valid(xml_val_enum):
                            value = xml_val_enum.text
                        else:
                            value = ""

                        standarditem = QStandardItem(value)

                        if model.rowCount() == 0:
                            attribut_valeur = key_enum

                        # Copie des valeurs dans le model qui sera utilisé dans la QCombobox
                        model.appendRow([QStandardItem(key_enum), standarditem])

                        translation_dict[key_enum] = value

                self.enumeration_translations[attribute_number] = translation_dict

                if attribute_number == "209":
                    model.sort(1, Qt.AscendingOrder)
                    self.enumeration_translations["GW"] = translation_dict

                self.allplan_attribute_add(number=attribute_number,
                                           name=attribute_name,
                                           group=attribute_group,
                                           value=attribut_valeur,
                                           datatype=attribut_type,
                                           option=code_attr_combo_int,
                                           unit=attribut_unite,
                                           uid=attribute_uid,
                                           user=user,
                                           import_number=import_number,
                                           modify=attribut_modify,
                                           visible=attribut_visible,
                                           min_val=attribut_min,
                                           max_val=attribut_max,
                                           enumeration=model)
                continue

        return True

    def allplan_attribute_add(self, number: str, name: str, group: str,
                              value: str, datatype: str, option: str, unit: str, uid: str,
                              user: bool, import_number: bool,
                              modify: str, visible: str,
                              min_val: str, max_val: str,
                              enumeration=QStandardItemModel()):

        qs_number = QStandardItem(number)

        try:
            qs_number.setData(int(number), user_data_type)
        except:
            return

        self.attribute_name_list.append(re.escape(name))
        self.conversions_dict[name] = f"@{number}@"

        tooltips = self.allplan_attribut_get_tooltips(number, name, value, option, unit, user, import_number,
                                                      modify, visible,
                                                      min_val, max_val,
                                                      enumeration)

        self.attributes_dict[number] = {code_attr_number: number,
                                        code_attr_name: name,
                                        code_attr_group: group,
                                        code_attr_value: value,
                                        code_attr_datatype: datatype,
                                        code_attr_option: option,
                                        code_attr_unit: unit,
                                        code_attr_uid: uid,
                                        code_attr_user: user,
                                        code_attr_import: import_number,
                                        code_attr_min: min_val,
                                        code_attr_max: max_val,
                                        code_attr_modify: modify,
                                        code_attr_visible: visible,
                                        code_attr_tooltips: tooltips,
                                        code_attr_enumeration: enumeration}

        qs_name = QStandardItem(name)
        qs_name.setToolTip(tooltips)

        self.attribute_model.appendRow([qs_number,
                                        qs_name,
                                        QStandardItem(datatype),
                                        QStandardItem(group)])

    def allplan_attribut_get_tooltips(self, number: str, name: str, value: str, option: str, unit: str,
                                      user: bool, import_number: bool,
                                      modify: str, visible: str,
                                      min_val: str, max_val: str,
                                      enumeration: QStandardItemModel) -> str:

        # -------------------
        # User attribute
        # -------------------

        if user:
            attribut_utlisateur = self.tr("Oui")
        else:
            attribut_utlisateur = self.tr("Non")

        if import_number:
            attribut_import = self.tr("Oui")
        else:
            attribut_import = self.tr("Non")

        # -------------------
        # Option
        # -------------------

        if option == code_attr_str:
            type_element_translated = self.tr("Texte")

        elif option == code_attr_int:
            type_element_translated = self.tr("Nombre entier")

        elif option == code_attr_dbl:
            type_element_translated = self.tr("Nombre décimal")

        elif option == code_attr_date:
            type_element_translated = self.tr("Date")

        elif option == code_attr_combo_str_edit:
            type_element_translated = self.tr("ComboBox éditable - Texte")

        elif option == code_attr_combo_float_edit:
            type_element_translated = self.tr("ComboBox éditable - Nombre décimal")

        elif option == code_attr_combo_int_edit:
            type_element_translated = self.tr("ComboBox éditable - Nombre entier")

        elif option == code_attr_combo_int:
            type_element_translated = self.tr("ComboBox non modifiable - Nombre entier")

        elif option == code_attr_formule_str:
            type_element_translated = self.tr("Texte - Formule")

        elif option == code_attr_formule_int:
            type_element_translated = self.tr("Nombre entier - Formule")

        elif option == code_attr_formule_float:
            type_element_translated = self.tr("Nombre décimal - Formule")

        else:
            type_element_translated = self.tr("Inconnu")

        if type_element_translated is None:
            type_element_translated = self.tr("Inconnu")

        # -------------------
        # First part
        # -------------------

        a = self.tr("Numéro d'attribut")
        b = self.tr("Nom d'attribut")
        c = self.tr("Type d'attribut")
        e = self.tr("Unité")

        tooltip = ("<p style='white-space:pre'>"
                   f"{a} : {number}<br>"
                   f"{b} : <b>{name}</b><br>"
                   f"{c} : {type_element_translated}<br>")

        if attribut_utlisateur:

            d = self.tr("Attribut utilisateur")

            tooltip += f"{d} : {attribut_utlisateur}<br>"

        elif attribut_import:

            d2 = self.tr("Attribut Import")

            tooltip += f"{d2} : {attribut_import}<br>"

        if unit != "":
            tooltip += f"{e} : {unit}<br>"

        if min_val != "":
            tooltip += f"MinValue : {min_val}<br>"

        if max_val != "":
            tooltip += f"MaxValue : {max_val}<br>"

        tooltip += (f"Modify : {modify}<br>"
                    f"Visible : {visible}<br>")

        # f"UID : {uid}<br>")

        # -------------------
        # Second part - Enumeration Combobox
        # -------------------

        f = self.tr("LISTE DES CHOIX")
        g = self.tr("Index")
        h = self.tr("Valeur")
        i = self.tr("élément supplémentaire")
        i2 = self.tr("éléments supplémentaires")
        j = self.tr("Formule").upper()

        if option in [code_attr_combo_str_edit, code_attr_combo_float_edit, code_attr_combo_int_edit,
                      code_attr_combo_int]:

            row_count = enumeration.rowCount()

            if row_count == 0:
                return tooltip

            tooltip += "----------------------------------<br>"
            tooltip += f"          {f}\n"

            tooltip += "----------------------------------<br>"
            tooltip += f"{g} |   {h}\n "
            tooltip += "----------------------------------<br>"

            tronc = 0
            if row_count > 15:
                tronc = row_count - 15
                row_count = 15

            for index_item in range(row_count):
                qstandarditem_index: QStandardItem = enumeration.item(index_item, col_enum_index)
                qstandarditem_valeur: QStandardItem = enumeration.item(index_item, col_enum_valeur)

                id_item = qstandarditem_index.text()
                valeur_item = qstandarditem_valeur.text()

                tooltip += f"   - {id_item.zfill(2)} | {valeur_item}<br>"

            if tronc == 1:
                tooltip += f"   + 1 {i} ...<br>"

            elif tronc > 1:

                tooltip += f"   + {tronc} {i2} ...<br>"

            return tooltip

        # -------------------
        # Second part - Formula
        # -------------------

        if "Formule" in option:

            if value == "" or attribut_utlisateur != self.tr("Oui"):
                return tooltip

            formule_formater = self.traduction_formule_allplan(value)

            tooltip += "<br><br>----------------------------------<br>"
            tooltip += f"          {j}\n"

            tooltip += "----------------------------------<br>"
            tooltip += f"{formule_formater}\n "

            return tooltip

        # -------------------
        # Third part - Aim
        # -------------------

        if number not in self.aim_dict:
            return tooltip

        title, enumeration_list = self.aim_dict.get(number)

        if not isinstance(title, str) or not isinstance(enumeration_list, list):
            return tooltip

        if title == "":
            return tooltip

        tooltip += "<br><br>----------------------------------<br>"
        tooltip += f"Titre dans AIM : <b>{title}</b>"

        tooltip += "<br>----------------------------------<br>"

        if len(enumeration_list) != 0:

            tooltip += "LISTE DES CHOIX DANS AIM <br>"
            tooltip += "----------------------------------<br>"
            tooltip += f"{g} |   {h}<br>"
            tooltip += "----------------------------------<br>"

            row_count = len(enumeration_list)
            tronc = 0
            if row_count > 25:
                tronc = row_count - 25

            for index_item, valeur_item in enumerate(enumeration_list):
                id_item = str(index_item)
                tooltip += f"   - {id_item.zfill(2)} | {valeur_item}<br>"

                if index_item > 25:
                    break

            if tronc == 1:
                tooltip += f"   + 1 {i} ...<br>"

            elif tronc > 1:

                tooltip += f"   + {tronc} {i2} ...<br>"

        return tooltip

    @staticmethod
    def a___________________chargement_attributs______():
        pass

    def get_group_by_number(self, group_index: str, number: str) -> str:

        all_grp_txt = self.tr("Tous les attributs Allplan")

        try:
            number_int = int(group_index)

        except Exception as error:
            print(f"allplan_manage -- get_group_by_name -- {error}")
            return all_grp_txt

        groups_detected = [all_grp_txt]

        if number in self.material_favorite_list:
            groups_detected.append(self.tr("Favoris Ouvrage"))

        if number in self.component_favorite_list:
            groups_detected.append(self.tr("Favoris Composant"))

        if number in self.formula_favorite_list:
            groups_detected.append(self.tr("Favoris Formule"))

        if group_index in self.group_save_dict:
            groups_detected.extend(self.group_save_dict.get(group_index))

            all_grp_txt = ", ".join(groups_detected)
            return all_grp_txt

        new_grp = [nom for i, nom in enumerate(self.group_list) if number_int & (1 << i)]

        self.group_save_dict[group_index] = new_grp

        groups_detected.extend(new_grp)

        # self.attribute_group_list.append(nom)

        all_grp_txt = ", ".join(groups_detected)

        return all_grp_txt

    def allplan_231_loading(self) -> None:

        if self.langue not in translation_231:
            return

        translation_list = translation_231[self.langue]

        if not isinstance(translation_list, list):
            return

        self.model_231.clear()

        translation_dict_231 = dict()

        for row_index, value in enumerate(translation_list):
            self.model_231.appendRow([QStandardItem(f"{row_index}"), get_look_qs(QStandardItem(value))])
            translation_dict_231[f"{row_index}"] = value

        self.enumeration_translations["231"] = translation_dict_231

    def allplan_232_loading(self) -> None:

        if self.langue not in translation_232 or self.langue not in translation_232_combo:
            return

        translation_list = translation_232[self.langue]
        translation_list_combo = translation_232_combo[self.langue]

        translation_dict_232 = dict()

        if not isinstance(translation_list, list) or not isinstance(translation_list_combo, list):
            return

        self.model_232.clear()

        for row_index, value in enumerate(translation_list):
            qs = get_look_qs(QStandardItem(value))

            qs.setToolTip(translation_list[row_index])

            self.model_232.appendRow([QStandardItem(f"{row_index}"), qs])

            translation_dict_232[f"{row_index}"] = value

        self.enumeration_translations["232"] = translation_dict_232

    def allplan_233_loading(self) -> None:

        if self.langue not in translation_233:
            return

        translation_list = translation_233[self.langue]
        translation_dict_233 = dict()

        if not isinstance(translation_list, list):
            return

        self.model_233.clear()

        for row_index, value in enumerate(translation_list):
            self.model_233.appendRow([QStandardItem(f"{row_index}"), get_look_qs(QStandardItem(value))])

            translation_dict_233[f"{row_index}"] = value

        self.enumeration_translations["233"] = translation_dict_233

    def allplan_235_loading(self) -> None:

        if self.langue not in translation_235:
            return

        translation_list = translation_235[self.langue]
        translation_dict_235 = dict()

        if not isinstance(translation_list, list):
            return

        self.model_235.clear()

        for row_index, value in enumerate(translation_list):
            self.model_235.appendRow([QStandardItem(f"{row_index}"), get_look_qs(QStandardItem(value))])
            translation_dict_235[f"{row_index}"] = value

        self.enumeration_translations["235"] = translation_dict_235

    def allplan_339_loading(self) -> None:

        self.model_339.clear()

        self.model_339.appendRow([QStandardItem("0"), get_look_qs(QStandardItem(self.tr("Aucune")))])
        self.model_339.appendRow([QStandardItem("1"), get_look_qs(QStandardItem(self.tr("Dynamique")))])
        self.model_339.appendRow([QStandardItem("2"), get_look_qs(QStandardItem(self.tr("Fixe")))])

        self.enumeration_translations["339"] = {"0": self.tr("Aucune"),
                                                "1": self.tr("Dynamique"),
                                                "2": self.tr("Fixe")}

    # def allplan_18313_loading(self):
    #
    #     self.model_18313.clear()
    #
    #     self.model_18313.appendRow([QStandardItem("0"), QStandardItem("")])
    #
    #     xml_folder = f"{self.catalog_user_path}Xml\\AttrSet\\"
    #
    #     if not os.path.exists(xml_folder):
    #         return
    #
    #     file_list = glob.glob(f"{xml_folder}*.xml")
    #
    #     if len(file_list) == 0:
    #         return
    #
    #     attributes_object_list = list()
    #
    #     index_row = 1
    #
    #     for file in file_list:
    #
    #         category = file.replace(f"{xml_folder}AttributeSetCollection_", "").replace(".xml", "")
    #
    #         if ";" not in category:
    #             continue
    #
    #         category, group = category.split(";", maxsplit=1)
    #
    #         if group in attributes_object_list:
    #             continue
    #
    #         self.model_18313.appendRow([QStandardItem(f"{index_row}"), QStandardItem(group)])
    #
    #         index_row += 1

    @staticmethod
    def a___________________allplan_attribute_18358______():
        pass

    def allplan_18358_loading(self) -> bool:

        self.model_18358.clear()

        self.model_18358.appendRow([QStandardItem("0"), QStandardItem("")])

        self.allplan_18358_dict.clear()

        if not isinstance(self.allplan_paths, AllplanPaths):
            return False

        # ------------------
        # PRJ
        # ------------------

        if self.catalog_user_path != self.allplan_paths.std_path:

            xml_folder = f"{self.catalog_user_path}Xml\\AttrSet\\"

            attributes_object_list = self.allplan_18358_get_xml_list(folder_path=xml_folder)

            if len(attributes_object_list) > 30:
                self.allplan_18358_add_items(attributes_object_list=attributes_object_list)
                return True

        titles_dict = dict()
        name_attribut_set = "IFC Common"

        # ------------------
        # ETC
        # ------------------

        xml_folder = f"{self.allplan_paths.etc_xml_path}AttrSet\\"

        if not os.path.exists(xml_folder):
            return False

        attributes_object_list = self.allplan_18358_get_xml_list(folder_path=xml_folder)

        if len(attributes_object_list) <= 30:
            return False

        titles_dict[name_attribut_set] = attributes_object_list

        # ------------------
        # STD
        # ------------------

        xml_folder = f"{self.allplan_paths.std_xml_path}AttrSet\\"

        if not os.path.exists(xml_folder):
            self.allplan_18358_add_items(attributes_object_list=attributes_object_list)
            return True

        attributes_object_list = self.allplan_18358_get_xml_list(folder_path=xml_folder)

        if len(attributes_object_list) > 30:
            self.allplan_18358_add_items(attributes_object_list=attributes_object_list)
            return True

        for f in os.scandir(xml_folder):

            folder_path = f.path

            if not isinstance(folder_path, str):
                continue

            if not folder_path.endswith("\\"):
                folder_path += "\\"

            attributes_object_list = self.allplan_18358_get_xml_list(folder_path=folder_path)

            if len(attributes_object_list) > 30 and f.name not in titles_dict:
                name_attribut_set = f.name
                titles_dict[name_attribut_set] = attributes_object_list

        titles_count = len(titles_dict)

        if titles_count == 1:
            attributes_object_list = titles_dict.get(name_attribut_set, list())

            if not isinstance(attributes_object_list, list) and len(attributes_object_list) <= 30:
                return False

            self.allplan_18358_add_items(attributes_object_list=attributes_object_list)
            return True

        self.allplan_18358_dict = titles_dict

        return True

    def allplan_18358_choise_end(self, name_attribut_set: str, attributes_object_list: list) -> bool:

        if not isinstance(name_attribut_set, str) or not isinstance(attributes_object_list, list):
            return False

        if len(attributes_object_list) <= 30 or name_attribut_set == "":
            self.allplan_18358_dict.clear()
            return

        self.user_attributes_xml_path = f"{self.allplan_paths.std_xml_path}AttrSet\\{name_attribut_set}\\"

        if not self.allplan_18358_add_items(attributes_object_list=attributes_object_list):
            return False

        datas = self.attributes_dict.get("18358", dict())

        if not isinstance(datas, dict):
            return False

        if code_attr_option not in datas:
            return False

        datas[code_attr_option] = code_attr_combo_str_edit

        self.allplan_18358_dict.clear()

        return True

    def allplan_18358_add_items(self, attributes_object_list: list) -> bool:

        if len(attributes_object_list) == 0:
            return False

        for index_row, name in enumerate(attributes_object_list):
            self.model_18358.appendRow([QStandardItem(f"{index_row + 1}"), QStandardItem(name)])

        return True

    @staticmethod
    def allplan_18358_get_xml_list(folder_path: str) -> list:

        if not os.path.exists(folder_path):
            return list()

        file_list = glob.glob(f"{folder_path}*.xml")

        if len(file_list) == 0:
            return list()

        attributes_object_list = list()

        for index_row, file in enumerate(file_list):

            category = file.replace(f"{folder_path}AttributeSetCollection_", "").replace(".xml", "")

            if ";" in category:
                category, _ = category.split(";", maxsplit=1)

            if category in attributes_object_list:
                continue

            attributes_object_list.append(category)

        return attributes_object_list

    @staticmethod
    def a___________________allplan_attribute_favorites______():
        pass

    def favorite_loading(self):

        datas = settings_read(attribute_config_file)

        material_favorite_list = datas.get("material", attribute_config_datas["material"])
        self.material_favorite_list = convert_list_attribute_number(material_favorite_list)

        component_favorite_list = datas.get("component", attribute_config_datas["component"])
        self.component_favorite_list = convert_list_attribute_number(component_favorite_list)

        formula_favorite_list = datas.get("formula", attribute_config_datas["formula"])
        self.formula_favorite_list = convert_list_attribute_number(formula_favorite_list)

    @staticmethod
    def a___________________allplan_functions_reading______():
        pass

    # def get_excel_functions(self) -> None:
    #
    #     self.functions_excel_dict.clear()
    #
    #     self.functions_excel_dict["SUM"]

    def get_python_functions(self) -> None:

        if not isinstance(self.allplan_paths, AllplanPaths):
            return

        self.functions_python_dict.clear()

        if not os.path.exists(self.allplan_paths.std_path):
            print("allplan_manage -- get_python_functions -- not os.path.exists(std_path)")
            return

        function_file_path = f"{self.allplan_paths.std_path}Scripts\\functions.py"

        if not os.path.exists(function_file_path):
            print("allplan_manage -- get_python_functions -- not os.path.exists(function_file_path)")
            return

        content = read_file_to_list(file_path=function_file_path)

        if not isinstance(content, list):
            print("allplan_manage -- get_python_functions -- not isinstance(content, list)")
            return

        function_name = function_content = variables = ""

        for line in content:

            if not isinstance(line, str):
                print("allplan_manage -- get_python_functions -- not isinstance(line, str)")
                continue

            if line.startswith("def"):

                if function_name in self.functions_python_dict:
                    continue

                if function_name != "":
                    self.functions_python_dict[function_name] = {"args": variables,
                                                                 "content": function_content}

                # -----------------------------------------------------------

                function_name = line.strip().replace("def ", "")
                variables = ""

                function_content = line.rstrip() + "\n"

                if "(" in function_name and ")" in function_name:
                    txt_start = function_name.index("(")
                    txt_end = function_name.index(")")

                    variables = function_name[txt_start + 1:txt_end]
                    function_name = function_name[:txt_start]

                continue

            if line.strip() == "":
                continue

            function_content += line.rstrip() + "\n"

        return

    def get_vbs_functions(self) -> None:

        if not isinstance(self.allplan_paths, AllplanPaths):
            return

        self.functions_vbs_dict.clear()

        if not os.path.exists(self.allplan_paths.std_path):
            print("allplan_manage -- get_vbs_functions -- not os.path.exists(std_path)")
            return

        files_list = glob.glob(f"{self.allplan_paths.std_path}vbs\\*.vbs")

        if len(files_list) == 0:
            return

        for file_path in files_list:
            self.vbs_functions_reading(content=read_file_to_list(file_path=file_path))

    def vbs_functions_reading(self, content: list) -> None:

        if not isinstance(content, list):
            print("allplan_manage -- vbs_functions_reading -- not isinstance(content, list)")
            return

        function_name = function_content = variables = ""

        for line in content:

            if not isinstance(line, str):
                print("allplan_manage -- vbs_functions_reading -- not isinstance(line, str)")
                continue

            if line.startswith("Function"):

                function_name = line.strip().replace("Function ", "")
                variables = ""

                function_content = line.rstrip() + "\n"

                if "(" in function_name and ")" in function_name:
                    txt_start = function_name.index("(")
                    txt_end = function_name.index(")")

                    variables = function_name[txt_start + 1:txt_end]
                    function_name = function_name[:txt_start]

                continue

            if line.startswith("End Function"):

                if function_name in self.functions_vbs_dict:
                    continue

                function_content += line.rstrip() + "\n"

                self.functions_vbs_dict[function_name] = {"args": variables,
                                                          "content": function_content}

                continue

            if line.strip() == "":
                continue

            function_content += line.rstrip() + "\n"

        return

    def get_excel_functions(self):

        self.functions_excel_dict.clear()

        self.functions_excel_dict["TEXT"] = \
            {"args": "TEXT(value, format_text)",
             "content": "This function is used to convert a number or a date into a test string in the "
                        "specified format, where:\n"

                        "- Value is a numeric value you want to convert to text.\n"

                        " - Format_text is the desired format.\n"

                        '=TEXT(A1,"mm/dd/yyyy") - convert a date in cell A1 into a text string in the traditional US'
                        ' date format, such as "01/01/2015" (month/day/year).\n'

                        '=TEXT(A1,"€#,##0.00") - converts a number in A1 into a currency text string such as "€3.00".'}

        self.functions_excel_dict["TRIM"] = \
            {"args": "TRIM(text)",
             "content": "This function removes leading, trailing spaces as well as excess spaces between words.\n"
                        "Where text is either a text string or reference to the cell containing the text from "
                        "which you want to remove spaces."}

        self.functions_excel_dict["SUBSTITUTE"] = \
            {"args": "SUBSTITUTE(text, old_text, new_text, [instance_num])",
             "content": 'This functionreplaces one set of characters with another in a specified cell or a '
                        'text string.\n'

                        'The syntax of the SUBSTITUTE function is as follows:\n'

                        'Text - the original text string or reference to a cell where you '
                        'want to substitute certain characters.\n'

                        'Old_text - the characters you want to replace.\n'

                        'New_text - the characters you want to replace the old text with.\n'

                        'Nth_appearance - an optional parameter that specifies which occurrence of old_text'
                        ' you want to replace with new_text. \n'

                        'If omitted, then every occurrence of the old text will be replaced with the new text.\n'
                        'For example, the following SUBSTITUTE formula replaces all commas in text with '
                        'semicolons:\n'

                        '=SUBSTITUTE(text, ",", ";")'}

        self.functions_excel_dict["VALUE"] = \
            {"args": "VALUE(text)",
             "content": "This function converts a text string to a number.\n"

                        "This function is really helpful when it comes to converting text-formatted values "
                        "representing the numbers into numbers that can be used in other Excel formulas and "
                        "calculations."}

        self.functions_excel_dict["UPPER"] = \
            {"args": "UPPER(text)",
             "content": "This function converts all characters in a specified text string to upper case."}

        self.functions_excel_dict["LOWER"] = \
            {"args": "LOWER(text)",
             "content": "This function changes all uppercase letters in a text string to lowercase."}

        self.functions_excel_dict["PROPER"] = \
            {"args": "PROPER(text)",
             "content": "This function capitalizes the first letter of each word and converts all other "
                        "letters to lowercase \n"
                        "(more precisely, it capitalizes the letters that follow any character other than a letter)."}

        self.functions_excel_dict["LEFT"] = \
            {"args": "LEFT(text, [num_chars])",
             "content": "This function returns a specified number of characters from the beginning of "
                        "a text string."}

        self.functions_excel_dict["RIGHT"] = \
            {"args": "RIGHT(text, [num_chars]) ",
             "content": "This function returns a specified number of characters from the end of a "
                        "text string."}

        self.functions_excel_dict["MID"] = \
            {"args": "MID(text, start_num, num_chars)",
             "content": "This function returns a specific number of characters from a text string, "
                        "starting at any position that you specify.\n"

                        "In these functions, you supply the following arguments:\n"

                        "Text - a text string or a reference to a cell containing the characters you want to extract.\n"

                        "Start_num - indicates where to start (i.e. the position of the first character you want to "
                        "extract).\n"

                        "Num_chars - the number of characters you want to extract."}

        self.functions_excel_dict["IFERROR"] = \
            {"args": "IFERROR(value, value_if_error)",
             "content": "This function hecks if the formula or expression evaluates to an error. \n"

                        "If it does, the formula returns the value supplied in the value_if_error argument, "
                        "otherwise, the result of the formula is returned. \n"

                        "This function handles all possible Excel errors, "
                        "including VALUE, N/A, NAME, REF, NUM, and others."}

        self.functions_excel_dict["IFNA"] = \
            {"args": "IFNA (value, value_if_na)",
             "content": "it works similarly to IFERROR, but handles #N/A errors only."}

        self.functions_excel_dict["SUM"] = \
            {"args": "SUM(number1,[number2],…)",
             "content": "This function returns the sum of its arguments.\
             The arguments can be numbers, cells references or formula-driven numeric values."}

        self.functions_excel_dict["SUMIF"] = \
            {"args": "SUMIF(range, criteria, [sum_range]))",
             "content": "This function adds up the cells in a specified range that meet a certain condition. \n"
                        "The difference is that SUMIF can evaluate only a single criteria, "
                        "while SUMIFS allows for multiple criteria."}

        self.functions_excel_dict["SUMIFS"] = \
            {"args": "SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], …))",
             "content": "This function adds up the cells in a specified range that meet a certain condition. \n"
                        "The difference is that SUMIF can evaluate only a single criteria, "
                        "while SUMIFS allows for multiple criteria."}

        self.functions_excel_dict["RAND"] = \
            {"args": "RAND()",
             "content": "returns a random real (decimal) number between 0 and 1."}

        self.functions_excel_dict["RANDBETWEEN"] = \
            {"args": "RANDBETWEEN(bottom, top)",
             "content": "returns a random integer between the bottom and top numbers that you specify."}

        self.functions_excel_dict["ROUND"] = \
            {"args": "ROUND(number, num_digits)",
             "content": "round the number to the specified number of digits.\n"
                        "ROUND(15.55,1) rounds 15.55 to 15.6.\n"
                        "ROUND(15.55,-1) rounds 15.55 to the nearest 10 and returns 20 as the result\n"
                        "ROUND(15.55,0) rounds 15.55 to 16."}

        self.functions_excel_dict["ROUNDUP"] = \
            {"args": "ROUNDUP(number, num_digits)",
             "content": "round the number upward to the specified number of digits.\n"
                        "ROUNDUP(2.4, 0) -> 2\n"
                        "ROUNDUP(23.765, 2) -> 23.76\n"
                        "ROUNDUP(-56.58, -1) -> -50\n"
                        "ROUNDUP(-0.5, 0) -> -0"}

        self.functions_excel_dict["ROUNDDOWN"] = \
            {"args": "ROUNDDOWN(number, num_digits)",
             "content": "round the number downward to the specified number of digits.\n"
                        "ROUNDDOWN(2.4, 0) -> 3\n"
                        "ROUNDDOWN(23.765, 2) -> 23.77\n"
                        "ROUNDDOWN(-56.58, -1) -> -60\n"
                        "ROUNDDOWN(-0.5, 0) -> -1"}

        self.functions_excel_dict["MROUND"] = \
            {"args": "MROUND(number, multiple)",
             "content": "rounds the number upward or downward to the specified multiple.\n"
                        "ROUNDDOWN(15.67, 0.05) -> 15.65\n"
                        "ROUNDDOWN(15.67, 0.1) -> 15.70\n"
                        "ROUNDDOWN(15.67, 0.5) -> 15.50"}

        self.functions_excel_dict["FLOOR"] = \
            {"args": "FLOOR(number, significance)",
             "content": "round the number down to the specified multiple.\n"
                        "FLOOR(2.45, 2) -> 2\n"
                        "FLOOR(2.45, 0.2) -> 2.40\n"
                        "FLOOR(-2.45, 2) -> -4\n"
                        "FLOOR(-2.45, -2) -> -2"}

        self.functions_excel_dict["CEILING"] = \
            {"args": "CEILING(number, significance)",
             "content": "round the number up to the specified multiple\n"
                        "CEILING(2.45, 2) -> 4\n"
                        "CEILING(2.45, 0.2) -> 2.60\n"
                        "CEILING(-2.45, 2) -> -2\n"
                        "CEILING(-2.45, -2) -> -4"}

        self.functions_excel_dict["INT"] = \
            {"args": "INT(number)",
             "content": "round the number down to the nearest integer.\n"
                        "INT(2.45) -> 2\n"
                        "INT(-2.45) -> -3\n"
                        "INT(0.67) -> -0\n"
                        "INT(-0.67) -> -1"}

        self.functions_excel_dict["TRUNC"] = \
            {"args": "TRUNC(number, [num_digits])",
             "content": "truncate the number to a specified number of decimal places.\n"
                        "TRUNC(25.45, 1) -> 25.4\n"
                        "TRUNC(-25.45, 1) -> -25.4\n"
                        "TRUNC(25.45) -> -25\n"
                        "TRUNC(-25.45) -> -25\n"
                        "TRUNC(25.45, -1) -> -20\n"
                        "TRUNC(-25.45, -1) -> -20"}

        self.functions_excel_dict["ODD"] = \
            {"args": "ODD(number)",
             "content": "round the number up to the nearest even integer.\n"
                        "ODD(2.4) -> 3\n"
                        "ODD(-2.4) -> -3"}

        self.functions_excel_dict["EVEN"] = \
            {"args": "EVEN(number)",
             "content": "round the number up to the nearest odd integer.\n"
                        "EVEN(2.4) -> 4\n"
                        "EVEN(-2.4) -> -4"}

        self.functions_excel_dict["MIN"] = \
            {"args": "MIN(number1, [number2], …)",
             "content": "returns the minimal value from the list of arguments."}

        self.functions_excel_dict["MAX"] = \
            {"args": "MAX(number1, [number2], …)",
             "content": "returns the maximum value from the list of arguments"}

        self.functions_excel_dict["AVERAGE"] = \
            {"args": "AVERAGE(number1, [number2], …)",
             "content": "returns the average of the arguments."}

        self.functions_excel_dict["COUNT"] = \
            {"args": "COUNT(value1, [value2], …)",
             "content": "returns the number of numerical values (numbers and dates) in the list of arguments."}

        self.functions_excel_dict["COUNTA"] = \
            {"args": "COUNTA(value1, [value2], …)",
             "content": 'returns the number of non-empty cells in the list of arguments. \n'
                        'It counts cells containing any information, including error values and empty '
                        'text strings ("") returned by other formulas.'}

        self.functions_excel_dict["COUNTIF"] = \
            {"args": "COUNTIF(range, criteria)",
             "content": "counts the number of cells within the range that meet the specified criteria."}

        self.functions_excel_dict["COUNTIFS"] = \
            {"args": "COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2]…)",
             "content": "counts the number of cells that meet all of the specified criteria."}

        self.functions_excel_dict["DATE"] = \
            {"args": "DATE(year, month, day)",
             "content": "returns the serial number of a specified date.\n"
                        "DATE(2015, 5, 20) -> 20-May-2015\n"
                        "DATE(2015, 5, 20)-5 -> subtracts 5 days from May 20, 2015"}

        self.functions_excel_dict["DATEVALUE"] = \
            {"args": "DATEVALUE(date_text)",
             "content": "converts a date in the text format to a serial number that represents a date.\n"
                        'DATEVALUE("20-may-2015") -> 42144\n'
                        'DATEVALUE("5/20/2015") -> 42144'}

        self.functions_excel_dict["TODAY"] = \
            {"args": "TODAY()",
             "content": "function returns today's date,.\n"
                        'TODAY()+7'}

        self.functions_excel_dict["NOW"] = \
            {"args": "NOW()",
             "content": "function returns the current date and time. As well as TODAY"}

        self.functions_excel_dict["DAY"] = \
            {"args": "DAY(serial_number)",
             "content": "function returns a day of the month as an integer from 1 to 31.\n"
                        'DAY(DATE(2015,1,1)) -> 1-Jan-2015\n'
                        "DAY(TODAY()) - returns the day of today's date"}

        self.functions_excel_dict["MONTH"] = \
            {"args": "MONTH(serial_number)",
             "content": "function in Excel returns the month of a specified date as an integer ranging from 1 "
                        "(January) to 12 (December).\n"
                        "MONTH(TODAY()) - returns the current month."}

        self.functions_excel_dict["YEAR"] = \
            {"args": "YEAR(serial_number)",
             "content": "YEAR a year corresponding to a given date, as a number from 1900 to 9999.\n"
                        'YEAR("20-May-2015") - returns the year of the specified date.\n'
                        'YEAR(TODAY()) - returns the current year.'}

        self.functions_excel_dict["EOMONTH"] = \
            {"args": "EOMONTH(start_date, months)",
             "content": "function returns the last day of the month a given number of months from the start date.\n"
                        "EOMONTH(DATE(2015,4,15), 0) - returns the last day in April, 2015"}

        self.functions_excel_dict["WEEKDAY"] = \
            {"args": "WEEKDAY(serial_number,[return_type])",
             "content": "function returns the day of the week corresponding to a date, as a number"
                        "from 1 (Sunday) to 7 (Saturday).\n"

                        "WEEKDAY(TODAY()) - returns a number corresponding to today's day of the week; the week "
                        "begins on Sunday."}

        self.functions_excel_dict["WEEKNUM"] = \
            {"args": "WEEKNUM(serial_number, [return_type])",
             "content": "returns the week number of a specific date as an integer from 1 to 53.\n"
                        'WEEKNUM("1-Jan-2015")'}

        self.functions_excel_dict["DATEDIF"] = \
            {"args": "DATEDIF(start_date, end_date, unit)",
             "content": "function is specially designed to calculate the difference between two dates in days, "
                        "months or years.\n"
                        'DATEDIF("1-jan-13", 20-May-15, "m") -> 28'}

        self.functions_excel_dict["EDATE"] = \
            {"args": "EDATE(start_date, months)",
             "content": "function returns the serial number of the date that is the specified number of "
                        "months before or after the start date.\n"
                        "EDATE(TODAY(), -5) - subtracts 5 months from today's date."}

        self.functions_excel_dict["YEARFRAC"] = \
            {"args": "EDATE(start_date, months)",
             "content": "YEARFRAC(start_date, end_date, [basis])"}

        self.functions_excel_dict["WORKDAY"] = \
            {"args": "WORKDAY(start_date, days, [holidays])",
             "content": " function returns a date N workdays before or after the start date.\n"
                        "It automatically excludes weekend days from calculations as well as "
                        "any holidays that you specify."}

        self.functions_excel_dict["WORKDAY.INTL"] = \
            {"args": "WORKDAY.INTL(start_date, days, [weekend], [holidays])",
             "content": "is a more powerful variation of the WORKDAY"}

        self.functions_excel_dict["NETWORKDAYS"] = \
            {"args": "NETWORKDAYS(start_date, end_date, [holidays])",
             "content": " function returns the number of weekdays between two dates that you specify.\n"
                        "It automatically excludes weekend days and, optionally, the holidays."}

        self.functions_excel_dict["NETWORKDAYS.INTL"] = \
            {"args": "NETWORKDAYS.INTL(start_date, end_date, [weekend], [holidays])",
             "content": "is a more powerful modification of the NETWORKDAYS function. \n"
                        "It also returns the number of weekdays between two dates, "
                        "but lets you specify which days should be counted as weekends."}

    @staticmethod
    def a___________________allplan_recherche_attributs______():
        pass

    def search_xml_file(self, xml_folder_path: str) -> str:
        """

        recherche le nom du fichier xml
        :param xml_folder_path: chemin à vérifier
        :return: chemin complet valide
        """

        if xml_folder_path is None:
            return ""

        if not xml_folder_path.endswith("Xml\\"):
            return ""

        if not os.path.exists(xml_folder_path):
            return ""

        files_list = ["AttributeDefinitionCollectionLocal.xml",
                      f"AttributeDefinitionCollectionLocal_{self.langue.lower()}.xml",

                      "AttributeDefinitionCollectionLocal_en.xml",
                      "AttributeDefinitionCollectionLocal_fr.xml",

                      "AttributeDefinitionCollectionLocal_de.xml",
                      "AttributeDefinitionCollectionLocal_it.xml",
                      "AttributeDefinitionCollectionLocal_es.xml"]

        for file_name in files_list:

            path_full = f"{xml_folder_path}{file_name}"

            if os.path.exists(path_full):
                return path_full

        return ""

    def recherche_ligne_attribut(self, numero: str) -> int:

        search_number = self.attribute_model.findItems(numero, column=col_attr_number)

        if len(search_number) == 0:
            print(f"gestion_allplan -- recherche_ligne_attribut -- le numéro : {numero} n'a pas été trouvé")
            return -1

        if len(search_number) > 1:
            print(f"gestion_allplan -- recherche_ligne_attribut -- plusieurs numéros : {numero} a été trouvé")

        qs: QStandardItem = search_number[0]

        row_index: int = qs.row()

        return row_index

    def find_datas_by_number(self, number: str, key: str):

        if key not in [code_attr_number, code_attr_name, code_attr_group, code_attr_value, code_attr_datatype,
                       code_attr_option, code_attr_unit, code_attr_uid, code_attr_enumeration]:

            if key == "enumeration":
                return QStandardItemModel()
            return ""

        if not isinstance(number, str):
            if key == "enumeration":
                return QStandardItemModel()
            return ""

        datas: dict = self.attributes_dict.get(number, dict())

        if len(datas) == 0:
            if key == "enumeration":
                return QStandardItemModel()
            return ""

        if key == "enumeration":

            resultat = datas.get(key, QStandardItemModel())
        else:
            resultat = datas.get(key, "")

        return resultat

    def find_all_datas_by_number(self, number: str) -> dict:

        if not isinstance(number, str):
            return dict()

        datas: dict = self.attributes_dict.get(number, dict())

        return datas

    def find_number_by_name(self, name: str) -> str:

        if not isinstance(name, str):
            return ""

        search_start = self.attribute_model.index(0, col_attr_name)
        search_name = self.attribute_model.match(search_start, Qt.DisplayRole, name, 1, Qt.MatchExactly)

        if len(search_name) == 0:
            search_name = self.attribute_model.match(search_start, Qt.DisplayRole, name, 1, Qt.MatchFixedString)

        if len(search_name) == 0:
            return ""

        qm_name = search_name[0]

        qm_number = self.attribute_model.index(qm_name.row(), col_attr_number)

        if not qm_check(qm_number):
            return ""

        return qm_number.data()

    @staticmethod
    def a___________________allplan_tooltips_attributs______():
        pass

    def gestion_tooltip_formule(self, widget: QPlainTextEdit):
        """
        Permet d'affiche en tooltip le nom de l'attribut
        :param widget: widget sur lequel gérer les tooltips
        :return: None
        """

        # Mise en mémoire du texte sélectionné
        texte_selectionner = widget.textCursor().selectedText()

        # Vérification que le texte contient au moins 3 caractères
        if len(texte_selectionner) == 0:
            widget.setToolTip(self.traduction_formule_allplan(widget.toPlainText()))
            return

        if len(texte_selectionner) < 3:
            widget.setToolTip(self.tr("Sélectionner un attribut '@xxx@' et l'info-bulle affichera son nom !"))
            return

        if texte_selectionner == widget.toPlainText() and texte_selectionner.count("@") >= 2:
            widget.setToolTip(self.traduction_formule_allplan(widget.toPlainText()))
            return

        for texte_original, texte_final in self.piece_remplace.items():
            if texte_original in texte_selectionner:
                widget.setToolTip(texte_final)
                return

        for function_name, function_data in self.functions_excel_dict.items():

            if not isinstance(function_name, str) and not isinstance(function_data, dict):
                continue

            if function_name in texte_selectionner:
                function_args = function_data.get("args", "")
                function_detail = function_data.get("content", "")

                function_txt = self.tr("Fonction Excel")
                argument_txt = self.tr("Argument")
                detail_txt = self.tr("Détail de la fonction")

                tooltip = ("<p style='white-space:pre'>"
                           f"{function_txt} : <b>{function_name}</b><br>"
                           f"{argument_txt} : <b>{function_args}</b><br>"
                           f"{detail_txt} : <br><br><b>{function_detail}</b>")

                widget.setToolTip(tooltip)

                return

        for function_name, function_data in self.functions_python_dict.items():

            if not isinstance(function_name, str) and not isinstance(function_data, dict):
                continue

            if function_name in texte_selectionner:
                function_args = function_data.get("args", "")
                function_detail = function_data.get("content", "")

                function_txt = self.tr("Fonction Python")
                argument_txt = self.tr("Argument")
                detail_txt = self.tr("Détail de la fonction")

                tooltip = ("<p style='white-space:pre'>"
                           f"{function_txt} : <b>{function_name}</b><br>"
                           f"{argument_txt} : <b>{function_args}</b><br>"
                           f"{detail_txt} : <br><br><b>{function_detail}</b>")

                widget.setToolTip(tooltip)

                return

        for function_name, function_data in self.functions_vbs_dict.items():

            if not isinstance(function_name, str) and not isinstance(function_data, dict):
                continue

            if function_name in texte_selectionner:
                function_args = function_data.get("args", "")
                function_detail = function_data.get("content", "")

                function_txt = self.tr("Fonction VBS")
                argument_txt = self.tr("Argument")
                detail_txt = "Détail de la fonction"

                tooltip = ("<p style='white-space:pre'>"
                           f"{function_txt} : <b>{function_name}</b><br>"
                           f"{argument_txt} : <b>{function_args}</b><br>"
                           f"{detail_txt} : <br><br><b>{function_detail}</b>")

                widget.setToolTip(tooltip)

                return

        # Vérification qu'il y a bien seulement 2 @
        if texte_selectionner.count("@") != 2:

            texte_tmp = texte_selectionner.replace("@", "")

            try:

                numero_attribut = str(int(texte_tmp))

            except Exception:

                widget.setToolTip(self.tr("Sélectionner un attribut '@xxx@' et l'info-bulle affichera son nom !"))
                return

        elif "@OBJ@" in texte_selectionner:

            obj_names_dict = self.enumeration_translations.get("OBJ", dict())

            formula = self.formula_translate_function(formula=texte_selectionner,
                                                      function_name="OBJ",
                                                      replacement=obj_names_dict)
            if formula != texte_selectionner:
                widget.setToolTip(formula)
                return

            widget.setToolTip(self.tr("Aucun numéro trouvé dans le texte."))
            return

        else:

            if "@GW@" in texte_selectionner:
                texte_selectionner.replace('@GW', '@209@')

            recherche = re.search(r'@(\d+)@', texte_selectionner)

            if recherche:
                numero_attribut: str = recherche.group(1)
            else:
                widget.setToolTip(self.tr("Aucun numéro trouvé dans le texte."))
                return

        # Vérification que le numéro d'attribut est dans le dictionnaire des attributs
        if numero_attribut not in self.attributes_dict:
            widget.setToolTip(self.tr("Attention, Numéro d'attribut Inconnu !"))
            return

        if code_attr_tooltips not in self.attributes_dict[numero_attribut]:
            return

        data_attributes: dict = self.attributes_dict[numero_attribut]

        if not isinstance(data_attributes, dict):
            return

        if numero_attribut in self.enumeration_translations:

            names_dict = self.enumeration_translations.get(numero_attribut, dict())

            texte_selectionner = self.formula_translate_function(formula=texte_selectionner,
                                                                 function_name=numero_attribut,
                                                                 replacement=names_dict)

            if code_attr_name not in self.attributes_dict[numero_attribut]:
                tooltips = data_attributes.get(code_attr_tooltips, "")

            else:

                name = self.attributes_dict[numero_attribut][code_attr_name]

                tooltips_start = texte_selectionner.replace("@209@", name)

                tooltips_end = data_attributes.get(code_attr_tooltips, "")

                tooltips_end = tooltips_end.replace("<p style='white-space:pre'>", "")

                tooltips = (f"<p style='white-space:pre'>{tooltips_start}<br>"
                            f"----------------------------------<br><br>"
                            f"{tooltips_end}")

        else:

            tooltips = data_attributes.get(code_attr_tooltips, "")

        widget.setToolTip(tooltips)

    def traduire_unite(self, unite_actuelle: str) -> str:

        if unite_actuelle == "Qt":
            return self.tr("Qt")

        return unite_actuelle

    def traduire_valeur_232(self, value_current="", region="", default=False) -> str:

        if not isinstance(value_current, str) or not isinstance(region, str) or not isinstance(default, bool):
            return ""

        # -------------------------------------

        if default:

            translation_list = translation_232.get(self.langue, None)

            if not isinstance(translation_list, list):
                return ""

            value_translated = translation_list[0]

            return value_translated

        # -------------------------------------

        if self.langue not in translation_232:
            return value_current

        translation_list_end = translation_232[self.langue]

        if not isinstance(translation_list_end, list):
            return ""

        translation_list_end_count = len(translation_list_end)

        value_current = value_current.strip()
        region = region.upper()

        # -------------------------------------

        if value_current.isnumeric():

            try:

                value_int = int(value_current)

            except Exception:
                return value_current

            if value_int < translation_list_end_count:
                value_translated = translation_list_end[value_int]

                return value_translated

            return value_current

        # -------------------------------------

        if region == self.langue and value_current in translation_list_end:
            return value_current

        # -------------------------------------

        if region in translation_232:

            translation_list_start = translation_232[region]

            if not isinstance(translation_list_start, list):
                return value_current

            if len(translation_list_start) != translation_list_end_count:
                return value_current

            if value_current in translation_list_start:
                index_current = translation_list_start.index(value_current)

                value_translated = translation_list_end[index_current]

                return value_translated

        # -------------------------------------

        for language, translation_list in translation_232.items():

            if not isinstance(translation_list, list):
                continue

            if len(translation_list) != translation_list_end_count:
                return value_current

            if value_current in translation_list and language == self.langue:
                return value_current

            if value_current in translation_list:
                index_current = translation_list.index(value_current)

                value_translated = translation_list_end[index_current]

                return value_translated

        return value_current

    def traduire_valeur_233(self, value_current="", region="", default=False) -> str:

        if not isinstance(value_current, str) or not isinstance(region, str) or not isinstance(default, bool):
            return ""

        # -------------------------------------

        if default:

            translation_list = translation_233.get(self.langue, None)

            if not isinstance(translation_list, list):
                return ""

            value_translated = translation_list[0]

            return value_translated

        # -------------------------------------

        if self.langue not in translation_233:
            return value_current

        translation_list_end = translation_233[self.langue]

        if not isinstance(translation_list_end, list):
            return value_current

        translation_list_end_count = len(translation_list_end)

        value_current = value_current.strip()
        region = region.upper()

        # -------------------------------------

        if value_current.isnumeric():

            try:

                value_int = int(value_current)

            except Exception:
                return value_current

            if value_int < translation_list_end_count:
                value_translated = translation_list_end[value_int]

                return value_translated

            return value_current

        # -------------------------------------

        if region == self.langue and value_current in translation_list_end:
            return value_current

        # -------------------------------------

        if region in translation_233:

            translation_list_start = translation_233[region]

            if not isinstance(translation_list_start, list):
                return value_current

            if len(translation_list_start) != translation_list_end_count:
                return value_current

            if value_current in translation_list_start:
                index_current = translation_list_start.index(value_current)

                value_translated = translation_list_end[index_current]

                return value_translated

        # -------------------------------------

        for language, translation_list in translation_233.items():

            if not isinstance(translation_list, list):
                continue

            if len(translation_list) != translation_list_end_count:
                return value_current

            if value_current in translation_list and language == self.langue:
                return value_current

            if value_current in translation_list:
                index_current = translation_list.index(value_current)

                value_translated = translation_list_end[index_current]

                return value_translated

        return value_current

    def traduire_valeur_235(self, value_current="", region="", default=False) -> str:

        if not isinstance(value_current, str) or not isinstance(region, str) or not isinstance(default, bool):
            return ""

        # -------------------------------------

        if default:

            translation_list = translation_235.get(self.langue, None)

            if not isinstance(translation_list, list):
                return ""

            value_translated = translation_list[0]

            return value_translated

        # -------------------------------------

        if self.langue not in translation_235:
            return value_current

        translation_list_end = translation_235[self.langue]

        if not isinstance(translation_list_end, list):
            return ""

        translation_list_end_count = len(translation_list_end)

        value_current = value_current.strip()
        region = region.upper()

        # -------------------------------------

        if value_current.isnumeric():

            try:

                value_int = int(value_current)

            except Exception:
                return value_current

            if value_int < translation_list_end_count:
                value_translated = translation_list_end[value_int]

                return value_translated

            return value_current

        # -------------------------------------

        if region == self.langue and value_current in translation_list_end:
            return value_current

        # -------------------------------------

        if region in translation_235:

            translation_list_start = translation_235[region]

            if not isinstance(translation_list_start, list):
                return value_current

            if len(translation_list_start) != translation_list_end_count:
                return value_current

            if value_current in translation_list_start:
                index_current = translation_list_start.index(value_current)

                value_translated = translation_list_end[index_current]

                return value_translated

        # -------------------------------------

        for language, translation_list in translation_235.items():

            if not isinstance(translation_list, list):
                continue

            if len(translation_list) != translation_list_end_count:
                return value_current

            if value_current in translation_list and language == self.langue:
                return value_current

            if value_current in translation_list:
                index_current = translation_list.index(value_current)

                value_translated = translation_list_end[index_current]

                return value_translated

        return value_current

    @staticmethod
    def a___________________aim______():
        pass

    def aim_get_attributes(self):

        settings = QSettings('Allplan - Information Manager', 'Settings')
        chemin_py_pam_bdd = settings.value('chemin_bdd', "")

        if chemin_py_pam_bdd == "":
            return

        if not os.path.exists(chemin_py_pam_bdd):
            return

        try:
            with sqlite3.connect(chemin_py_pam_bdd) as connexion:

                cursor = connexion.cursor()

                self.aim_get_other(cursor=cursor)
                self.aim_get_combo(cursor=cursor)
                self.aim_get_radio(cursor=cursor)

                cursor.close()

        except Exception as error:

            print(f"gestion_allplan -- recherche_attribut_aim --> Erreur : {error}")

            try:

                cursor.close()

            except Exception as error:
                print(f"gestion_allplan -- recherche_attribut_aim --> Erreur 2 : {error}")
                return

    def aim_get_combo(self, cursor: sqlite3.Cursor):
        try:

            cursor.execute("""SELECT num_attr, titre_attr, liste_attr FROM INFOS_COMBOBOX""")

            result = cursor.fetchall()

            if not isinstance(result, list):
                return

            for item_datas in result:

                if not isinstance(item_datas, tuple):
                    continue

                if len(item_datas) != 3:
                    continue

                number = item_datas[0]

                if not isinstance(number, str):
                    continue

                if number in self.aim_dict:
                    continue

                title = item_datas[1]

                if not isinstance(title, str):
                    continue

                enumaration_str = item_datas[2]

                if not isinstance(enumaration_str, str):
                    continue

                if len(enumaration_str) > 0:
                    enumeration_list: list = enumaration_str.split("\n")
                else:
                    enumeration_list = list()

                self.aim_dict[number] = [title, enumeration_list]

        except Exception as error:
            print(f"gestion_allplan -- aim_get_combo --> Erreur: {error}")

    def aim_get_radio(self, cursor: sqlite3.Cursor):

        try:

            cursor.execute(f"""SELECT num_attr, titre_attr, 
            nom_radio_1, nom_radio_2, nom_radio_3, nom_radio_4, nom_radio_5, nom_radio_6 FROM INFOS_RADIO""")

            result = cursor.fetchall()

            if not isinstance(result, list):
                return

            for item_datas in result:

                if not isinstance(item_datas, tuple):
                    continue

                if len(item_datas) != 8:
                    continue

                number = item_datas[0]

                if not isinstance(number, str):
                    continue

                if number in self.aim_dict:
                    continue

                title = item_datas[1]

                if not isinstance(title, str):
                    continue

                enumeration_list = list()

                for item_index in range(2, len(item_datas)):
                    text = item_datas[item_index]

                    if not isinstance(text, str):
                        break

                    if text == "":
                        break

                    enumeration_list.append(text)

                self.aim_dict[number] = [item_datas[1], enumeration_list]

        except Exception as error:
            print(f"gestion_allplan -- aim_get_radio --> Erreur: {error}")

    def aim_get_other(self, cursor: sqlite3.Cursor):
        try:

            for categorie in ["INFOS_LINEEDIT", "INFOS_CHECKBOX", "INFOS_FORMATAGE"]:

                cursor.execute(f"""SELECT num_attr, titre_attr FROM {categorie}""")

                resultat = cursor.fetchall()

                if not isinstance(resultat, list):
                    continue

                for item_datas in resultat:

                    if not isinstance(item_datas, tuple):
                        continue

                    if len(item_datas) != 2:
                        continue

                    number = item_datas[0]

                    if not isinstance(number, str):
                        continue

                    if number in self.aim_dict:
                        continue

                    title = item_datas[1]

                    if not isinstance(title, str):
                        continue

                    self.aim_dict[number] = [item_datas[1], []]

        except Exception as error:
            print(f"gestion_allplan -- aim_get_other --> Erreur: {error}")

    @staticmethod
    def a___________________allplan_formules______():
        pass

    def traduction_formule_allplan(self, formula: str, format_on=True):
        """
        Permet de traduire les formules d'allplan
        :param formula: texte saisie par l'utilisateur à convertir
        :return: Formule convertie
        """

        if formula == "":
            return ""

        liste_attributs = re.findall("@(.*?)@", formula)

        if len(liste_attributs) == 0:
            return formula

        liste_attributs = list(set(liste_attributs))

        texts_list = self.get_all_text_from_formula(formula=formula)

        if len(texts_list) != 0:
            formula = self.formula_exclude_text(formula=formula, texts_list=texts_list)

        formula = self.formula_translate(formula=formula, fonction_dict=self.piece_remplace)

        for texte_original, texte_final in self.tooltips_remplace.items():
            if texte_original in formula:
                formula = formula.replace(texte_original, texte_final)

        for function_name in self.functions_excel_dict:

            if not isinstance(function_name, str):
                continue

            function_txt = self.tr("Fonction Excel")

            if f"x:{function_name}" in formula:
                formula = formula.replace(f"x:{function_name}", f"{function_txt} : {function_name}")
                continue

            if f"x: {function_name}" in formula:
                formula = formula.replace(f"x: {function_name}", f"{function_txt} : {function_name}")

        for function_name in self.functions_python_dict:

            if not isinstance(function_name, str):
                continue

            function_txt = self.tr("Fonction Python")

            if f"p:{function_name}" in formula:
                formula = formula.replace(f"p:{function_name}", f"{function_txt} : {function_name}")
                continue

            if f"p: {function_name}" in formula:
                formula = formula.replace(f"p: {function_name}", f"{function_txt} : {function_name}")

        for function_name in self.functions_vbs_dict:

            if not isinstance(function_name, str):
                continue

            function_txt = self.tr("Fonction VBS")

            if f"v:{function_name}" in formula:
                formula = formula.replace(f"v:{function_name}", f"{function_txt} : {function_name}")
                continue

            if f"v: {function_name}" in formula:
                formula = formula.replace(f"v: {function_name}", f"{function_txt} : {function_name}")

        formula = formula.replace("  ", " ").strip()

        if "_IF_" in formula:
            texte_si = self.tr("Si")
            formula = formula.replace("_IF_", texte_si)

        if "_ELSE_" in formula:
            texte_sinon = self.tr("Sinon")
            formula = formula.replace("_ELSE_", f'\n      {texte_sinon} ')

        for key, valeur in dict_html.items():
            if key in formula:
                formula = formula.replace(key, valeur)

        formula = self.formula_translate(formula=formula, fonction_dict=self.fonction_replace)

        for numero_attribut in liste_attributs:

            if numero_attribut == "OBJ":
                obj_names_dict = self.enumeration_translations.get("OBJ", dict())

                formula = self.formula_translate_function(formula=formula,
                                                          function_name="OBJ",
                                                          replacement=obj_names_dict)

                formula = formula.replace("@OBJ@", "<b>@OBJ@</b>")

                continue

            if numero_attribut in self.enumeration_translations:
                names_dict = self.enumeration_translations.get(numero_attribut, dict())

                formula = self.formula_translate_function(formula=formula,
                                                          function_name=numero_attribut,
                                                          replacement=names_dict)

            if numero_attribut == "GW":
                numero_attribut = "209"
                formula = formula.replace("@GW@", "@209@")

            if "[" in numero_attribut and "]" in numero_attribut:

                end_attribute = numero_attribut.index("[")

                numero_attribut = numero_attribut[:end_attribute]

                numero_attribut = numero_attribut.strip()

                special_attribute = True

            else:
                special_attribute = False

            try:
                int(numero_attribut)
            except ValueError:
                continue

            if numero_attribut not in self.attributes_dict:
                continue

            titre, _ = self.aim_dict.get(numero_attribut, ["", list()])

            if titre != "":

                nom_attribut = f"[{titre}]"

            else:

                if code_attr_name not in self.attributes_dict[numero_attribut]:
                    continue

                nom_attribut = self.attributes_dict[numero_attribut][code_attr_name]

            if special_attribute:
                formula = formula.replace(f"@{numero_attribut}", f" <b>{nom_attribut}</b>").replace("]@", "]")
            else:
                formula = formula.replace(f"@{numero_attribut}@", f" <b>{nom_attribut}</b> ")

        if len(texts_list) != 0:
            formula = self.formula_restore_text(formula=formula, texts_list=texts_list)

        formula = self.formattage_formule(formula)

        if format_on:
            return f"<p style='white-space:pre'>{formula}"

        return formula

    @staticmethod
    def formattage_formule(text):

        nb_max = 200

        if len(text) <= nb_max:
            return text

        lines = text.split('\n')
        truncated_lines = []

        for line in lines:
            words = line.split("(")
            current_line = words[0]

            for word in words[1:]:
                if len(current_line) + len(word) + 1 <= nb_max:
                    current_line += '(' + word
                else:
                    truncated_lines.append(current_line)
                    current_line = '(' + word

            truncated_lines.append(current_line)

        return '<br>'.join(truncated_lines)

    def verification_formule(self, formula: str):

        if formula == "":
            return ""

        # Vérification si formule = "1" ==> "1"
        try:
            int(formula)
            return ""
        except ValueError:
            pass

        error_message = list()

        check_word = True

        # -------------------
        # Special
        # -------------------
        try:
            pattern_special_number = r'@(\d+)\s*\[\s*(\d+)\s*\]@'
            formula = re.sub(pattern_special_number, "", formula)

            pattern_special_string = r'@(\d+)\s*\[\s*"([^"]*)"\s*\]@'
            formula = re.sub(pattern_special_string, "", formula)

        except Exception:
            pass

        # -------------------
        # Check quote
        # -------------------

        if '"' in formula:

            if not formula.count('"') % 2 == 0:

                formula_without_quotes = formula
                error_message.append(self.tr("le nombre de guillemets n'est pas correct"))
                check_word = False

            else:

                formula_without_quotes = re.sub(r'"[^"]*"', '', formula)

        else:
            formula_without_quotes = formula

        # -------------------
        # Check @@
        # -------------------

        if "@" in formula:

            errors_list = self.is_formula_valid(formula=formula)

            if not formula.count("@") % 2 == 0:

                formula_without_attrib = formula_without_quotes
                error_message.append(self.tr("le nombre de '@' n'est pas correct"))
                check_word = False

            elif len(errors_list) != 0:

                formula_without_attrib = formula_without_quotes
                error_message.extend(errors_list)
                check_word = False

            else:

                formula_without_attrib = re.sub(r'@\d+@', '', formula_without_quotes)

                formula_without_space = formula_without_quotes.replace(" ", "")

                matches = re.finditer(r"@(.*?)@", formula_without_space)

                text_part_1 = self.tr("La syntaxe est invalide")

                unknown_txt = self.tr("Attribut inconnu")
                unknown_attributes = list()

                special_attributes = ["@OBJ@", "@VOB@", "@GW@"]
                symbol_valid_befor = ["&", "|", "+", "-", "*", "/", "=", ">", "<", "!", "(", ")", ""]
                symbol_valid_after = ["&", "|", "+", "-", "*", "/", "=", ">", "<", ")", ";", "^", ""]

                for match in matches:

                    attribute = match.group()

                    start, end = match.span()

                    before = formula_without_space[start - 1] if start > 0 else ''

                    after = formula_without_space[end] if end < len(formula_without_space) else ''

                    if before not in symbol_valid_befor:
                        error_message.append(f"{text_part_1} : {before}{attribute}")

                    if after not in symbol_valid_after:
                        error_message.append(f"{text_part_1} : {attribute}{after}")

                    if attribute.upper() in special_attributes:
                        formula_without_attrib = formula_without_attrib[:start] + formula_without_attrib[end:]
                        continue

                    number = attribute.replace("@", "")

                    if number in unknown_attributes:
                        continue

                    if number in self.attributes_dict:
                        continue

                    if not isinstance(number, str):
                        continue

                    if not number.isdigit():
                        convert = self.formula_match_name(name=number)

                        if convert != "":
                            continue

                    unknown_attributes.append(number)
                    error_message.append(f"{unknown_txt} : @{number}@")

        else:

            formula_without_attrib = formula_without_quotes

        # -------------------
        # Check parenthesis
        # -------------------

        if not formula.count("(") == formula.count(")"):
            error_message.append(self.tr("le nombre de parenthèses n'est pas correct"))

        # -------------------
        # Check classic error
        # -------------------

        if "_ELSE_IF_" in formula:
            error_message.append(self.tr("La condition doit s'écrire _ELSE__IF_"))

        if "_ELSE(" in formula:
            error_message.append(self.tr("La condition doit s'écrire _ELSE_("))

        if "_IF(" in formula:
            error_message.append(self.tr("La condition doit s'écrire _IF_("))

        for caractere in liste_caracteres_fin:
            if formula.endswith(caractere):
                error_message.append(self.tr("La formule se termine par un caractère non valide"))
                break

        if "_ELSE_" in formula_without_attrib:
            formula_without_attrib = formula_without_attrib.replace("_ELSE_", " ")

        # -------------------
        # Check bad syntaxe
        # -------------------

        if check_word:
            words = re.findall(r'\b\w+\b', formula_without_attrib)

            for word in words:

                if not isinstance(word, str):
                    continue

                if word == "p" and "p:" in formula_without_attrib:
                    continue

                if word == "v" and "v:" in formula_without_attrib:
                    continue

                if word == "x" and "x:" in formula_without_attrib:
                    continue

                if (word in fonction_list or word in self.functions_python_dict or word in self.functions_vbs_dict
                        or word.upper() in self.functions_excel_dict):
                    continue

                if word.isdigit():
                    continue

                error_message.append(word + " " + self.tr("n'est pas correct"))

                if len(error_message) > 20:
                    error_message.append("...")
                    break

        # -------------------
        # Define message
        # -------------------

        if len(error_message) == 0:
            return ""

        return "- " + "\n- ".join(error_message)

    def formula_replace_all_name(self, formula: str) -> str:

        texts_list = self.get_all_text_from_formula(formula=formula)

        if len(texts_list) != 0:
            formula_tmp = self.formula_exclude_text(formula=formula, texts_list=texts_list)
        else:
            formula_tmp = formula

        attribute_list = re.findall("@(.*?)@", formula_tmp)
        attribute_list = list(set(attribute_list))

        if len(attribute_list) == 0:
            return formula

        attribute_unknown = [number for number in attribute_list
                             if number not in self.attributes_dict and
                             number != "" and number != "OBJ" and number != "VOB" and number != "GW"]

        if len(attribute_unknown) == 0:
            return formula

        for name in attribute_unknown:

            if not isinstance(name, str):
                continue

            if name.isdigit():
                continue

            number = self.formula_match_name(name=name)

            if number == "":
                continue

            formula_tmp = formula_tmp.replace(f"@{name}@", f"@{number}@")

        if len(texts_list) != 0:
            formula_tmp = self.formula_restore_text(formula=formula_tmp, texts_list=texts_list)

        return formula_tmp

    def formula_match_name(self, name: str) -> str:

        start_search = self.attribute_model.index(0, col_attr_name)

        search = self.attribute_model.match(start_search, Qt.DisplayRole, name, -1,
                                            Qt.MatchContains)

        if len(search) == 0:
            return ""

        for qm_name in search:

            if not isinstance(qm_name, QModelIndex):
                continue

            name_current = qm_name.data()

            if not isinstance(name_current, str):
                continue

            if name_current.lower() != name.lower():
                continue

            qm_number = self.attribute_model.index(qm_name.row(), col_attr_number)

            if not qm_check(qm_number):
                continue

            number = qm_number.data()

            if not isinstance(number, str):
                continue

            return number

        return ""

    def is_formula_valid(self, formula: str) -> list:

        formula = formula.replace(" ", "")

        invalid_pattern = r'(@\d+@)\s*([A-Za-zÀ-ÿ0-9\'"\(@,])'

        errors_list = list()

        text_part_1 = self.tr("La syntaxe est invalide")
        text_part_2 = self.tr("Caractère problématique")

        try:

            matches = re.findall(invalid_pattern, formula)

            if not matches:
                return errors_list

            for segment, invalid_char in matches:

                errors_text = f"{text_part_1} : {segment} -> {text_part_2} : {invalid_char}"

                if errors_text not in errors_list:
                    errors_list.append(errors_text)

        except Exception:
            pass

        return errors_list

    def convertir_formule_bdd(self, formule: str):
        """
        Permet de séparer les formules métré et des formules de matériaux dyn
        :param formule: formule à analyser
        :return: tuple( formule, materiaux_dyn)
        :rtype: tuple
        """

        formule_metre = materiaux_dyn = quantite = objet = ""

        nb_char = len(formule)

        if nb_char == 0:
            return formule_metre, materiaux_dyn, objet, quantite

        if "CAD." not in formule:
            return formule_metre, materiaux_dyn, objet, quantite

        if "\r\n" in formule:
            formule = formule.replace("\r\n", "")

        resultat = {}
        cad_occurrences = formule.split("CAD.")

        for occurrence in cad_occurrences[1:]:  # On ignore le premier élément vide résultant du split
            cle, valeur = occurrence.split(":", 1)
            cle = cle.strip()
            valeur = valeur.strip()
            resultat[cle] = valeur

        if len(resultat) == 0:
            return formule_metre, materiaux_dyn, objet, quantite

        for attribut, valeur in resultat.items():

            if attribut in liste_for:
                formule_metre = self.convertir_formule(valeur)
                continue

            if attribut in liste_qte:
                quantite = self.convertir_formule(valeur)
                continue

            if attribut in liste_mat:
                materiaux_dyn = self.convertir_formule(valeur)
                continue

            if attribut in liste_obj:
                objet = self.convertir_formule(valeur)
                continue

        return formule_metre, materiaux_dyn, objet, quantite

    def convertir_formule(self, formula: str):
        """

        :param formula:
        :return: formule convertie
        """

        if formula == "":
            return formula

        if formula in self.formula_dict:
            return self.formula_dict[formula]

        if len([ele for ele in formula if ele.isalpha()]) == 0:
            self.formula_dict[formula] = formula
            return formula

        # Vérification si formule = "Surface" ==> "@229@"
        if formula in self.conversions_dict:
            texte_final = self.conversions_dict[formula]

            self.formula_dict[formula] = texte_final

            return texte_final

        try:
            int(formula)
            return formula
        except ValueError:
            pass

        texts_list: list = self.get_all_text_from_formula(formula=formula)

        texts_count = len(texts_list)

        formula = self.formula_exclude_text(texts_list=texts_list, formula=formula)

        try:
            formula = re.sub(self.pattern, lambda x: self.conversions_dict[x.group()], formula)
        except re.error as error:
            print(f"gestion_allplan -- convertir_formule -- erreur : {error}")

        if texts_count == 0:
            return formula

        formula = self.formula_restore_text(texts_list=texts_list, formula=formula)

        if "><" in formula:
            formula = formula.replace("><", "<>")

        self.formula_dict[formula] = formula

        return formula

    @staticmethod
    def get_all_text_from_formula(formula: str) -> list:

        if not isinstance(formula, str):
            return list()

        try:
            texts_list = re.findall('"([^"]*)"', formula)

            texts_list.sort(key=len, reverse=True)

            return texts_list

        except Exception:
            return list()

    @staticmethod
    def formula_translate(formula: str, fonction_dict) -> str:

        for formula_function, formula_translation in fonction_dict.items():

            try:

                pattern = r'\b' + re.escape(formula_function) + r'\b'

                formula = re.sub(pattern, formula_translation, formula, flags=re.IGNORECASE)

            except Exception:
                continue

        return formula

    @staticmethod
    def formula_translate_function(formula: str, function_name: str, replacement: dict) -> str:

        if not isinstance(formula, str) or not isinstance(replacement, dict) or not isinstance(function_name, str):
            return ""

        if len(replacement) == 0 or formula == "" or function_name == "":
            return formula

        pattern = fr'(@{re.escape(function_name)}@\s*=\s*)(\d{{1,5}})'

        try:

            def replace_match(match):
                prefix = match.group(1)
                number = match.group(2)
                return prefix + replacement.get(number, number)

            result_text = re.sub(pattern, replace_match, formula)

            return result_text

        except Exception:
            return formula

    def formula_format(self, formula: str) -> str:

        texts_list = self.get_all_text_from_formula(formula=formula)

        if len(texts_list) != 0:
            formula = self.formula_exclude_text(formula=formula, texts_list=texts_list)

        for formula_function in fonction_list:

            try:

                pattern = r'\b' + re.escape(formula_function) + r'\b'

                formula = re.sub(pattern, formula_function, formula, flags=re.IGNORECASE)

            except Exception:
                continue

        if len(texts_list) != 0:
            formula = self.formula_restore_text(formula=formula, texts_list=texts_list)

        return formula

    @staticmethod
    def formula_exclude_text(formula: str, texts_list: list) -> str:

        if not isinstance(formula, str):
            return ""

        if not isinstance(texts_list, list):
            return ""

        if len(texts_list) == 0:
            return formula

        nb_textes = len(texts_list)

        if nb_textes == 0:
            return formula

        for index_texte, texte in enumerate(texts_list):

            texte_analyse = f'"{texte}"'

            if texte_analyse in formula:
                formula = formula.replace(texte_analyse, f"$¤{index_texte}¤$")

        return formula

    @staticmethod
    def formula_restore_text(formula: str, texts_list: list) -> str:

        if not isinstance(formula, str):
            return ""

        if not isinstance(texts_list, list):
            return ""

        if len(texts_list) == 0:
            return formula

        nb_textes = len(texts_list)

        if nb_textes == 0:
            return formula

        for index_texte, texte in enumerate(texts_list):
            texte_tps = f"$¤{index_texte}¤$"

            formula = formula.replace(texte_tps, f'"{texte}"')

        return formula

    def convert_unit(self, unit: str):

        # todo traduction
        if unit == "Qt" and self.langue == "EN":
            return "Pcs"

        elif unit == "Pcs" and self.langue != "EN":
            return "Qt"

        unite_convert = dict_unites.get(unit.lower(), self.traduire_unite(unit))
        return unite_convert

    def recherche_formule_defaut(self, unite: str):
        """
        conversion d'une unité
        :param unite: unité à convertir
        :return: unité convetie
        :rtype: str
        """

        unite_convert = dict_unites.get(unite.lower(), self.traduire_unite(unite))
        formule = dict_formules_by_unite.get(unite_convert, "1")

        return formule

    # @staticmethod
    # def a___________________apn______():
    #     pass
    #
    # def get_real_path_of_apn_file(self, file_path: str, version_name: str, is_cat_folder=False, show_msg=True) -> str:
    #     """
    #
    #     :param file_path: Chemin du fichier APN ou PRJ
    #     :param version_name: Chemin du dossier prj dans lequel rechercher
    #     :param is_cat_folder: renvoyer le chemin du dossier SmartCatalog
    #     :param show_msg: Show avertissement message
    #     :return: le chemin du dossier PRJ ou SmartCatalog
    #     """
    #
    #     # -------------------
    #     # File Path check
    #     # -------------------
    #
    #     if not isinstance(file_path, str):
    #         print("allplan_manage -- get_real_path_of_apn_file -- not isinstance(file_path, str)")
    #         return ""
    #
    #     if not os.path.exists(file_path):
    #         print("allplan_manage -- get_real_path_of_apn_file -- not os.path.exists(file_path)")
    #         return ""
    #
    #     file_name = find_filename(file_path)
    #
    #     # -------------------
    #     # Prj file check
    #     # -------------------
    #
    #     if file_path.endswith(".prj"):
    #
    #         try:
    #             with open(file_path, "r") as file:
    #
    #                 datas_config_apn: list = file.readlines()
    #
    #         except Exception as erreur:
    #             print(f"allplan_manage -- get_real_path_of_apn_file -- erreur : {erreur}")
    #             return ""
    #
    #         if len(datas_config_apn) < 3:
    #             print("allplan_manage -- get_real_path_of_apn_file -- erreur : Fichier non valide")
    #             return ""
    #
    #         tmp_path: str = datas_config_apn[0]
    #         tmp_path = tmp_path.replace("\n", "")
    #
    #         if not tmp_path.endswith("\\"):
    #             tmp_path += "\\"
    #
    #         tmp_prj_path = f"{tmp_path}{file_name}.prj\\"
    #
    #         if not os.path.exists(tmp_prj_path):
    #             print("allplan_manage -- get_real_path_of_apn_file -- erreur : projet inexistant")
    #
    #             msg(titre=application_title,
    #                 message=self.tr("Le projet n'existe pas dans le dossier temporaire d'Allplan."),
    #                 icone_avertissement=True)
    #
    #             return ""
    #
    #         if not is_cat_folder:
    #             return tmp_prj_path
    #
    #         chemin_dossier_prj_cat = f"{tmp_prj_path}Xml\\SmartCatalog\\"
    #
    #         if not os.path.exists(chemin_dossier_prj_cat):
    #             return ""
    #
    #     # -------------------
    #     # Apn file check
    #     # -------------------
    #
    #     elif file_path.endswith(".apn"):
    #
    #         # if not self.allplan_paths.
    #
    #
    #         path_file_prj = f"{prj_path}{file_name}.prj"
    #
    #         if not os.path.exists(file_path):
    #
    #             if show_msg:
    #                 a = QCoreApplication.translate("outils", "Le fichier '.prj' n'existe pas dans le dossier PRJ")
    #                 b = QCoreApplication.translate("outils", "Vous devez créer une liaison du projet dans Allplan")
    #                 c = QCoreApplication.translate("outils", "Fichier")
    #                 d = QCoreApplication.translate("outils", "Gestion de ressources avancés")
    #                 e = QCoreApplication.translate("outils", "Mes projets")
    #                 f = QCoreApplication.translate("outils", "clic droit")
    #                 g = QCoreApplication.translate("outils", "lier un projet existant")
    #
    #                 msg(titre=application_title,
    #                     message=f"{a}.\n{b} :\n{c} -> {d} -> \n{e} -> {f} -> {g}",
    #                     icone_avertissement=True)
    #
    #             print("outils -- recherche_chemin_projet_apn -- erreur : Fichier non lié")
    #
    #             return ""
    #
    #     else:
    #         print("outils -- recherche_chemin_projet_apn -- erreur : extension non reconnue")
    #         return ""
    #
    # def apn_file(self, file_path: str):
    #
    #     if not isinstance(self.allplan_paths, AllplanPaths):
    #         return ""
    #
    #     if not isinstance(file_path, str):
    #         return ""
    #
    #     if not os.path.exists(file_path):
    #         return ""
    #
    #     file_name = find_filename(file_path)
    #
    #     prj_file_path =f"{self.allplan_paths.prj_path}{file_name}.prj"
    #
    #     if os.path.exists(prj_file_path):
    #         return
    #
    #
    # def prj_file_get_path(self, prj_file_path: str):
    #
    #     if not isinstance(prj_file_path, str):
    #         return ""
    #
    #     if not os.path.exists(prj_file_path):
    #         return ""
    #
    #     try:
    #         with open(prj_file_path, "r") as file:
    #
    #             datas: list = file.readlines()
    #
    #     except Exception as erreur:
    #         print(f"outils -- recherche_chemin_projet_apn -- erreur : {erreur}")
    #         return ""
    #
    #     if len(datas) < 3:
    #         print("outils -- recherche_chemin_projet_apn -- erreur : Fichier non valide")
    #         return ""
    #
    #     file_name = find_filename(file_path)
    #
    #     tmp_path: str = datas[0]
    #     tmp_path = tmp_path.replace("\n", "")
    #
    #     if not tmp_path.endswith("\\"):
    #         tmp_path += "\\"
    #
    #     chemin_tmp_prj = f"{tmp_path}{file_name}.prj\\"
    #
    #     if not os.path.exists(chemin_tmp_prj):
    #         pass

    @staticmethod
    def a___________________end______():
        pass


# ====================================================== CREATION ===============

class Creation(QObject):

    def __init__(self, allplan):
        super().__init__()

        self.allplan: AllplanDatas = allplan

        self.unknown_txt = self.tr("Attribut inconnu")
        self.unknown_index = self.tr("Index non valide !")
        self.add_error = self.tr("Valeur ajoutée -> introuvable ds liste déroulante !")

        self.attributes_datas = dict()
        self.formula_datas = dict()

        # ---------------- Folder ----------------

    def folder_line(self, value: str, description="", icon_path="", tooltips=True) -> list:
        qs_main = Folder(value=value, icon_path=icon_path, tooltips=tooltips)
        qs_main.appendRow(self.attribute_line(value=description, number="207"))

        return [qs_main,
                Info(value=description, type_ele=folder_code),
                Info(value=attribute_default_base, type_ele=folder_code)]

    # ---------------- Material ----------------

    def material_line(self, value: str, description="", used_by_links=0, tooltips=True) -> list:
        qs_main = Material(value=value, used_by_links=used_by_links, tooltips=tooltips)
        qs_main.appendRow(self.attribute_line(value=description, number="207"))

        return [qs_main,
                Info(value=description, type_ele=material_code),
                Info(value=attribute_default_base, type_ele=material_code)]

    # ---------------- Component ----------------

    def component_line(self, value: str, description="", tooltips=True) -> list:
        qs_main = Component(value=value, tooltips=tooltips)
        qs_main.appendRow(self.attribute_line(value=description, number="207"))

        return [qs_main,
                Info(value=description, type_ele=component_code),
                Info(value=attribute_default_base, type_ele=component_code)]

    # ---------------- Link ----------------

    @staticmethod
    def link_line(value: str, description="", tooltips=True) -> list:
        return [Link(value=value, tooltips=tooltips),
                Info(value=description, type_ele=component_code),
                Info(value=attribute_default_base, type_ele=link_code)]

    # ---------------- Attribute ----------------

    def attribute_line(self, value: str, number: str, model_enumeration=None, use_default=False,
                       formula_convert=True) -> list:

        if "\n" in value:
            value = value.replace("\n", " ")

        attributes_datas_code = f"{number} - {value}"

        # if number == "232":
        #     print("a")

        if attributes_datas_code in self.attributes_datas:
            value, index_combo, name = self.attributes_datas[attributes_datas_code]

            return [Attribute(value=value),
                    Attribute(value=index_combo),
                    Attribute(value=number)]

        datas: dict = self.allplan.attributes_dict.get(number, dict())

        if len(datas) == 0:
            return [Attribute(value=value),
                    Attribute(value="-1"),
                    Attribute(value=number)]

        name = datas.get(code_attr_name, "")

        if number == "111" and (value == "0" or value == "-1" or value == ""):
            self.attributes_datas[attributes_datas_code] = ["", "-1", name]

            return [Attribute(value=""),
                    Attribute(value="0"),
                    Attribute(value=number)]

        option = datas.get(code_attr_option, "")

        if use_default and value == "":
            value = datas.get(code_attr_value)

        elif option == code_attr_dbl:
            value = format_float_value(value=value, allplan_version=self.allplan.version_allplan_current)

        elif number == "335":
            if value.startswith("\\\\"):
                value = value[2:]
            elif value.startswith("\\"):
                value = value[1:]

        elif option in [code_attr_formule_str, code_attr_formule_int, code_attr_formule_float]:

            user = datas.get(code_attr_user, False)

            if user:

                value = datas.get(code_attr_value, "")
                formula_check = ""

            else:

                if formula_convert:
                    value = self.allplan.formula_replace_all_name(formula=value)

                if value in self.formula_datas:
                    formula_check = self.formula_datas[value]
                else:

                    formula_check = self.allplan.verification_formule(value)
                    self.formula_datas[value] = formula_check

            qs_value = Attribute(value=value)

            if formula_check != "":
                qs_value.setData(formula_check, user_formule_ok)

            return [qs_value,
                    Attribute(value="-1"),
                    Attribute(value=number)]

        if "ComboBox" not in option:
            return [Attribute(value=value),
                    Attribute(value="-1"),
                    Attribute(value=number)]

        if model_enumeration is None:
            model_enumeration: QStandardItemModel = datas.get(code_attr_enumeration, QStandardItemModel())

        if option == code_attr_combo_int:
            colonne_donnees_save = col_enum_index

            try:
                value = str(int(value))
            except Exception:
                pass

        else:
            if model_enumeration.rowCount() == 0:
                self.attributes_datas[attributes_datas_code] = [value, "-1", name]

                return [Attribute(value=value),
                        Attribute(value="-1"),
                        Attribute(value=number)]

            colonne_donnees_save = col_enum_valeur

        if value.startswith("??_"):
            value = value.replace("??_", "")

        search = model_enumeration.findItems(value, Qt.MatchExactly, colonne_donnees_save)

        if len(search) > 0:
            index_combo = model_enumeration.item(search[0].row(), col_enum_index).text()
            value = model_enumeration.item(search[0].row(), col_enum_valeur).text()

            self.attributes_datas[attributes_datas_code] = [value, f"{index_combo}", name]

            return [Attribute(value=value),
                    Attribute(value=f"{index_combo}"),
                    Attribute(value=number)]

        # recherche dans l'autre colonne si la 1ère recherche est infructueuse
        if colonne_donnees_save == col_enum_index:
            col_recherche_secondaire = col_enum_valeur
        else:
            col_recherche_secondaire = col_enum_index

        search = model_enumeration.findItems(value, Qt.MatchExactly, col_recherche_secondaire)

        if len(search) > 0:
            index_combo = model_enumeration.item(search[0].row(), col_enum_index).text()
            value = model_enumeration.item(search[0].row(), col_enum_valeur).text()

            self.attributes_datas[attributes_datas_code] = [value, f"{index_combo}", name]

            return [Attribute(value=value),
                    Attribute(value=f"{index_combo}"),
                    Attribute(value=number)]

        if number == "141" and model_enumeration.columnCount() > 2:
            search = model_enumeration.findItems(value, Qt.MatchExactly, 2)

            if len(search) > 0:
                index_combo = model_enumeration.item(search[0].row(), col_enum_index).text()
                value = model_enumeration.item(search[0].row(), col_enum_valeur).text()

                self.attributes_datas[attributes_datas_code] = [value, f"{index_combo}", name]

                return [Attribute(value=value),
                        Attribute(value=f"{index_combo}"),
                        Attribute(value=number)]

            else:

                model_enumeration.appendRow(
                    [QStandardItem(value), QStandardItem(self.unknown_index), QStandardItem("???")])

                font = QStandardItem().font()
                font.setBold(True)
                font.setPointSize(10)

                standard_item_nom_layer = QStandardItem(get_icon(layer_icon), value)
                standard_item_nom_layer.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                standard_item_nom_layer.setFont(font)

                standard_item_numero_layer = QStandardItem(self.unknown_index)
                standard_item_numero_layer.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                standard_item_numero_layer.setFont(font)

                standard_item_code_layer = QStandardItem("???")
                standard_item_code_layer.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                standard_item_numero_layer.setFont(font)

                self.allplan.model_layers_view.appendRow([standard_item_nom_layer, standard_item_numero_layer,
                                                          standard_item_code_layer])

        # La valeur est dans aucune colonne !! création index

        if option == code_attr_combo_int:
            index_combo = value
            value = self.unknown_index

            self.attributes_datas[attributes_datas_code] = [value, f"{index_combo}", name]

            return [Attribute(value=value),
                    Attribute(value=f"{index_combo}"),
                    Attribute(value=number)]

        if number == "202":
            index_combo = model_enumeration.rowCount()
            model_enumeration.appendRow([QStandardItem(f"{index_combo}"), QStandardItem(value)])

            self.attributes_datas[attributes_datas_code] = [value, f"{index_combo}", name]

            return [Attribute(value=value),
                    Attribute(value=f"{index_combo}"),
                    Attribute(value=number)]

        qs_attribute = QStandardItem(value)
        qs_attribute.setData(QColor(255, 127, 39), Qt.BackgroundRole)

        qs_attribute.setData(self.add_error, Qt.ToolTipRole)

        index_combo = model_enumeration.rowCount()

        model_enumeration.appendRow([QStandardItem(index_combo), qs_attribute])

        self.attributes_datas[attributes_datas_code] = [value, f"{index_combo}", name]

        return [Attribute(value=value),
                Attribute(value=f"{index_combo}"),
                Attribute(value=number)]

    @staticmethod
    def a___________________end______():
        pass


class AllplanPaths:

    def __init__(self, allplan_version: str, allplan_version_name: str, installroot_path: str):
        super().__init__()

        self.installroot_path = installroot_path

        self.allplan_version = allplan_version
        self.allplan_version_name = allplan_version_name

        self.bad_config = False
        self.bad_config_note = ""

        self.allplan_version_int = -1

        try:
            self.allplan_version_int = int(self.allplan_version)
        except Exception as error:
            print(f"allplan_manage -- AllplanPaths -- init -- error : {error}")

        self.apn_compatible = self.allplan_version == "99" or self.allplan_version_int >= first_allplan_version_int

        # -------------
        # ETC Paths
        # -------------

        self.etc_path = ""
        self.etc_xml_path = ""
        self.etc_cat_path = ""

        self.etc_netmanager_path = ""

        self.workgroup = False

        # -------------
        # PRG Paths
        # -------------

        self.prg_path = ""
        self.prg_name = ""

        # -------------
        # Datas Paths
        # -------------

        self.datas_path = ""

        # -------------
        # STD Paths
        # -------------

        self.std_path = ""
        self.std_xml_path = ""
        self.std_cat_path = ""
        self.std_asw_path = ""
        self.std_obj000 = ""

        # -------------
        # PRJ Paths
        # -------------

        self.prj_path = ""

        # -------------
        # PRJ Paths
        # -------------

        self.net_path = ""

        # -------------
        # TMP Paths
        # -------------

        self.tmp_path = ""
        self.windows_user = os.path.expanduser(f'~\\')

        # -------------
        # USR Paths
        # -------------

        self.usr_path = ""

        # -------------
        # Load Paths
        # -------------

        self.load_paths()

    @staticmethod
    def a___________________load______():
        pass

    def load_paths(self):

        if not self.get_etc_paths():
            self.bad_config = True
            self.bad_config_note = "error ETC"
            return

        if not self.get_prg_path():
            self.bad_config = True
            self.bad_config_note = "error PRG"
            return

        if not self.get_datas_path():
            self.bad_config = True
            self.bad_config_note = "error Datas"
            return

        if not self.get_std_path():
            self.bad_config = True
            self.bad_config_note = "error STD"
            return

        if not self.get_prj_path():
            self.bad_config = True
            self.bad_config_note = "error PRJ"
            return

        if not self.get_user_path():
            self.bad_config = True
            self.bad_config_note = "error USR"
            return

        if not self.get_tmp_path():
            self.bad_config = True
            self.bad_config_note = "error TMP"
            return

        return

    @staticmethod
    def a___________________etc______():
        pass

    def get_etc_paths(self) -> bool:

        # -------------
        # Clear_datas
        # -------------

        self.etc_path = self.etc_xml_path = self.etc_netmanager_path = self.etc_cat_path = ""

        # -------------
        # Check CustomizedPaths
        # -------------

        installroot = f"{self.installroot_path}\\CustomizedPaths"

        reg_key = "Etc"

        etc_path = registry_find_value(installroot, reg_key)

        if etc_path != "" and os.path.exists(etc_path):

            if not etc_path.endswith("\\"):
                etc_path += "\\"

            self.etc_path = etc_path

            if self.get_etc_other_paths():
                return True

        # -------------
        # Check registry
        # -------------

        reg_etc_drive = "ProgramDataDrive"
        reg_etc_path = "ProgramDataPath"

        reg_drive_data = registry_find_value(self.installroot_path, reg_etc_drive)
        reg_path_data = registry_find_value(self.installroot_path, reg_etc_path)

        etc_path = f"{reg_drive_data}{reg_path_data}"

        if not etc_path.endswith("\\"):
            etc_path += "\\"

        etc_path += "Etc\\"

        # -------------
        # Check Etc path
        # -------------

        if not os.path.exists(etc_path):

            etc_path = f"C:\\ProgramData\\Nemetschek\\Allplan\\{self.allplan_version}\\Etc\\"

            if not os.path.exists(etc_path):
                print("allplan_manage -- AllplanVersion -- get_etc_path -- not os.path.exists(etc_path)")
                return False

        self.etc_path = etc_path

        return self.get_etc_other_paths()

    def get_etc_other_paths(self):

        # -------------
        # Check Netmanager path
        # -------------

        etc_netmanager_path = f"{self.etc_path}netmanager.xml"

        if not os.path.exists(etc_netmanager_path):
            print("allplan_manage -- AllplanVersion -- get_etc_other_paths -- not os.path.exists(etc_netmanager_path)")
            return False

        self.etc_netmanager_path = etc_netmanager_path

        # -------------
        # Check Etc Xml path
        # -------------

        etc_xml_path = f"{self.etc_path}Xml\\"

        if not os.path.exists(etc_xml_path):
            print("allplan_manage -- AllplanVersion -- get_etc_other_paths -- not os.path.exists(etc_xml_path)")
            return False

        self.etc_xml_path = etc_xml_path

        # -------------
        # Check Etc Catalog path
        # -------------

        for catalog_title in ["SmartCatalog", "Catalogs", "AVACatalog"]:

            etc_cat_path = f"{etc_xml_path}{catalog_title}\\"

            if os.path.exists(etc_cat_path):
                self.etc_cat_path = etc_cat_path
                break

        if self.etc_cat_path == "":
            print("allplan_manage -- AllplanVersion -- get_etc_other_paths -- self.etc_cat_path is empty")
            return False

        return True

    @staticmethod
    def a___________________prg______():
        pass

    def get_prg_path(self) -> bool:

        # -------------
        # Clear_datas
        # -------------

        self.prg_path = self.prg_name = ""

        # -------------
        # Program Name
        # -------------

        reg_prg_name_path = "ProgramName"

        reg_prg_name_data = registry_find_value(self.installroot_path, reg_prg_name_path)

        if reg_prg_name_data == "":
            return False

        self.prg_name = reg_prg_name_data

        # -------------
        # Check CustomizedPaths
        # -------------

        installroot = f"{self.installroot_path}\\CustomizedPaths"

        reg_key = "Prg"

        prg_path = registry_find_value(installroot, reg_key)

        if prg_path != "" and os.path.exists(prg_path):

            if not prg_path.endswith("\\"):
                prg_path += "\\"

            allplan_exe = f"{prg_path}{self.prg_name}"

            if os.path.exists(allplan_exe):
                self.prg_path = prg_path
                return True

        # -------------
        # Check registry
        # -------------

        reg_prg_drive = "ProgramDrive"
        reg_prg_path = "ProgramPath"

        reg_drive_data = registry_find_value(self.installroot_path, reg_prg_drive)
        reg_path_data = registry_find_value(self.installroot_path, reg_prg_path)

        prg_path = f"{reg_drive_data}{reg_path_data}"

        if not prg_path.endswith("\\"):
            prg_path += "\\"

        # -------------
        # Check PRG path
        # -------------

        allplan_exe = f"{prg_path}{self.prg_name}"

        if not os.path.exists(allplan_exe):
            print("allplan_manage -- AllplanVersion -- get_prg_path -- not os.path.exists(allplan_exe)")
            return False

        self.prg_path = prg_path

        return True

    @staticmethod
    def a___________________datas______():
        pass

    def get_datas_path(self) -> bool:

        # -------------
        # Clear_datas
        # -------------

        self.datas_path = self.net_path = ""

        self.workgroup = False

        # -------------
        # Check netmanager
        # -------------

        tree = validation_fichier_xml(self.etc_netmanager_path)

        if tree is None:
            print("allplan_manage -- AllplanVersion -- get_datas_path -- tree is None")
            return False

        search_path = tree.find('Path')

        if search_path is None:
            print("allplan_manage -- AllplanVersion -- get_datas_path -- search_path is None")
            return False

        datas_path = search_path.text

        if not isinstance(datas_path, str):
            print("allplan_manage -- AllplanVersion -- get_datas_path -- not isinstance(datas_path, str)")
            return False

        if not datas_path.endswith("\\"):
            datas_path += "\\"

        if not os.path.exists(datas_path):
            print("allplan_manage -- AllplanVersion -- get_datas_path -- not os.path.exists(datas_path)")
            return False

        self.datas_path = datas_path

        # -------------
        # Net path
        # -------------

        net_path = f"{datas_path}Net\\"

        if os.path.exists(net_path):
            self.net_path = net_path

        # -------------
        # Workgroup
        # -------------

        search_workgroup = tree.find('Active')

        if search_workgroup is None:
            print("allplan_manage -- AllplanVersion -- get_datas_path -- search_workgroup is None")
            return True

        self.workgroup = search_workgroup.text == "1"

        return True

    @staticmethod
    def a___________________std______():
        pass

    def get_std_path(self) -> bool:

        # -------------
        # Clear_datas
        # -------------

        self.std_path = ""
        self.std_xml_path = ""
        self.std_cat_path = ""
        self.std_asw_path = ""
        self.std_obj000 = ""

        # -------------
        # Check CustomizedPaths
        # -------------

        installroot = f"{self.installroot_path}\\CustomizedPaths"

        reg_key = "Std"

        std_path = registry_find_value(installroot, reg_key)

        if std_path != "" and os.path.exists(std_path):

            if not std_path.endswith("\\"):
                std_path += "\\"

            if os.path.exists(std_path):
                self.std_path = std_path

                self.get_std_other_paths()

                return True

        # -------------
        # Check STD path
        # -------------

        if self.datas_path == "":
            print("allplan_manage -- VersionDatas -- get_std_path -- self.datas_path is empty")
            return False

        std_path = f"{self.datas_path}STD\\"

        if not os.path.exists(std_path):
            print("allplan_manage -- VersionDatas -- get_std_path -- not os.path.exists(std_path)")
            return False

        self.std_path = std_path

        self.get_std_other_paths()

        return True

    def get_std_other_paths(self) -> bool:

        # -------------
        # Check Std Asw path
        # -------------

        std_asw_path = f"{self.std_path}Asw\\"

        if os.path.exists(std_asw_path):
            self.std_asw_path = std_asw_path

        else:
            print("allplan_manage -- AllplanVersion -- get_std_other_paths -- not os.path.exists(std_asw_path)")

        # -------------
        # Check objekt.000
        # -------------

        std_obj000 = f"{self.std_path}objekt.000"

        if os.path.exists(std_obj000):
            self.std_obj000 = std_obj000

        else:
            print("allplan_manage -- AllplanVersion -- get_std_other_paths -- not os.path.exists(std_obj000)")

        # -------------
        # Check Std Xml path
        # -------------

        std_xml_path = f"{self.std_path}Xml\\"

        if not os.path.exists(std_xml_path):
            print("allplan_manage -- AllplanVersion -- get_std_other_paths -- not os.path.exists(std_xml_path)")
            return False

        self.std_xml_path = std_xml_path

        # -------------
        # Check Std Catalog path
        # -------------

        for catalog_title in ["SmartCatalog", "Catalogs", "AVACatalog"]:

            std_cat_path = f"{std_xml_path}{catalog_title}\\"

            if os.path.exists(std_cat_path):
                self.std_cat_path = std_cat_path
                break

        if self.std_cat_path == "":

            if self.allplan_version == "2022":
                std_cat_path = f"{std_xml_path}AVACatalog\\"
            else:
                std_cat_path = f"{std_xml_path}SmartCatalog\\"

            try:
                os.mkdir(std_cat_path)

            except Exception:
                return False

            self.std_cat_path = std_cat_path
        return True

    @staticmethod
    def a___________________prj______():
        pass

    def get_prj_path(self) -> bool:

        # -------------
        # Clear_datas
        # -------------

        self.prj_path = ""

        # -------------
        # Check CustomizedPaths
        # -------------

        installroot = f"{self.installroot_path}\\CustomizedPaths"

        reg_key = "Prj"

        prj_path = registry_find_value(installroot, reg_key)

        if prj_path != "" and os.path.exists(prj_path):

            if not prj_path.endswith("\\"):
                prj_path += "\\"

            if os.path.exists(prj_path):
                self.prj_path = prj_path

                return True

        # -------------
        # Check Prj path
        # -------------

        if self.datas_path == "":
            print("allplan_manage -- VersionDatas -- get_prj_path -- self.datas_path is empty")
            return False

        prj_path = f"{self.datas_path}PRJ\\"

        if not os.path.exists(prj_path):
            print("allplan_manage -- VersionDatas -- get_prj_path -- not os.path.exists(prj_path)")
            return False

        self.prj_path = prj_path

        return True

    @staticmethod
    def a___________________usr______():
        pass

    def get_user_path(self) -> bool:

        # -------------
        # Clear_datas
        # -------------

        self.usr_path = ""

        # -------------
        # Check CustomizedPaths
        # -------------

        installroot = f"{self.installroot_path}\\CustomizedPaths"

        reg_key = "Usr"

        usr_path = registry_find_value(installroot, reg_key)

        if usr_path != "" and os.path.exists(usr_path):

            if usr_path.endswith("Local"):
                usr_path = usr_path.replace("Local", "")
            elif usr_path.endswith("Local\\"):
                usr_path = usr_path.replace("Local\\", "")

            if not usr_path.endswith("\\"):
                usr_path += "\\"

            self.usr_path = usr_path

            return True

        # -------------
        # Check Usr path
        # -------------

        usr_path = f"{allplan_docs}Nemetschek\\Allplan\\{self.allplan_version}\\Usr\\"

        if os.path.exists(usr_path):
            self.usr_path = usr_path
            return True

        usr_path = (f"{allplan_docs}Nemetschek\\Allplan_{self.allplan_version}_Verification\\"
                    f"{self.allplan_version}\\Usr\\")

        if os.path.exists(usr_path):
            self.usr_path = usr_path
            return True

        return True

    @staticmethod
    def a___________________tmp______():
        pass

    def get_tmp_path(self) -> bool:

        # -------------
        # Clear_datas
        # -------------

        self.tmp_path = ""

        # -------------
        # Check CustomizedPaths
        # -------------

        installroot = f"{self.installroot_path}\\CustomizedPaths"

        reg_key = "Tmp"

        tmp_path = registry_find_value(installroot, reg_key)

        if tmp_path != "" and os.path.exists(tmp_path):

            if not tmp_path.endswith("\\"):
                tmp_path += "\\"

            self.tmp_path = tmp_path

            return True

        # -------------
        # Check CustomizedPaths
        # -------------

        if os.path.exists(self.windows_user):

            tmp_path = f"{self.windows_user}AppData\\Local\\Nemetschek\\Allplan\\{self.allplan_version}\\Tmp\\"

            if os.path.exists(tmp_path):
                self.tmp_path = tmp_path
                return True

            tmp_path = (f"{self.windows_user}AppData\\Local\\Nemetschek\\Allplan_{self.allplan_version}_Verification\\"
                        f"{self.allplan_version}\\Tmp\\")

            if os.path.exists(tmp_path):
                self.tmp_path = tmp_path
                return True

        return True

    @staticmethod
    def a___________________end______():
        pass
