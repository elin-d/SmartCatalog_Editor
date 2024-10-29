#!/usr/bin/python3
# -*- coding: utf-8 -*
from typing import Union
from allplan_manage import AllplanDatas
from formatting_widget import Formatting
from tools import ValidatorDouble, move_widget_ss_bouton, get_look_tableview, get_look_combobox
from tools import format_float_value, taille_police
from tools import afficher_message as msg
from ui_attribute_231 import Ui_Attribute231
from ui_attribute_232 import Ui_Attribute232
from ui_attribute_233 import Ui_Attribute233
from ui_attribute_235 import Ui_Attribute235
from ui_room import Ui_Room
from ui_room_favorite_modify import Ui_RoomFavoriteModify
from main_datas import *

col_favoris = 0
col_231 = 1
col_235 = 2
col_232 = 3
col_266 = 4
col_233 = 5
col_264 = 6
col_nb = 7


class WidgetAttribute231(QWidget):
    modif_termine = pyqtSignal(str)

    def __init__(self, widget_piece, langue: str):
        super().__init__(parent=widget_piece)

        self.setWindowFlags(Qt.Popup)

        # Création de l'interface
        self.ui = Ui_Attribute231()
        self.ui.setupUi(self)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(f":/Images/room_231_{langue.lower()}.png")))
        self.setPalette(palette)

        self.lancer_enregistrement = True
        self.valeur_actuelle = ""

        self.ui.bt_r_rdc.installEventFilter(self)
        self.ui.bt_r_etage_11.installEventFilter(self)
        self.ui.bt_r_etage_12.installEventFilter(self)
        self.ui.bt_r_etage_2.installEventFilter(self)
        self.ui.bt_r_garage.installEventFilter(self)
        self.ui.bt_r_etage_22.installEventFilter(self)
        self.ui.bt_s_loggia.installEventFilter(self)
        self.ui.bt_s_ext.installEventFilter(self)
        self.ui.bt_s_balcon.installEventFilter(self)

        self.ui.bt_valider.clicked.connect(self.close)
        self.ui.bt_quitter.clicked.connect(self.fermer)

        # ---------------------

        if langue in translation_231:
            self.translation_list = translation_231.get(langue)
        else:
            self.translation_list = translation_231.get("EN")

        r_text = self.translation_list[0]
        s_text = self.translation_list[1]

        self.ui.bt_r_rdc.setText(r_text)
        self.ui.bt_r_etage_11.setText(r_text)
        self.ui.bt_r_etage_12.setText(r_text)
        self.ui.bt_r_etage_2.setText(r_text)
        self.ui.bt_r_etage_22.setText(r_text)
        self.ui.bt_r_garage.setText(r_text)

        self.ui.bt_s_balcon.setText(s_text)
        self.ui.bt_s_loggia.setText(s_text)
        self.ui.bt_s_ext.setText(s_text)

    def personnaliser(self):

        if self.valeur_actuelle == self.translation_list[0]:
            self.ui.bt_r_rdc.setChecked(True)

        elif self.valeur_actuelle == self.translation_list[1]:
            self.ui.bt_s_loggia.setChecked(True)

    def fermer(self):

        self.lancer_enregistrement = False
        self.close()

    def enregistrer(self):

        if self.ui.bt_s_loggia.isChecked() or self.ui.bt_s_ext.isChecked() or self.ui.bt_s_balcon.isChecked():
            self.modif_termine.emit(self.translation_list[1])
            return

        self.modif_termine.emit(self.translation_list[0])

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if self.lancer_enregistrement:
            self.enregistrer()

        self.lancer_enregistrement = True

        super().closeEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if (obj == self.ui.bt_r_rdc or obj == self.ui.bt_r_etage_11 or obj == self.ui.bt_r_etage_12 or
            obj == self.ui.bt_r_etage_2 or obj == self.ui.bt_r_garage or obj == self.ui.bt_r_etage_22 or
            obj == self.ui.bt_s_loggia or obj == self.ui.bt_s_ext or obj == self.ui.bt_s_balcon) and \
                event.type() == QEvent.MouseButtonDblClick:
            self.close()

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass


class WidgetAttribute232(QWidget):
    modif_termine = pyqtSignal(str)

    def __init__(self, parent_current, allplan: AllplanDatas):
        super().__init__(parent=parent_current)

        self.setWindowFlags(Qt.Popup)

        # Création de l'interface
        self.ui = Ui_Attribute232()
        self.ui.setupUi(self)

        self.langue = allplan.langue

        self.lancer_enregistrement = True
        self.valeur_actuelle = ""

        self.ui.list.doubleClicked.connect(self.close)

        get_look_tableview(self.ui.list)

        self.ui.bt_valider.clicked.connect(self.close)
        self.ui.bt_quitter.clicked.connect(self.fermer)

        # ---------------------

        if self.langue in translation_232_combo:
            self.translation_list = translation_232_combo.get(self.langue)
        else:
            self.translation_list = translation_232_combo.get("EN")

        self.ui.list.clear()
        self.ui.list.addItems(self.translation_list)

    def personnaliser(self):

        if self.valeur_actuelle in self.translation_list:
            row_index = self.translation_list.index(self.valeur_actuelle)
        else:
            row_index = 0

        self.ui.list.setCurrentRow(row_index)

    def fermer(self):

        self.lancer_enregistrement = False
        self.close()

    def enregistrer(self):

        current_row = self.ui.list.currentRow()

        translation_list = translation_232.get(self.langue, list())

        row_count = len(translation_list)

        if row_count != translation_232_count:
            return

        if current_row < 0 or current_row >= row_count:
            self.modif_termine.emit(translation_list[0])
            return

        self.modif_termine.emit(translation_list[current_row])

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if self.lancer_enregistrement:
            self.enregistrer()

        self.lancer_enregistrement = True

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class WidgetAttribute233(QWidget):
    modif_termine = pyqtSignal(str)

    def __init__(self, widget_piece, langue):
        super().__init__(parent=widget_piece)

        self.setWindowFlags(Qt.Popup)

        self.ui = Ui_Attribute233()
        self.ui.setupUi(self)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(f":/Images/room_233_{langue.lower()}.png")))
        self.setPalette(palette)

        # ---------------------------

        self.lancer_enregistrement = True
        self.valeur_actuelle = ""

        self.ui.bt_sh.installEventFilter(self)
        self.ui.bt_sa.installEventFilter(self)
        self.ui.bt_se.installEventFilter(self)
        self.ui.bt_nh.installEventFilter(self)

        self.ui.bt_valider.clicked.connect(self.close)
        self.ui.bt_quitter.clicked.connect(self.fermer)

        # ---------------------------

        if langue in translation_233:
            self.translation_list = translation_233.get(langue)
        else:
            self.translation_list = translation_233.get("EN")

        self.ui.bt_sh.setText(self.translation_list[0])
        self.ui.bt_sa.setText(self.translation_list[1])
        self.ui.bt_se.setText(self.translation_list[2])
        self.ui.bt_nh.setText(self.translation_list[3])

    def personnaliser(self):

        if self.valeur_actuelle == self.translation_list[0]:
            self.ui.bt_sh.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[1]:
            self.ui.bt_sa.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[2]:
            self.ui.bt_se.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[3]:
            self.ui.bt_nh.setChecked(True)

    def fermer(self):

        self.lancer_enregistrement = False
        self.close()

    def enregistrer(self):

        if self.ui.bt_sa.isChecked():
            self.modif_termine.emit(self.ui.bt_sa.text())
            return

        if self.ui.bt_se.isChecked():
            self.modif_termine.emit(self.ui.bt_se.text())
            return

        if self.ui.bt_nh.isChecked():
            self.modif_termine.emit(self.ui.bt_nh.text())
            return

        self.modif_termine.emit(self.ui.bt_sh.text())

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if self.lancer_enregistrement:
            self.enregistrer()

        self.lancer_enregistrement = True

        super().closeEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if (obj == self.ui.bt_sh or obj == self.ui.bt_sa or obj == self.ui.bt_se or obj == self.ui.bt_nh) and \
                event.type() == QEvent.MouseButtonDblClick:
            self.close()

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass


