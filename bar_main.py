#!/usr/bin/python3
# -*- coding: utf-8 -*

import shutil

from catalog import WidgetCatalogNew
from catalog_manage import *
from tools import get_real_path_of_apn_file, settings_save, MyContextMenu, help_modify_tooltips
from tools import menu_ht_ligne, taille_police_menu, find_global_point
from tools import open_folder, verification_catalogue_correct, verification_nom_catalogue, menu_ht_widget
from browser import browser_file


class MainBar(QObject):

    def __init__(self, asc):
        super().__init__()

        self.asc = asc

        self.menu_cat_recent = MyContextMenu()

        self.ui: Ui_MainWindow = self.asc.ui
        self.catalog: CatalogDatas = self.asc.catalog
        self.allplan: AllplanDatas = self.asc.allplan

        self.dossier_defaut_ouvrir = ""

        # ---------------------------------------
        # CHARGEMENT Catalogue - Fichier
        # ---------------------------------------

        self.ui.new_bt.clicked.connect(self.catalogue_nouveau)
        help_modify_tooltips(widget=self.ui.new_bt, short_link=help_cat_new_cat, help_text=self.asc.help_tooltip)

        # -----

        self.ui.open_bt.clicked.connect(self.catalog_open_browse)
        help_modify_tooltips(widget=self.ui.open_bt, short_link=help_cat_open_cat, help_text=self.asc.help_tooltip)

        # -----

        self.ui.open_list_bt.clicked.connect(self.menu_cat_recent_show)
        self.ui.open_list_bt.customContextMenuRequested.connect(self.menu_cat_recent_show)

        # ---------------------------------------
        # CHARGEMENT Catalogue - Paramètre
        # ---------------------------------------

        self.ui.parameters_bt.clicked.connect(self.catalogue_modifier_parametres)
        help_modify_tooltips(widget=self.ui.parameters_bt,
                             short_link=help_cat_settings,
                             help_text=self.asc.help_tooltip)

        # ---------------------------------------
        # CHARGEMENT Catalogue - Enregistrer
        # ---------------------------------------

        self.ui.save_bt.clicked.connect(self.catalog.catalog_save)
        help_modify_tooltips(widget=self.ui.save_bt, short_link=help_cat_save, help_text=self.asc.help_tooltip)

        self.ui.update_cat_bt.clicked.connect(self.asc.catalogue_update)
        help_modify_tooltips(widget=self.ui.update_cat_bt, short_link=help_cat_update, help_text=self.asc.help_tooltip)

        self.ui.save_as_bt.clicked.connect(self.catalog_save_as)
        help_modify_tooltips(widget=self.ui.save_as_bt, short_link=help_cat_save_as, help_text=self.asc.help_tooltip)

        # ---------------------------------------
        # CHARGEMENT Nouveau catalogue
        # ---------------------------------------

        self.widget_nouveau = WidgetCatalogNew(self.asc)

    @staticmethod
    def a___________________nouveau______():
        pass

    def catalogue_nouveau(self):

        self.asc.formula_widget_close()

        if not self.catalog.catalog_save_ask():
            return

        self.widget_nouveau.personnalisation(new=True)

    def catalogue_importer(self):

        self.asc.formula_widget_close()

        if not self.catalog.catalog_save_ask():
            return

        self.widget_nouveau.personnalisation(convert_bdd=True)

    @staticmethod
    def a___________________ouvrir______():
        pass

    def catalog_open_browse(self):

        self.asc.formula_widget_close()

        if not self.catalog.catalog_save_ask():
            return

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            path_default = self.allplan.allplan_paths.std_cat_path

            shortcuts_list = [self.allplan.allplan_paths.etc_cat_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.tmp_path]
        else:
            path_default = ""

            shortcuts_list = list()

        chemin_fichier = browser_file(parent=self.asc,
                                      title=application_title,
                                      registry=[app_setting_file, "path_catalog_open"],
                                      shortcuts_list=shortcuts_list,
                                      datas_filters={self.tr("Fichier Catalogue"): [".xml", ".apn", ".prj"]},
                                      current_path=self.catalog.catalog_path,
                                      default_path=path_default,
                                      use_setting_first=True)

        if chemin_fichier == "":
            return

        if chemin_fichier.endswith(".apn") or chemin_fichier.endswith(".prj"):

            # version_current = self.allplan.allplan_paths

            # todo à modifier

            if "2024" in self.allplan.version_datas:

                version_obj = self.allplan.version_datas["2024"]

                if not isinstance(version_obj, AllplanPaths):
                    return

                chemin_prj = version_obj.prj_path

            elif "2025" not in self.allplan.version_datas:

                version_obj = self.allplan.version_datas["2025"]

                if not isinstance(version_obj, AllplanPaths):
                    return

                chemin_prj = version_obj.prj_path

            else:
                return

            chemin_catalogue_tmp = get_real_path_of_apn_file(chemin_fichier, chemin_prj, True)

            if chemin_catalogue_tmp == "":
                return

            chemin_fichier = chemin_catalogue_tmp

        if verification_catalogue_correct(chemin_fichier, True) == "":
            return

        print(f"onglet_catalogue -- catalogue_ouvrir -- lancer chargement catalogue : {chemin_fichier}")

        self.catalog.catalog_load_start(catalog_path=chemin_fichier)

    def menu_cat_recent_show(self):

        self.menu_cat_recent.clear()
        dict_cat = dict()

        dict_cat[self.tr("Catalogue de démo")] = list()

        for version_allplan in self.allplan.versions_list:
            dict_cat[f"ETC -- Allplan {version_allplan}"] = list()
            dict_cat[f"PRJ -- Allplan {version_allplan}"] = list()

        chemin_cat_2023 = f"{asc_user_path}Catalogue - exemples\\2023\\CMI.xml"

        cat_2023_existe = os.path.exists(chemin_cat_2023)

        if cat_2023_existe:
            liste: list = dict_cat[self.tr("Catalogue de démo")]
            liste.append(chemin_cat_2023)

        dict_cat["ETC"] = list()
        dict_cat["PRJ"] = list()
        dict_cat[self.tr("Autres")] = list()

        liste_fichiers_ouverts = settings_list(cat_list_file)
        liste_fichiers_ouverts.sort()

        liste_fichiers_ouverts_fin = list(liste_fichiers_ouverts)

        for chemin_fichier in reversed(liste_fichiers_ouverts):

            dossier_catalogue = os.path.dirname(chemin_fichier)

            if not os.path.exists(chemin_fichier) or len(chemin_fichier) < 2:
                liste_fichiers_ouverts_fin.remove(chemin_fichier)
                continue

            if "\\etc\\" in chemin_fichier.lower():

                recherche = False
                for version_allplan in self.allplan.versions_list:

                    if version_allplan in dossier_catalogue:
                        liste: list = dict_cat[f"ETC -- Allplan {version_allplan}"]
                        liste.append(chemin_fichier)
                        recherche = True
                        break

                if not recherche:
                    liste: list = dict_cat["ETC"]
                    liste.append(chemin_fichier)

            elif "\\prj\\" in chemin_fichier.lower():

                recherche = False
                for version_allplan in self.allplan.versions_list:

                    if version_allplan in dossier_catalogue:
                        liste: list = dict_cat[f"PRJ -- Allplan {version_allplan}"]
                        liste.append(chemin_fichier)
                        recherche = True
                        break

                if not recherche:
                    liste: list = dict_cat["PRJ"]
                    liste.append(chemin_fichier)

            else:

                liste: list = dict_cat[self.tr("Autres")]
                liste.append(chemin_fichier)

        settings_save(cat_list_file, liste_fichiers_ouverts_fin)

        menu_ok = False

        for key_dict, liste_datas in dict_cat.items():

            key_dict: str
            liste_datas: list

            if len(liste_datas) == 0:
                continue

            liste_datas.sort()

            menu_ok = True

            self.menu_cat_recent.add_title(title=f"{key_dict}")

            for index_menu, chemin_catalogue in enumerate(liste_datas):

                if chemin_catalogue == chemin_cat_2023 and cat_2023_existe and key_dict != self.tr("Catalogue de démo"):
                    continue

                self.menu_cat_recent.addAction(self.menu_deroulant_chemin(chemin_catalogue, index_menu,
                                                                          key_dict == self.tr("Catalogue de démo")))

        if not menu_ok:
            return

        self.menu_cat_recent.exec_(find_global_point(self.ui.open_list_bt))

    @staticmethod
    def menu_titre_projet(chemin) -> str:

        chemin_cat_2023 = f"{asc_user_path}Catalogue - exemples\\2023\\CMI.xml"

        if chemin == chemin_cat_2023:
            return "CMI - 2023"

        nom_catalogue = os.path.basename(chemin)

        if ".prj" not in chemin:
            return nom_catalogue

        try:
            start = chemin.rfind("\\", 0, chemin.find(".prj"))
            end = chemin.find(".prj")

            if start == -1:
                return nom_catalogue
            elif end == 3:
                return nom_catalogue
            else:
                nom_fichier = chemin[start + 1:end]
                return f"{nom_fichier} --> {nom_catalogue}"

        except ValueError:
            return nom_catalogue

    def menu_bt_supprimer(self, chemin: str):

        settings_list(cat_list_file, ele_del=chemin)

        self.menu_cat_recent.close()
        self.menu_cat_recent_show()

    def catalog_open_file(self, chemin_fichier: str):
        print(f"onglet_hierarchie -- menu_bt_charger -- lancer chargement catalogue : {chemin_fichier}")

        self.asc.formula_widget_close()

        self.menu_cat_recent.close()

        if not self.catalog.catalog_save_ask():
            return

        self.catalog.catalog_load_start(catalog_path=chemin_fichier)

    @staticmethod
    def menu_bt_ouvrir_dossier(chemin: str):
        if os.path.exists(chemin):
            open_folder(find_folder_path(chemin))

    @staticmethod
    def a___________________parametres______():
        pass

    def catalogue_modifier_parametres(self):

        self.asc.formula_widget_close()

        if not self.catalog.catalog_save_ask():
            return

        self.widget_nouveau.personnalisation(modify=True)

    @staticmethod
    def a___________________enregistrer______():
        pass

    def catalog_save_as(self):

        self.asc.formula_widget_close()

        if self.catalog.catalog_path == "":
            return

        if isinstance(self.allplan.allplan_paths, AllplanPaths):

            path_default = self.allplan.allplan_paths.std_cat_path

            shortcuts_list = [self.allplan.allplan_paths.etc_cat_path,
                              self.allplan.allplan_paths.std_cat_path,
                              self.allplan.allplan_paths.prj_path,
                              self.allplan.allplan_paths.tmp_path]
        else:
            path_default = ""

            shortcuts_list = list()

        catalog_path_new = browser_file(parent=self.asc,
                                        title=application_title,
                                        registry=[app_setting_file, "path_catalog_save"],
                                        shortcuts_list=shortcuts_list,
                                        datas_filters={self.tr("Fichier Catalogue"): [".xml"]},
                                        current_path=self.catalog.catalog_path,
                                        default_path=path_default,
                                        file_name=self.catalog.catalog_name,
                                        use_setting_first=True,
                                        use_save=True)

        if catalog_path_new == self.catalog.catalog_path or catalog_path_new == "":
            return

        catalog_path_new = verification_nom_catalogue(catalog_path_new)

        # ---------------------
        # Dossier settings
        # ---------------------

        settings_folder_new = get_catalog_setting_folder(catalog_folder=find_folder_path(catalog_path_new))

        catalog_name = find_filename(catalog_path_new)

        # ---------------------
        # Dossier path INI
        # ---------------------

        if os.path.exists(self.catalog.catalog_setting_path_file):

            setting_path_file_new = get_catalog_setting_path_file(catalog_settings_folder=settings_folder_new,
                                                                  catalog_name=catalog_name)

            try:
                shutil.copy(self.catalog.catalog_setting_path_file, setting_path_file_new)

            except Exception as erreur:

                msg(titre=application_title,
                    message=self.tr("Une erreur est survenue."),
                    icone_avertissement=True,
                    details=f"{erreur}")

                return

        else:
            return

        # ---------------------
        # Dossier Affichage
        # ---------------------

        if os.path.exists(self.catalog.catalog_setting_display_file):

            setting_display_file_new = get_catalog_setting_display_file(catalog_settings_folder=settings_folder_new,
                                                                        catalog_name=catalog_name)

            try:
                shutil.copy(self.catalog.catalog_setting_display_file, setting_display_file_new)
            except Exception as erreur:

                msg(titre=application_title,
                    message=self.tr("Une erreur est survenue."),
                    icone_avertissement=True,
                    details=f"{erreur}")

                return

        else:
            return

        # ---------------------
        # Catalogue
        # ---------------------

        CatalogSave(asc=self.asc, catalog=self.catalog, allplan=self.allplan,
                    catalog_path=catalog_path_new,
                    catalog_setting_display_file=setting_display_file_new)

        if msg(titre=application_title,
               message=self.tr("Voulez-vous ouvrir ce nouveau catalogue?"),
               type_bouton=QMessageBox.Ok | QMessageBox.No,
               defaut_bouton=QMessageBox.No,
               icone_ouvrir=True) == QMessageBox.Ok:
            print(f"onglet_catalogue -- catalogue_enregistrer_sous -- lancer chargement catalogue : {catalog_path_new}")

            if not self.catalog.catalog_save_ask():
                return

            self.catalog.catalog_load_start(catalog_path=catalog_path_new)

        else:

            settings_save_value(file_name=app_setting_file, key_name="path_catalog", value=catalog_path_new)

            catalog_opened_list = settings_list(file_name=cat_list_file, ele_add=catalog_path_new)

            self.asc.open_list_manage(catalog_opened_list=catalog_opened_list)

    @staticmethod
    def a___________________outils______():
        pass

    def menu_deroulant_chemin(self, chemin: str, index_menu: int, demo=False) -> QWidgetAction:

        action_widget = QWidgetAction(self.asc)
        action_widget.setEnabled(True)
        action_widget.setIconVisibleInMenu(False)

        widget = QWidget()

        font = widget.font()
        font.setPointSize(taille_police_menu)
        widget.setFont(font)

        widget.setMinimumWidth(150)
        widget.setFixedHeight(menu_ht_ligne)

        projet_actif = chemin == self.catalog.catalog_path

        if projet_actif:
            widget.setStyleSheet("QWidget{background-color: #8FADCC}")

        else:

            if index_menu % 2:
                widget.setStyleSheet("QWidget{background-color: #E7E7E7}"
                                     "QPushButton:hover{background-color: #BAD0E7; "
                                     "border-style: inset; border-width: 0px;}"
                                     "QPushButton:pressed{background-color: #8FADCC; "
                                     "border-style: inset; border-width: 0px;}")
            else:
                widget.setStyleSheet("QWidget{background-color: #FFFFFF}"
                                     "QPushButton:hover{background-color: #BAD0E7; "
                                     "border-style: inset; border-width: 0px;}"
                                     "QPushButton:pressed{background-color: #8FADCC; "
                                     "border-style: inset; border-width: 0px;}")

        horizontallayout = QHBoxLayout(widget)
        horizontallayout.setContentsMargins(6, 0, 6, 0)

        # ---------

        pushbutton_ouvrir = QPushButton(get_icon(catalog_icon), "")
        pushbutton_ouvrir.setFlat(True)
        pushbutton_ouvrir.setIconSize(QSize(18, 18))
        pushbutton_ouvrir.setFixedSize(QSize(24, 24))

        horizontallayout.addWidget(pushbutton_ouvrir)

        pushbutton_ouvrir.clicked.connect(lambda: self.menu_bt_ouvrir_dossier(chemin))
        pushbutton_ouvrir.setToolTip(self.tr("Afficher ce catalogue dans votre explorateur de fichier"))

        # ---------

        titre = self.menu_titre_projet(chemin)

        pushbutton_titre = QPushButton(titre)
        pushbutton_titre.setFlat(True)
        pushbutton_titre.setFixedHeight(menu_ht_widget)
        pushbutton_titre.setMinimumWidth(150)
        pushbutton_titre.setStyleSheet("padding-left:4px; text-align:left")
        pushbutton_titre.setFont(font)

        horizontallayout.addWidget(pushbutton_titre)

        pushbutton_titre.clicked.connect(lambda: self.catalog_open_file(chemin))

        titre_trad = self.tr('Charger catalogue')

        pushbutton_titre.setToolTip(f"{titre_trad} : {chemin}")

        # ---------

        pushbutton_corbeille = QPushButton(get_icon(delete_icon), "")
        pushbutton_corbeille.setFlat(True)
        pushbutton_corbeille.setIconSize(QSize(18, 18))
        pushbutton_corbeille.setFixedSize(QSize(24, 24))

        pushbutton_corbeille.clicked.connect(lambda: self.menu_bt_supprimer(chemin))

        if projet_actif or demo:
            pushbutton_corbeille.setEnabled(False)
            pushbutton_corbeille.setToolTip(self.tr("Suppression impossible : Catalogue actif"))

        elif demo:
            pushbutton_corbeille.setEnabled(False)
            pushbutton_corbeille.setToolTip(self.tr("Suppression impossible : Catalogue de démo"))

        else:
            pushbutton_corbeille.setToolTip(self.tr("Supprimer ce catalogue de la liste"))

        # ---------
        horizontallayout.addWidget(pushbutton_corbeille)

        widget.sizeHint()

        action_widget.setDefaultWidget(widget)

        return action_widget