class WidgetAttribute235(QWidget):
    modif_termine = pyqtSignal(str)

    def __init__(self, widget_piece, langue: str):
        super().__init__(parent=widget_piece)

        self.setWindowFlags(Qt.Popup)

        self.ui = Ui_Attribute235()
        self.ui.setupUi(self)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(f":/Images/room_235_{langue.lower()}.png")))
        self.setPalette(palette)

        # ---------------------------

        self.lancer_enregistrement = True
        self.valeur_actuelle = ""

        self.ui.bt_su.installEventFilter(self)
        self.ui.bt_sit.installEventFilter(self)
        self.ui.bt_su1.installEventFilter(self)
        self.ui.bt_su2.installEventFilter(self)
        self.ui.bt_su3.installEventFilter(self)
        self.ui.bt_su4.installEventFilter(self)
        self.ui.bt_su5.installEventFilter(self)
        self.ui.bt_su6.installEventFilter(self)
        self.ui.bt_su7.installEventFilter(self)
        self.ui.bt_st.installEventFilter(self)
        self.ui.bt_sd.installEventFilter(self)

        self.ui.bt_valider.clicked.connect(self.close)
        self.ui.bt_quitter.clicked.connect(self.fermer)

        # ---------------------------

        if langue in translation_235:
            self.translation_list = translation_235.get(langue)
        else:
            self.translation_list = translation_235.get("EN")

        self.ui.bt_su.setText(self.translation_list[0])

        self.ui.bt_sit.setText(self.translation_list[1])
        self.ui.bt_st.setText(self.translation_list[1])

        self.ui.bt_sd.setText(self.translation_list[2])
        self.ui.bt_sd2.setText(self.translation_list[2])

        self.ui.bt_su1.setText(self.translation_list[3])
        self.ui.bt_su2.setText(self.translation_list[4])
        self.ui.bt_su3.setText(self.translation_list[5])
        self.ui.bt_su4.setText(self.translation_list[6])
        self.ui.bt_su5.setText(self.translation_list[7])
        self.ui.bt_su6.setText(self.translation_list[8])
        self.ui.bt_su7.setText(self.translation_list[9])

    def personnaliser(self):

        if self.valeur_actuelle == self.translation_list[0]:
            self.ui.bt_su.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[1]:
            self.ui.bt_sit.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[2]:
            self.ui.bt_sd.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[3]:
            self.ui.bt_su1.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[4]:
            self.ui.bt_su2.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[5]:
            self.ui.bt_su3.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[6]:
            self.ui.bt_su4.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[7]:
            self.ui.bt_su5.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[8]:
            self.ui.bt_su6.setChecked(True)
            return

        if self.valeur_actuelle == self.translation_list[9]:
            self.ui.bt_su7.setChecked(True)
            return

    def fermer(self):

        self.lancer_enregistrement = False
        self.close()

    def enregistrer(self):

        if self.ui.bt_su.isChecked():
            self.modif_termine.emit(self.ui.bt_su.text())
            return

        if self.ui.bt_su1.isChecked():
            self.modif_termine.emit(self.ui.bt_su1.text())
            return

        if self.ui.bt_su2.isChecked():
            self.modif_termine.emit(self.ui.bt_su2.text())
            return

        if self.ui.bt_su3.isChecked():
            self.modif_termine.emit(self.ui.bt_su3.text())
            return

        if self.ui.bt_su4.isChecked():
            self.modif_termine.emit(self.ui.bt_su4.text())
            return

        if self.ui.bt_su5.isChecked():
            self.modif_termine.emit(self.ui.bt_su5.text())
            return

        if self.ui.bt_su6.isChecked():
            self.modif_termine.emit(self.ui.bt_su6.text())
            return

        if self.ui.bt_su7.isChecked():
            self.modif_termine.emit(self.ui.bt_su7.text())
            return

        if self.ui.bt_st.isChecked():
            self.modif_termine.emit(self.ui.bt_st.text())
            return

        if self.ui.bt_sit.isChecked():
            self.modif_termine.emit(self.ui.bt_sit.text())
            return

        if self.ui.bt_sd.isChecked():
            self.modif_termine.emit(self.ui.bt_sd.text())

        if self.ui.bt_sd2.isChecked():
            self.modif_termine.emit(self.ui.bt_sd2.text())
            return

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if self.lancer_enregistrement:
            self.enregistrer()

        self.lancer_enregistrement = True

        super().closeEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if (obj == self.ui.bt_su or obj == self.ui.bt_sit or obj == self.ui.bt_su1 or obj == self.ui.bt_su2 or
            obj == self.ui.bt_su3 or obj == self.ui.bt_su4 or obj == self.ui.bt_su5 or obj == self.ui.bt_su6 or
            obj == self.ui.bt_su7 or obj == self.ui.bt_st or obj == self.ui.bt_sd) and \
                event.type() == QEvent.MouseButtonDblClick:
            self.close()

        return super().eventFilter(obj, event)

    @staticmethod
    def a___________________end______():
        pass


class WidgetRoom(QWidget):
    modif_termine = pyqtSignal(str, str, str, str, str, str, str)
    save_favoris = pyqtSignal()

    def __init__(self, allplan, liste_titres: list):
        super().__init__()

        self.ui = Ui_Room()
        self.ui.setupUi(self)

        self.allplan: AllplanDatas = allplan

        self.demande_enregistrer = False
        self.modification_favoris = False

        self.liste_titres = liste_titres

        # ---------------------------------------
        # Room name button
        # ---------------------------------------

        if (self.allplan.langue in translation_room and self.allplan.langue in translation_231 and
                self.allplan.langue in translation_235):

            self.room_names_list = translation_room.get(self.allplan.langue)
            self.room_231_list = translation_231.get(self.allplan.langue)
            self.room_235_list = translation_235.get(self.allplan.langue)

        else:
            self.room_names_list = translation_room.get("EN")
            self.room_231_list = translation_231.get("EN")
            self.room_235_list = translation_235.get("EN")

        # -----------

        room_name, bt_title = self.get_title(room_index=aeration_index)

        self.ui.bt_aeration.setText(bt_title)
        self.ui.bt_aeration.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=air_frais_index)

        self.ui.bt_air_frais.setText(bt_title)
        self.ui.bt_air_frais.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=bain_index)

        self.ui.bt_bain.setText(bt_title)
        self.ui.bt_bain.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=balcon_index)

        self.ui.bt_balcon_1.setText(bt_title)
        self.ui.bt_balcon_1.clicked.connect(self.charger_favoris(room_name))

        self.ui.bt_balcon_2.setText(bt_title)
        self.ui.bt_balcon_2.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=bureau_index)

        self.ui.bt_bureau.setText(bt_title)
        self.ui.bt_bureau.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=chauffage_index)

        self.ui.bt_chauffage.setText(bt_title)
        self.ui.bt_chauffage.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=comble_index)

        self.ui.bt_comble.setText(bt_title)
        self.ui.bt_comble.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=couloir_index)

        self.ui.bt_couloir.setText(bt_title)
        self.ui.bt_couloir.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=cour_index)

        self.ui.bt_cour.setText(bt_title)
        self.ui.bt_cour.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=debarras_index)

        self.ui.bt_debarras.setText(bt_title)
        self.ui.bt_debarras.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=escalier_index)

        self.ui.bt_escalier.setText(bt_title)
        self.ui.bt_escalier.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=hall_index)

        self.ui.bt_hall.setText(bt_title)
        self.ui.bt_hall.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=loggias_index)

        self.ui.bt_loggias.setText(bt_title)
        self.ui.bt_loggias.clicked.connect(self.charger_favoris(room_name))

        # -----------

        room_name, bt_title = self.get_title(room_index=sejour_index)

        self.ui.bt_sejour.setText(bt_title)
        self.ui.bt_sejour.clicked.connect(self.charger_favoris(room_name))

        attribut_text = self.tr("Attribut")

        self.ui.titre_231.setToolTip(f"{attribut_text} 231")
        self.ui.titre_232.setToolTip(f"{attribut_text} 232")
        self.ui.titre_233.setToolTip(f"{attribut_text} 233")
        self.ui.titre_235.setToolTip(f"{attribut_text} 235")
        self.ui.titre_264.setToolTip(f"{attribut_text} 264")
        self.ui.titre_266.setToolTip(f"{attribut_text} 266")

        # ---------------------------------------
        # Favoris
        # ---------------------------------------

        self.model_room_favoris = QStandardItemModel()

        self.filtre_room_favoris = QSortFilterProxyModel()
        self.filtre_room_favoris.setSourceModel(self.model_room_favoris)
        self.filtre_room_favoris.setFilterCaseSensitivity(Qt.CaseInsensitive)

        qcompleter_room_favoris = QCompleter()
        qcompleter_room_favoris.setModel(self.filtre_room_favoris)
        qcompleter_room_favoris.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_room_favoris.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_fav.setCompleter(qcompleter_room_favoris)

        self.ui.valeur_fav.currentIndexChanged.connect(self.favoris_change)

        get_look_combobox(self.ui.valeur_fav)

        self.ui.valeur_fav.installEventFilter(self)

        # ---------------------------------------
        # 231 - Pourtour de salle
        # ---------------------------------------

        self.ui_231 = WidgetAttribute231(self, self.allplan.langue)
        self.ui_231.modif_termine.connect(self.ui.valeur_231.setCurrentText)
        self.ui_231.modif_termine.connect(self.ui.valeur_231.setFocus)

        self.filtre_231 = QSortFilterProxyModel()
        self.filtre_231.setSourceModel(self.allplan.model_231)
        self.filtre_231.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_231.setFilterKeyColumn(1)

        self.ui.valeur_231.setModel(self.allplan.model_231)
        self.ui.valeur_231.setModelColumn(1)

        qcompleter_231 = QCompleter()
        qcompleter_231.setModel(self.filtre_231)
        qcompleter_231.setCompletionColumn(1)
        qcompleter_231.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_231.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_231.setCompleter(qcompleter_231)

        self.ui.valeur_231.currentIndexChanged.connect(self.change_231)
        self.ui.valeur_231.lineEdit().textEdited.connect(self.filtre_231.setFilterFixedString)

        self.ui.bt_231.clicked.connect(self.afficher_ui_231)

        self.ui.valeur_231.installEventFilter(self)

        self.valeur_231_defaut = ""

        get_look_combobox(self.ui.valeur_231)

        # ---------------------------------------
        # 235 - Type utlisation
        # ---------------------------------------

        self.ui_235 = WidgetAttribute235(self, self.allplan.langue)
        self.ui_235.modif_termine.connect(self.ui.valeur_235.setCurrentText)
        self.ui_235.modif_termine.connect(self.ui.valeur_235.setFocus)

        self.filtre_235 = QSortFilterProxyModel()
        self.filtre_235.setSourceModel(self.allplan.model_235)
        self.filtre_235.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_235.setFilterKeyColumn(1)

        self.ui.valeur_235.setModel(self.allplan.model_235)
        self.ui.valeur_235.setModelColumn(1)

        qcompleter_235 = QCompleter()
        qcompleter_235.setModel(self.filtre_235)
        qcompleter_235.setCompletionColumn(1)
        qcompleter_235.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_235.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_235.setCompleter(qcompleter_235)

        self.ui.valeur_235.currentIndexChanged.connect(self.change_235)
        self.ui.valeur_235.lineEdit().textEdited.connect(self.filtre_235.setFilterFixedString)

        self.ui.bt_235.clicked.connect(self.afficher_ui_235)

        self.ui.valeur_235.installEventFilter(self)

        self.valeur_235_defaut = ""

        get_look_combobox(self.ui.valeur_235)

        # ---------------------------------------
        # 232 - Type de surface
        # ---------------------------------------

        self.ui_232 = WidgetAttribute232(self, self.allplan)
        self.ui_232.modif_termine.connect(self.ui.valeur_232.setCurrentText)
        self.ui_232.modif_termine.connect(self.ui.valeur_232.setFocus)

        self.filtre_232 = QSortFilterProxyModel()
        self.filtre_232.setSourceModel(self.allplan.model_232)
        self.filtre_232.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_232.setFilterKeyColumn(1)

        self.ui.valeur_232.setModel(self.allplan.model_232)
        self.ui.valeur_232.setModelColumn(1)

        qcompleter_232 = QCompleter()
        qcompleter_232.setModel(self.filtre_232)
        qcompleter_232.setCompletionColumn(1)
        qcompleter_232.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_232.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_232.setCompleter(qcompleter_232)

        self.ui.valeur_232.currentIndexChanged.connect(self.change_232)
        self.ui.valeur_232.lineEdit().textEdited.connect(self.filtre_232.setFilterFixedString)

        self.ui.bt_232.clicked.connect(self.afficher_ui_232)

        self.ui.valeur_232.installEventFilter(self)

        self.valeur_232_defaut = ""

        get_look_combobox(self.ui.valeur_232)

        # ---------------------------------------
        # 266 - Facteur Din
        # ---------------------------------------

        self.ui.valeur_266.setValidator(ValidatorDouble())
        self.ui.valeur_266.editingFinished.connect(self.change_266)

        # ---------------------------------------
        # 233 - Type surface hab
        # ---------------------------------------

        self.ui_233 = WidgetAttribute233(self, self.allplan.langue)
        self.ui_233.modif_termine.connect(self.ui.valeur_233.setCurrentText)
        self.ui_233.modif_termine.connect(self.ui.valeur_233.setFocus)

        self.filtre_233 = QSortFilterProxyModel()
        self.filtre_233.setSourceModel(self.allplan.model_233)
        self.filtre_233.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtre_233.setFilterKeyColumn(1)

        self.ui.valeur_233.setModel(self.allplan.model_233)
        self.ui.valeur_233.setModelColumn(1)

        qcompleter_233 = QCompleter()
        qcompleter_233.setModel(self.filtre_233)
        qcompleter_233.setCompletionColumn(1)
        qcompleter_233.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        qcompleter_233.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.valeur_233.setCompleter(qcompleter_233)

        self.ui.valeur_233.currentIndexChanged.connect(self.change_233)
        self.ui.valeur_233.lineEdit().textEdited.connect(self.filtre_233.setFilterFixedString)

        self.ui.bt_233.clicked.connect(self.afficher_ui_233)

        self.ui.valeur_233.installEventFilter(self)

        self.valeur_233_defaut = ""

        get_look_combobox(self.ui.valeur_233)
        # ---------------------------------------
        # 264 - Facteur de surface habitable
        # ---------------------------------------

        self.ui.valeur_264.setValidator(ValidatorDouble())
        self.ui.valeur_264.editingFinished.connect(self.change_264)

        # ---------------------------------------
        # sélection rapide
        # ---------------------------------------
        self.widget_room_favoris = WidgetRoomFavoriteModify()
        self.widget_room_favoris.creation_termine.connect(self.ajouter_favoris_action)
        self.widget_room_favoris.modif_termine.connect(self.renommer_favoris_action)

        self.ui.bt_ajouter.clicked.connect(self.ajouter_favoris)
        self.ui.bt_renommer.clicked.connect(self.renommer_favoris)
        self.ui.bt_supprimer.clicked.connect(self.supprimer_favoris)

        # ---------------------------------------
        # enregistrer
        # ---------------------------------------

        self.ui.bt_enregistrer.clicked.connect(self.enregistrer)
        self.ui.bt_quitter.clicked.connect(self.close)

        self.modification_en_cours = False

    @staticmethod
    def a___________________chargement______():
        pass

    def get_title(self, room_index: int) -> tuple:

        try:

            room_name = self.room_names_list[room_index]

            config_list = room_config_list[room_index]

            index_231 = config_list[0]
            index_235 = config_list[3]

            room_231 = self.room_231_list[index_231]
            room_235 = self.room_235_list[index_235]

            return room_name, f"{room_name}\n{room_235} {room_231}"

        except Exception as error:
            print(f"room -- get_title -- error : {error}")
            return "", ""

    def chargement(self, nom_favoris: str, valeur_231: str, valeur_235: str, valeur_232: str, valeur_266: str,
                   valeur_233: str, valeur_264: str):

        print(f"widget_piece -- chargement -- {nom_favoris}")

        self.filtre_room_favoris.setSourceModel(self.model_room_favoris)
        self.ui.valeur_fav.setModel(self.model_room_favoris)

        nom_favoris = self.rechercher_favoris(nom_favoris, valeur_231, valeur_235, valeur_232, valeur_266, valeur_233,
                                              valeur_264)

        self.valeur_231_defaut = valeur_231
        self.valeur_235_defaut = valeur_235
        self.valeur_232_defaut = valeur_232
        self.valeur_233_defaut = valeur_233

        self.set_current_texte(self.ui.valeur_fav, nom_favoris, True)
        self.set_current_texte(self.ui.valeur_231, valeur_231, True)
        self.set_current_texte(self.ui.valeur_235, valeur_235, True)
        self.set_current_texte(self.ui.valeur_232, valeur_232, True)
        self.ui.valeur_266.setText(valeur_266)
        self.set_current_texte(self.ui.valeur_233, valeur_233, True)
        self.ui.valeur_264.setText(valeur_264)

        self.gestion_bouton_favoris()

        self.demande_enregistrer = False
        self.modification_en_cours = False
        self.modification_favoris = False

    @staticmethod
    def set_current_texte(object_combo: QComboBox, valeur_recherche: str, blocksignal=False):

        index_item = object_combo.findText(valeur_recherche, Qt.MatchExactly)

        object_combo.blockSignals(blocksignal)

        object_combo.setCurrentIndex(index_item)

        object_combo.blockSignals(False)

    @staticmethod
    def a___________________favoris______():
        pass

    def chargement_favoris(self, valeur_231: str, valeur_235: str, valeur_232: str, valeur_266: str,
                           valeur_233: str, valeur_264: str):

        print("widget_type_piece -- favoris chargement")

        self.set_current_texte(self.ui.valeur_231, valeur_231, True)
        self.set_current_texte(self.ui.valeur_232, valeur_232, True)
        self.set_current_texte(self.ui.valeur_233, valeur_233, True)
        self.set_current_texte(self.ui.valeur_235, valeur_235, True)
        self.ui.valeur_264.setText(valeur_264)
        self.ui.valeur_266.setText(valeur_266)

    def recherche_favoris_auto(self):

        print("widget_piece -- recherche_favoris_auto")

        valeur_fav = self.ui.valeur_fav.currentText()

        valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264 = self.recherche_valeurs()

        nom_favoris = self.rechercher_favoris(valeur_fav, valeur_231, valeur_235, valeur_232, valeur_266, valeur_233,
                                              valeur_264)

        if nom_favoris == valeur_fav:
            return

        self.set_current_texte(self.ui.valeur_fav, nom_favoris)
        self.modification_en_cours = True
        return

    def rechercher_favoris(self, nom_favoris: str, valeur_231: str, valeur_235: str, valeur_232: str, valeur_266: str,
                           valeur_233: str, valeur_264: str):

        valeur_264_clean = valeur_264.replace(",", "").replace(".", "")
        valeur_266_clean = valeur_266.replace(",", "").replace(".", "")

        if nom_favoris != "":
            index_qstandarditem = self.ui.valeur_fav.findText(nom_favoris)

            # --------------

            qs_231 = self.model_room_favoris.item(index_qstandarditem, col_231)

            if not isinstance(qs_231, QStandardItem):
                return

            data_231 = qs_231.text()

            # --------------

            qs_232 = self.model_room_favoris.item(index_qstandarditem, col_232)

            if not isinstance(qs_232, QStandardItem):
                return

            data_232 = qs_232.text()

            # --------------

            qs_233 = self.model_room_favoris.item(index_qstandarditem, col_233)

            if not isinstance(qs_233, QStandardItem):
                return

            data_233 = qs_233.text()

            # --------------

            qs_235 = self.model_room_favoris.item(index_qstandarditem, col_235)

            if not isinstance(qs_235, QStandardItem):
                return

            data_235 = qs_235.text()

            # --------------

            qs_264 = self.model_room_favoris.item(index_qstandarditem, col_264)

            if not isinstance(qs_264, QStandardItem):
                return

            data_264 = qs_264.text()
            data_264_clean = data_264.replace(",", "").replace(".", "")

            # --------------

            qs_266 = self.model_room_favoris.item(index_qstandarditem, col_266)

            if not isinstance(qs_266, QStandardItem):
                return

            data_266 = qs_266.text()
            data_266_clean = data_266.replace(",", "").replace(".", "")

            if (data_231 == valeur_231 and data_235 == valeur_235 and data_232 == valeur_232 and
                    data_266_clean == valeur_266_clean and data_233 == valeur_233 and
                    data_264_clean == valeur_264_clean):
                return nom_favoris

        print("widget_piece -- recherche_favoris")

        for index_qstandarditem in range(1, self.model_room_favoris.rowCount()):

            # --------------

            qs_fav = self.model_room_favoris.item(index_qstandarditem, col_favoris)

            if not isinstance(qs_fav, QStandardItem):
                return

            nom_favoris = qs_fav.text()

            # --------------

            qs_231 = self.model_room_favoris.item(index_qstandarditem, col_231)

            if not isinstance(qs_231, QStandardItem):
                return

            data_231 = qs_231.text()

            if data_231 != valeur_231:
                continue

            # --------------

            qs_232 = self.model_room_favoris.item(index_qstandarditem, col_232)

            if not isinstance(qs_232, QStandardItem):
                return

            data_232 = qs_232.text()

            if data_232 != valeur_232:
                continue

            # --------------

            qs_233 = self.model_room_favoris.item(index_qstandarditem, col_233)

            if not isinstance(qs_233, QStandardItem):
                return

            data_233 = qs_233.text()

            if data_233 != valeur_233:
                continue

            # --------------

            qs_235 = self.model_room_favoris.item(index_qstandarditem, col_235)

            if not isinstance(qs_235, QStandardItem):
                return

            data_235 = qs_235.text()

            if data_235 != valeur_235:
                continue

            # --------------

            qs_264 = self.model_room_favoris.item(index_qstandarditem, col_264)

            if not isinstance(qs_264, QStandardItem):
                return

            data_264 = qs_264.text()
            data_264_clean = data_264.replace(",", "").replace(".", "")

            if data_264_clean != valeur_264_clean:
                continue

            # --------------

            qs_266 = self.model_room_favoris.item(index_qstandarditem, col_266)

            if not isinstance(qs_266, QStandardItem):
                return

            data_266 = qs_266.text()
            data_266_clean = data_266.replace(",", "").replace(".", "")

            if data_266_clean != valeur_266_clean:
                continue

            # --------------

            return nom_favoris

        index_qstandarditem = 0

        tooltips = self.creation_tooltips("", valeur_231, valeur_235, valeur_232, valeur_266, valeur_233,
                                          valeur_264)

        # --------------

        qs_fav = self.model_room_favoris.item(index_qstandarditem, col_favoris)

        if not isinstance(qs_fav, QStandardItem):
            return

        qs_fav.setToolTip(tooltips)

        # --------------

        qs_231 = self.model_room_favoris.item(index_qstandarditem, col_231)

        if not isinstance(qs_231, QStandardItem):
            return

        qs_231.setText(valeur_231)

        # --------------

        qs_231 = self.model_room_favoris.item(index_qstandarditem, col_231)

        if not isinstance(qs_231, QStandardItem):
            return

        qs_231.setText(valeur_231)

        # --------------

        qs_232 = self.model_room_favoris.item(index_qstandarditem, col_232)

        if not isinstance(qs_232, QStandardItem):
            return

        qs_232.setText(valeur_232)

        # --------------

        qs_233 = self.model_room_favoris.item(index_qstandarditem, col_233)

        if not isinstance(qs_233, QStandardItem):
            return

        qs_233.setText(valeur_233)

        # --------------

        qs_235 = self.model_room_favoris.item(index_qstandarditem, col_235)

        if not isinstance(qs_235, QStandardItem):
            return

        qs_235.setText(valeur_235)

        # --------------

        qs_264 = self.model_room_favoris.item(index_qstandarditem, col_264)

        if not isinstance(qs_264, QStandardItem):
            return

        qs_264.setText(valeur_264)

        # --------------

        qs_266 = self.model_room_favoris.item(index_qstandarditem, col_266)

        if not isinstance(qs_266, QStandardItem):
            return

        qs_266.setText(valeur_266)

        # --------------

        return ""

    def recherche_valeurs(self) -> tuple:

        valeur_231 = self.ui.valeur_231.currentText()
        valeur_235 = self.ui.valeur_235.currentText()
        valeur_232 = self.ui.valeur_232.currentText()
        valeur_266 = self.ui.valeur_266.text()
        valeur_233 = self.ui.valeur_233.currentText()
        valeur_264 = self.ui.valeur_264.text()

        return valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264

    @staticmethod
    def a___________________favoris_changement______():
        pass

    @staticmethod
    def creation_tooltips(nom_favoris: str, valeur_231: str, valeur_235: str, valeur_232: str, valeur_266: str,
                          valeur_233: str, valeur_264: str):

        return (f"Nom favoris : <b>{nom_favoris}</b><br><br>"
                f"231 : <b>{valeur_231}</b><br>"
                f"235 : <b>{valeur_235}</b><br>"
                f"232 : <b>{valeur_232}</b><br>"
                f"266 : <b>{valeur_266}</b><br>"
                f"233 : <b>{valeur_233}</b><br>"
                f"264 : <b>{valeur_264}</b>")

    def favoris_change(self):

        if self.ui.valeur_fav.view().isVisible():
            return

        current_row: int = self.ui.valeur_fav.currentIndex()
        current_text: str = self.ui.valeur_fav.currentText()

        if current_row == -1:
            return

        print(f"widget_piece -- favoris_change -- {current_text} --> {current_row}")

        # --------------

        qs_231 = self.model_room_favoris.item(current_row, col_231)

        if not isinstance(qs_231, QStandardItem):
            return

        valeur_231 = qs_231.text()

        # --------------

        qs_232 = self.model_room_favoris.item(current_row, col_232)

        if not isinstance(qs_232, QStandardItem):
            return

        valeur_232 = qs_232.text()

        # --------------

        qs_233 = self.model_room_favoris.item(current_row, col_233)

        if not isinstance(qs_233, QStandardItem):
            return

        valeur_233 = qs_233.text()

        # --------------

        qs_235 = self.model_room_favoris.item(current_row, col_235)

        if not isinstance(qs_235, QStandardItem):
            return

        valeur_235 = qs_235.text()

        # --------------

        qs_264 = self.model_room_favoris.item(current_row, col_264)

        if not isinstance(qs_264, QStandardItem):
            return

        valeur_264 = qs_264.text()

        # --------------

        qs_266 = self.model_room_favoris.item(current_row, col_266)

        if not isinstance(qs_266, QStandardItem):
            return

        valeur_266 = qs_266.text()

        # --------------

        self.chargement_favoris(valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264)
        self.gestion_bouton_favoris()

    def charger_favoris(self, nom_favoris: str):

        def charger_favoris_action():
            print(f"widget_piece -- charger_favoris -- {nom_favoris}")

            self.set_current_texte(object_combo=self.ui.valeur_fav, valeur_recherche=nom_favoris)

            self.modification_en_cours = True

        return charger_favoris_action

    def gestion_bouton_favoris(self):

        if self.allplan.langue in translation_room:
            favoris_defaut = translation_room.get(self.allplan.langue)
        else:
            favoris_defaut = translation_room.get("EN")

        if len(favoris_defaut) != translation_room_count:
            self.ui.bt_supprimer.setEnabled(False)
            self.ui.bt_renommer.setEnabled(False)
            return

        current_texte = self.ui.valeur_fav.currentText()

        if current_texte == "" or current_texte in favoris_defaut:
            self.ui.bt_supprimer.setEnabled(False)
            self.ui.bt_renommer.setEnabled(False)
            return

        self.ui.bt_supprimer.setEnabled(True)
        self.ui.bt_renommer.setEnabled(True)

    @staticmethod
    def a___________________favoris_ajouter______():
        pass

    def ajouter_favoris(self):

        self.charger_widget_room_favoris(self.ui.valeur_fav.currentText())

    def charger_widget_room_favoris(self, valeur_actuelle: str, mode="creation"):

        self.widget_room_favoris.liste_favoris_upper.clear()
        self.widget_room_favoris.liste_favoris.clear()

        self.widget_room_favoris.valeur_actuelle = valeur_actuelle

        for index_item in range(self.model_room_favoris.rowCount()):

            qs_fav = self.model_room_favoris.item(index_item, col_favoris)

            if not isinstance(qs_fav, QStandardItem):
                continue

            texte = qs_fav.text()
            self.widget_room_favoris.liste_favoris.append(texte)
            self.widget_room_favoris.liste_favoris_upper.append(texte.upper())

        move_widget_ss_bouton(button=self.ui.bt_ajouter, widget=self.widget_room_favoris)

        self.widget_room_favoris.personnaliser(mode)

    def ajouter_favoris_action(self, nom_favoris: str, current_index: int):

        print(f"widget_piece -- ajouter_favoris_action -- {nom_favoris}")

        valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264 = self.recherche_valeurs()

        tooltips = self.creation_tooltips(nom_favoris, valeur_231, valeur_235, valeur_232, valeur_266, valeur_233,
                                          valeur_264)

        font = QStandardItem().font()
        font.setFamily("Segoe UI")
        font.setPointSize(taille_police)

        if current_index == -1:

            qstandarditem_favoris = QStandardItem(nom_favoris)
            qstandarditem_favoris.setFont(font)
            qstandarditem_favoris.setToolTip(tooltips)

            liste = [qstandarditem_favoris,
                     QStandardItem(valeur_231),
                     QStandardItem(valeur_235),
                     QStandardItem(valeur_232),
                     QStandardItem(valeur_266),
                     QStandardItem(valeur_233),
                     QStandardItem(valeur_264)]

            self.model_room_favoris.appendRow(liste)

            self.model_room_favoris.sort(col_favoris, Qt.AscendingOrder)

        else:

            # --------------

            qs_fav = self.model_room_favoris.item(current_index, col_favoris)

            if not isinstance(qs_fav, QStandardItem):
                return

            qs_fav.setText(nom_favoris)
            qs_fav.setToolTip(tooltips)

            # --------------

            qs_231 = self.model_room_favoris.item(current_index, col_231)

            if not isinstance(qs_231, QStandardItem):
                return

            qs_231.setText(self.ui.valeur_231.currentText())

            # --------------

            qs_232 = self.model_room_favoris.item(current_index, col_232)

            if not isinstance(qs_232, QStandardItem):
                return

            qs_232.setText(self.ui.valeur_232.currentText())

            # --------------

            qs_233 = self.model_room_favoris.item(current_index, col_233)

            if not isinstance(qs_233, QStandardItem):
                return

            qs_233.setText(self.ui.valeur_233.currentText())

            # --------------

            qs_235 = self.model_room_favoris.item(current_index, col_235)

            if not isinstance(qs_235, QStandardItem):
                return

            qs_235.setText(self.ui.valeur_235.currentText())

            # --------------

            qs_264 = self.model_room_favoris.item(current_index, col_264)

            if not isinstance(qs_264, QStandardItem):
                return

            qs_264.setText(self.ui.valeur_264.text())

            # --------------

            qs_266 = self.model_room_favoris.item(current_index, col_266)

            if not isinstance(qs_266, QStandardItem):
                return

            qs_266.setText(self.ui.valeur_266.text())

        self.set_current_texte(self.ui.valeur_fav, nom_favoris)
        self.ui.valeur_fav.setFocus()

        self.modification_favoris = True
        self.modification_en_cours = True

    @staticmethod
    def a___________________favoris_supprimer______():
        pass

    def supprimer_favoris(self):

        current_index = self.ui.valeur_fav.currentIndex()

        print(f"widget_piece -- supprimer_favoris -- current_texte")

        if current_index == -1:
            return

        if msg(titre=self.windowTitle(),
               message=self.tr("Voulez-vous supprimer ce favoris?"),
               type_bouton=QMessageBox.Ok | QMessageBox.Cancel,
               defaut_bouton=QMessageBox.Ok,
               icone_question=True) == QMessageBox.Cancel:
            return

        self.model_room_favoris.takeRow(current_index)

        self.modification_favoris = True
        self.modification_en_cours = True

    @staticmethod
    def a___________________favoris_enregistrer______():
        pass

    def renommer_favoris(self):

        if self.allplan.langue in translation_room:
            favoris_defaut = translation_room.get(self.allplan.langue)
        else:
            favoris_defaut = translation_room.get("EN")

        if len(favoris_defaut) == 0:
            self.ui.bt_supprimer.setEnabled(False)
            self.ui.bt_renommer.setEnabled(False)
            return

        current_index = self.ui.valeur_fav.currentIndex()

        if current_index == -1:
            return

        current_texte = self.ui.valeur_fav.currentText()

        if current_texte in favoris_defaut:
            return

        self.charger_widget_room_favoris(current_texte, "renommer")

    def renommer_favoris_action(self, ancien_nom: str, nom_favoris: str):

        print(f"widget_piece -- enregistrer_favoris_action -- {nom_favoris}")

        current_index = self.ui.valeur_fav.findText(ancien_nom)

        if current_index == -1:
            return

        valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264 = self.recherche_valeurs()

        tooltips = self.creation_tooltips(nom_favoris, valeur_231, valeur_235, valeur_232, valeur_266, valeur_233,
                                          valeur_264)

        # --------------

        qs_fav = self.model_room_favoris.item(current_index, col_favoris)

        if not isinstance(qs_fav, QStandardItem):
            return

        qs_fav.setText(nom_favoris)
        qs_fav.setToolTip(tooltips)

        # --------------

        self.model_room_favoris.sort(col_favoris, Qt.AscendingOrder)

        self.ui.valeur_fav.setFocus()

        self.modification_en_cours = True
        self.modification_favoris = True

    @staticmethod
    def a___________________231_pourtour_de_salle______():
        pass

    def change_231(self):
        if not self.isVisible():
            return

        self.valeur_231_defaut = self.verification_datas(self.ui.valeur_231, self.valeur_231_defaut, "231")

    def afficher_ui_231(self):
        self.charger_gestion_surfaces(widget_popup=self.ui_231,
                                      bouton=self.ui.bt_231,
                                      valeur=self.ui.valeur_231.currentText())

    @staticmethod
    def a___________________235_type_utilisation______():
        pass

    def change_235(self):
        if not self.isVisible():
            return

        self.valeur_235_defaut = self.verification_datas(self.ui.valeur_235, self.valeur_235_defaut, "235")

    def afficher_ui_235(self):
        self.charger_gestion_surfaces(widget_popup=self.ui_235,
                                      bouton=self.ui.bt_235,
                                      valeur=self.ui.valeur_235.currentText())

    @staticmethod
    def a___________________232_type_surface______():
        pass

    def change_232(self):
        if not self.isVisible():
            return

        self.valeur_232_defaut = self.verification_datas(self.ui.valeur_232, self.valeur_232_defaut, "232")

    def afficher_ui_232(self):
        self.charger_gestion_surfaces(widget_popup=self.ui_232,
                                      bouton=self.ui.bt_232,
                                      valeur=self.ui.valeur_232.currentText())

    @staticmethod
    def a___________________266_facteur_din______():
        pass

    def change_266(self):

        if not self.isVisible():
            return

        value = format_float_value(value=self.ui.valeur_266.text(),
                                   allplan_version=self.allplan.version_allplan_current)

        if self.ui.valeur_266.text() == value:
            return

        self.ui.valeur_266.setText(value)

        self.recherche_favoris_auto()

        self.modification_en_cours = True

    @staticmethod
    def a___________________233_type_surface_hab______():
        pass

    def change_233(self):

        if not self.isVisible():
            return

        self.valeur_233_defaut = self.verification_datas(self.ui.valeur_233, self.valeur_233_defaut, "233")

    def afficher_ui_233(self):
        self.charger_gestion_surfaces(widget_popup=self.ui_233,
                                      bouton=self.ui.bt_233,
                                      valeur=self.ui.valeur_233.currentText())

    @staticmethod
    def a___________________264_facteur_hab______():
        pass

    def change_264(self):

        if not self.isVisible():
            return

        value = format_float_value(value=self.ui.valeur_264.text(),
                                   allplan_version=self.allplan.version_allplan_current)

        if self.ui.valeur_264.text() == value:
            return

        self.modification_en_cours = True

        self.ui.valeur_264.setText(value)
        self.recherche_favoris_auto()

    @staticmethod
    def a___________________datas______():
        pass

    def verification_datas(self, obj_valeur: QComboBox, valeur_defaut: str, attribut: str):

        if obj_valeur.view().isVisible():
            return

        if not self.isVisible():
            return

        print(f"widget_piece -- verification_datas -- {attribut}")

        texte = obj_valeur.currentText()
        index_row = obj_valeur.currentIndex()

        if index_row == -1 or texte == "":
            self.set_current_texte(obj_valeur, valeur_defaut)
            self.recherche_favoris_auto()
            return valeur_defaut

        recherche = obj_valeur.findText(texte, Qt.MatchExactly)

        if recherche == -1:
            self.set_current_texte(obj_valeur, valeur_defaut)
            self.recherche_favoris_auto()
            return valeur_defaut

        self.recherche_favoris_auto()
        return texte

    @staticmethod
    def a___________________ui_annexe______():
        pass

    @staticmethod
    def charger_gestion_surfaces(
            widget_popup: Union[WidgetAttribute231, WidgetAttribute232, WidgetAttribute233, WidgetAttribute235],
            bouton: QPushButton, valeur: str):

        widget_popup.valeur_actuelle = valeur

        move_widget_ss_bouton(bouton, widget_popup)

        widget_popup.personnaliser()

        widget_popup.show()

    @staticmethod
    def a___________________enregistrement______():
        pass

    def enregistrer(self):

        if self.modification_favoris:
            self.save_favoris.emit()
            self.modification_favoris = False

        valeur_fav = self.ui.valeur_fav.currentText()
        valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264 = self.recherche_valeurs()

        self.modif_termine.emit(valeur_fav, valeur_231, valeur_235, valeur_232, valeur_266, valeur_233, valeur_264)
        self.modification_en_cours = False

        self.close()

    def enregistrer_question(self):

        if not self.demande_enregistrer and not self.modification_en_cours:
            return

        if msg(titre=self.windowTitle(),
               message=self.tr("Voulez-vous enregistrer les modifications?"),
               type_bouton=QMessageBox.Ok | QMessageBox.No,
               defaut_bouton=QMessageBox.Ok,
               icone_sauvegarde=True) == QMessageBox.Ok:
            self.enregistrer()

    def quitter(self):
        self.demande_enregistrer = False

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        self.enregistrer_question()

        self.demande_enregistrer = True

        super().closeEvent(event)

    def eventFilter(self, obj: QWidget, event: QEvent):

        if not self.isVisible():
            return super().eventFilter(obj, event)

        if not isinstance(obj, QComboBox):
            return super().eventFilter(obj, event)

        if obj.view().isVisible():
            return super().eventFilter(obj, event)

        if obj == self.ui.valeur_fav:

            if event.type() == QEvent.FocusOut:
                self.favoris_change()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_fav.hasFocus():
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

        if obj == self.ui.valeur_231:

            if event.type() == QEvent.FocusOut:
                if self.ui.valeur_231.view().isVisible():
                    return super().eventFilter(obj, event)

                self.change_231()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_231.hasFocus():
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

        if obj == self.ui.valeur_235:

            if event.type() == QEvent.FocusOut:
                self.change_235()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_235.hasFocus():
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

        if obj == self.ui.valeur_232:

            if event.type() == QEvent.FocusOut:
                self.change_232()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_232.hasFocus():
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

        if obj == self.ui.valeur_233:

            if event.type() == QEvent.FocusOut:
                self.change_233()
                return super().eventFilter(obj, event)

            if event.type() == QEvent.Wheel:
                if not self.ui.valeur_233.hasFocus():
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


class WidgetRoomFavoriteModify(QWidget):
    creation_termine = pyqtSignal(str, int)
    modif_termine = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.Popup)

        self.ui = Ui_RoomFavoriteModify()
        self.ui.setupUi(self)

        self.widget_options = Formatting()
        self.widget_options.save_modif_formatage.connect(self.options_retour_datas)

        self.ui.format_bt.clicked.connect(self.options_afficher)

        self.valeur_actuelle = ""

        self.liste_favoris = list()
        self.liste_favoris_upper = list()
        self.mode = "creation"

        completer = QCompleter(self.liste_favoris)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.favorite_name.setCompleter(completer)

        self.ui.favorite_name.textChanged.connect(self.changement)

        self.ui.ok.clicked.connect(self.enregistrer)
        self.ui.quit.clicked.connect(self.close)

    def personnaliser(self, mode="creation"):

        self.mode = mode

        if mode == "creation":
            completer = QCompleter(self.liste_favoris)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.ui.favorite_name.setCompleter(completer)
        else:
            self.ui.favorite_name.setCompleter(None)

        self.ui.favorite_name.setText(self.valeur_actuelle)

        self.changement()
        self.ui.favorite_name.setFocus()
        self.show()

    def changement(self):

        valeur = self.ui.favorite_name.text().strip()

        if valeur == "":
            self.ui.verification.setIcon(get_icon(error_icon))
            self.ui.verification.setToolTip(self.tr("Impossible de laisser ce titre sans texte."))

            self.ui.ok.setEnabled(False)

            self.ui.favorite_name.setStyleSheet("QLineEdit{padding-left: 5px; "
                                                "border: 2px solid orange;"
                                                "border-top-left-radius:5px; "
                                                "border-bottom-left-radius: 5px; }")

            return

        if "|" in valeur:
            self.ui.verification.setIcon(get_icon(error_icon))
            self.ui.verification.setToolTip(self.tr("Le caractère ' | ' est interdit, désolé !"))
            self.ui.ok.setEnabled(False)

            self.ui.favorite_name.setStyleSheet("QLineEdit{padding-left: 5px; "
                                                "border: 2px solid orange;"
                                                "border-top-left-radius:5px; "
                                                "border-bottom-left-radius: 5px; }")
            return

        if valeur.upper() in self.liste_favoris_upper:

            if self.mode == "creation":
                self.ui.verification.setIcon(get_icon(error_icon))
                self.ui.verification.setToolTip(
                    self.tr("Ce titre existe déjà, ses paramètres seront mis à jour!"))

                self.ui.favorite_name.setStyleSheet("QLineEdit{padding-left: 5px; "
                                                    "border: 1px solid #8f8f91;"
                                                    "border-right-width: 0px; "
                                                    "border-top-left-radius:5px; "
                                                    "border-bottom-left-radius: 5px; }")

                self.ui.ok.setEnabled(True)
                self.ui.ok.setText(self.tr("Mettre à jour"))
                return

            self.ui.verification.setToolTip(self.tr("Ce titre est déjà utilisé."))
            self.ui.ok.setEnabled(False)

            self.ui.favorite_name.setStyleSheet("QLineEdit{padding-left: 5px; "
                                                "border: 2px solid orange;"
                                                "border-top-left-radius:5px; "
                                                "border-bottom-left-radius: 5px; }")

            return

        self.ui.verification.setIcon(get_icon(valid_icon))
        self.ui.verification.setToolTip(self.tr("C'est tout bon!"))
        self.ui.ok.setEnabled(True)

        self.ui.favorite_name.setStyleSheet("QLineEdit{padding-left: 5px; "
                                            "border: 1px solid #8f8f91;"
                                            "border-right-width: 0px; "
                                            "border-top-left-radius:5px; "
                                            "border-bottom-left-radius: 5px; }")

        if self.mode == "creation":
            self.ui.ok.setText(self.tr("Création"))
            return

        self.ui.ok.setText(self.tr("Renommer"))

    def options_afficher(self):

        self.widget_options.formatting_show(current_parent=self.ui.format_bt,
                                            current_text=self.ui.favorite_name.text(),
                                            show_code=False)

    def options_retour_datas(self, nouveau_texte: str):

        self.ui.favorite_name.setText(nouveau_texte)
        self.changement()

    def enregistrer(self):

        tooltip = self.ui.ok.text()

        if tooltip == self.tr("Renommer"):
            self.modif_termine.emit(self.valeur_actuelle, self.ui.favorite_name.text())

        elif tooltip == self.tr("Mettre à jour"):
            index_item = self.liste_favoris.index(self.ui.favorite_name.text())
            self.creation_termine.emit(self.ui.favorite_name.text(), index_item)

        elif tooltip == self.tr("Création"):
            self.creation_termine.emit(self.ui.favorite_name.text(), -1)

        self.close()

    @staticmethod
    def a___________________end______():
        pass
