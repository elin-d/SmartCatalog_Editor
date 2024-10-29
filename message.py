#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from main_datas import detail_hide_icon, paste_icon, detail_show_icon, information_icon, help_icon, warning_icon
from main_datas import valid_icon, error_icon, save_icon, lock_icon, open_icon, get_icon

from ui_message import Ui_Message
from ui_message_children import Ui_MessageChildren
from ui_message_existing import Ui_MessageExisting
from ui_message_location import Ui_MessageLocation


class WidgetMessage(QDialog):

    def __init__(self):
        super().__init__()

        # Chargement de l'interface
        self.ui = Ui_Message()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.ui.bt_oui.clicked.connect(self.bouton_oui_clicked)
        self.ui.bt_non.clicked.connect(self.bouton_non_clicked)
        self.ui.bt_save.clicked.connect(self.bouton_save_clicked)
        self.ui.bt_annuler.clicked.connect(self.bouton_annuler_clicked)

        self.deplier_actif = False
        self.avec_checkbox = False
        self.save = False

        self.reponse = None
        self.check = False

        self.ht_defaut = 104
        self.ht_chk = 123
        self.ht_details_chk = 126
        self.ht_details = 225

        self.resize(QSize(300, self.ht_defaut))

        self.ui.bt_deplier.clicked.connect(self.gestion_deplier)
        self.ui.bt_deplier.clicked.connect(self.gestion_dimensions)

    def show_message(self, title: str, message: str, infos="",
                     type_bouton=None, defaut_bouton=None,
                     bt_oui=str(), bt_non=str(), bt_annuler=True,
                     icone_question=False, icone_avertissement=False, icone_critique=False, icone_valide=False,
                     icone_sauvegarde=False, icone_lock=False, icone_ouvrir=False,
                     details=None, txt_save=str(), afficher_details=False):
        """
        Permet d'afficher un message
        :param title: Titre de la fenêtre
        :param message: Message à afficher
        :param infos: Checkbox pour ne plus afficher -> nom de l'élément dans la base de registre
        :param type_bouton: Défini le type de bouton :
                            QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel | QMessageBox.Save)

        :param defaut_bouton: Défini le bouton par défaut à selectionner
        :param bt_oui: Texte du bouton oui -> QMessageBox.Ok
        :param bt_non: Texte du bouton non -> QMessageBox.No
        :param bt_annuler: (obsolète)
        :param icone_question: Permet d'afficher l'icône de question
        :param icone_avertissement: Permet d'afficher l'icône de l'avertissement
        :param icone_critique: Permet d'afficher l'icône d'une erreur critique
        :param icone_valide: Permet d'afficher l'icône pour la validation (OK)
        :param icone_sauvegarde: Permet d'affciher l'icône de sauvegarde
        :param icone_lock: Permet d'affciher l'icône de sauvegarde
        :param icone_ouvrir: Permet d'afficher l'icône ouvrir
        :param details: Permet d'afficher plus de détails
        :param txt_save: Permet d'afficher et de modifier le texte -> QMessageBox.Save
        :param afficher_details: Bool permettant d'afficher ou masquer les détails (défaut false)
        :return: None
        """

        # Gestion du titre
        self.setWindowTitle(title)

        # Gestion du message
        self.ui.message.setText(message)

        # Gestion icône
        self.gestion_icone(icone_question,
                           icone_avertissement,
                           icone_critique,
                           icone_valide,
                           icone_sauvegarde,
                           icone_lock,
                           icone_ouvrir)

        # Gestion boutons
        self.gestions_boutons(type_bouton, defaut_bouton, bt_oui, bt_non, bt_annuler, txt_save)

        # Gestion checkbox
        self.gestion_checkbox(infos)

        # Géstion détails
        self.gestion_details(details, afficher_details)

        # Gestion dimensions
        self.gestion_dimensions()

        self.exec()

    def gestion_icone(self, icone_question: bool, icone_avertissement: bool, icone_critique: bool, icone_valide,
                      icone_sauvegarde: bool, icone_lock: bool, icone_ouvrir: bool):
        """
        Permet de gérer les icônes
        :param icone_question: Permet d'afficher l'icône de question
        :param icone_avertissement: Permet d'afficher l'icône de l'avertissement
        :param icone_critique: Permet d'afficher l'icône d'une erreur critique
        :param icone_valide: Permet d'afficher l'icône pour la validation (OK)
        :param icone_sauvegarde: Permet d'affciher l'icône de sauvegarde
        :param icone_lock: Permet d'affciher l'icône cadenas
        :param icone_ouvrir: Permet d'afficher l'icône Ouvrir
        :return: None
        """

        image = information_icon

        if icone_question:
            image = help_icon

        elif icone_avertissement:
            image = warning_icon

        elif icone_critique:
            image = error_icon

        elif icone_valide:
            image = valid_icon

        elif icone_sauvegarde:
            image = save_icon

        elif icone_lock:
            image = lock_icon

        elif icone_ouvrir:
            image = open_icon

        self.ui.icon.setIcon(get_icon(image))

    def gestions_boutons(self, type_bouton=None, defaut_bouton=None,
                         bt_oui=str(), bt_non=str(), bt_annuler=True, txt_save=str()):

        """
        Permet de gérer les textes et l'affichage des boutons
        :param type_bouton: Défini le type de bouton
        :param defaut_bouton: Défini le bouton par défaut à selectionner
        :param bt_oui: Texte du bouton oui -> QMessageBox.Ok
        :param bt_non: Texte du bouton non -> QMessageBox.No
        :param bt_annuler: Permet de cacher le bouton annuler -> QMessageBox.Cancel
        :param txt_save: Permet de changer le nom save -> QMessageBox.Save
        :return: None
        """

        if type_bouton is not None:

            # Bouton seul (4)
            if type_bouton == QMessageBox.No:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_save.setVisible(False)

            elif type_bouton == QMessageBox.Save:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_non.setVisible(False)
                self.ui.bt_annuler.setVisible(False)

            elif type_bouton == QMessageBox.Cancel:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_non.setVisible(False)
                self.ui.bt_save.setVisible(False)

            # Bouton OK (3)
            elif type_bouton == QMessageBox.Ok | QMessageBox.No:
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_save.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.Save:
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_non.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.Cancel:
                self.ui.bt_non.setVisible(False)
                self.ui.bt_save.setVisible(False)

            # Bouton non (2)
            elif type_bouton == QMessageBox.No | QMessageBox.Save:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_annuler.setVisible(False)

            elif type_bouton == QMessageBox.No | QMessageBox.Cancel:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_save.setVisible(False)

            # Bouton save (1)
            elif type_bouton == QMessageBox.Save | QMessageBox.Cancel:
                self.ui.bt_oui.setVisible(False)
                self.ui.bt_non.setVisible(False)

            # Bouton triple
            elif type_bouton == QMessageBox.Ok | QMessageBox.Save | QMessageBox.Cancel:
                self.ui.bt_non.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.No | QMessageBox.Save:
                self.ui.bt_annuler.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel:
                self.ui.bt_save.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.Save | QMessageBox.Cancel:
                self.ui.bt_non.setVisible(False)

            elif type_bouton == QMessageBox.No | QMessageBox.Save | QMessageBox.Cancel:
                self.ui.bt_oui.setVisible(False)

            elif type_bouton == QMessageBox.Ok | QMessageBox.No | QMessageBox.Save | QMessageBox.Cancel:
                pass

            else:
                self.ui.bt_non.setVisible(False)
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_oui.setText("OK")

        else:

            if (bt_oui == "" or bt_oui == "Ok") and bt_non == "" and txt_save == "":
                self.ui.bt_non.setVisible(False)
                self.ui.bt_annuler.setVisible(False)
                self.ui.bt_oui.setText("OK")

        self.ui.bt_oui.setFocus()

        if defaut_bouton is not None:

            if defaut_bouton == QMessageBox.No:
                self.ui.bt_non.setFocus()

            elif defaut_bouton == QMessageBox.Save:
                self.ui.bt_save.setFocus()

            elif defaut_bouton == QMessageBox.Cancel:
                self.ui.bt_annuler.setFocus()

        if bt_oui != "":
            self.ui.bt_oui.setText(f" {bt_oui} ")

        if bt_non != "":
            self.ui.bt_non.setText(f" {bt_non} ")

        if txt_save != "":
            self.ui.bt_save.setVisible(True)
            self.ui.bt_save.setText(f" {txt_save} ")

        else:
            self.ui.bt_save.setVisible(False)

        if not bt_annuler:
            pass

        self.sizeHint()

    def gestion_checkbox(self, infos: str):
        """
        Permet de gérer l'affichage de la checkbox
        :param infos: Checkbox pour ne plus afficher -> nom de l'élément dans la base de registre
        :return: None
        """

        if infos == "":
            self.ui.checkbox.setVisible(False)
            return

        self.avec_checkbox = True

    def gestion_deplier(self):
        """
        Permet de gérer l'affichage de l'icône pour déplier et replier les détails
        :return: None
        """

        self.deplier_actif = not self.deplier_actif

        if self.deplier_actif:

            self.ui.details.setVisible(True)
            self.adjustSize()

            self.ui.bt_deplier.setIcon(get_icon(detail_hide_icon))

        else:

            self.ui.details.setVisible(False)
            self.adjustSize()

            self.ui.bt_deplier.setIcon(get_icon(detail_show_icon))

    def gestion_details(self, details, afficher_details):
        """
        Permet de gérer l'affichage du détail
        :param details: Permet d'afficher plus de détails
        :param afficher_details: Permet d'afficher plus de détails
        :return:
        """

        texte = ""

        if isinstance(details, list):

            nb_caractere = 3

            try:
                nb_items = str(len(details))
                nb_caractere = len(nb_items)

            except ValueError:
                pass

            for index_item in range(len(details)):

                try:

                    index_str = str(index_item)
                    index_str = index_str.zfill(nb_caractere)

                except ValueError:
                    index_str = f"{index_item}"

                texte += f"{index_str} ==> {details[index_item]}\n"

        elif isinstance(details, dict):

            for key in details.keys():
                texte += f"{key} ==> {details[key]}\n"

        else:

            texte = details

        if details is None:

            self.ui.bt_deplier.setVisible(False)

            self.ui.details.setVisible(False)

            self.ui.details.clear()

            self.deplier_actif = False

        elif details == "":

            self.ui.bt_deplier.setVisible(False)

            self.ui.details.setVisible(False)

            self.ui.details.clear()

            self.deplier_actif = False

        else:

            self.ui.bt_deplier.setVisible(True)

            self.ui.details.setVisible(afficher_details)

            self.ui.details.setText(f"{texte}")

            self.deplier_actif = afficher_details

    def gestion_dimensions(self):
        """
        Permet de gérer les dimensions de a boite de dialogue
        :return:None
        """

        if self.check:

            if not self.deplier_actif:
                self.resize(QSize(self.width(), self.ht_chk))

            else:

                if self.size().width() <= 400:
                    self.resize(QSize(400, self.ht_chk))

        else:

            if not self.deplier_actif:

                self.resize(QSize(self.width(), self.ht_defaut))

            else:

                if self.size().width() <= 400:
                    self.resize(QSize(400, self.ht_defaut))

    def bouton_oui_clicked(self):
        """
        Permet de mettre en mémoire la réponse de l'utilisateur = OK
        :return: None
        """
        self.save = True
        self.reponse = QMessageBox.Ok
        self.check = self.ui.checkbox.isChecked()
        # print(f"bouton_ok_clicked -- checkbox == {self.ui.checkbox.isChecked()}")
        self.close()

    def bouton_non_clicked(self):
        """
        Permet de mettre en mémoire la réponse de l'utilisateur = No
        :return:None
        """

        self.save = True
        self.reponse = QMessageBox.No
        self.check = self.ui.checkbox.isChecked()

        # print(f"bouton_no_clicked -- checkbox == {self.ui.checkbox.isChecked()}")
        self.close()

    def bouton_annuler_clicked(self):
        """
        Permet de mettre en mémoire la réponse de l'utilisateur = Cancel
        :return: None
        """

        self.save = True
        self.reponse = QMessageBox.Cancel
        self.check = self.ui.checkbox.isChecked()

        # print(f"bouton_cancel_clicked -- checkbox == {self.ui.checkbox.isChecked()}")

        self.close()

    def bouton_save_clicked(self):
        """
        Permet de mettre en mémoire la réponse de l'utilisateur = Save
        :return: None
        """

        self.save = True
        self.reponse = QMessageBox.Save
        self.check = self.ui.checkbox.isChecked()

        # print(f"bouton_cancel_clicked -- checkbox == {self.ui.checkbox.isChecked()}")

        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if not self.save:
            self.reponse = QMessageBox.Cancel
            self.check = False

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class LoadingSplash(QSplashScreen):

    def __init__(self):
        super().__init__()

        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.setObjectName("loading")
        self.resize(400, 74)

        self.setStyleSheet("QWidget#loading {border: 1px solid #8f8f91; background-color: #FFFFFF; }")

        layout = QVBoxLayout(self)

        self.titre = QLabel()
        font = self.titre.font()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        self.titre.setFont(font)
        self.titre.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.titre)

        progress = QProgressBar()
        progress.setStyleSheet("QProgressBar{border: 1px solid #8f8f91; border-radius:5px;}")

        progress.setMaximum(0)
        progress.setMinimum(0)

        layout.addWidget(progress)

    def launch_show(self, titre: str):
        self.titre.setText(titre)

        self.show()
        self.showMessage("")
        self.setFocus()

    @staticmethod
    def a___________________end______():
        pass


class MessageExisting(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MessageExisting()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.ui.update.clicked.connect(self.update_clicked)
        self.ui.replace.clicked.connect(self.replace_clicked)
        self.ui.duplicate.clicked.connect(self.duplicate_clicked)
        self.ui.quit.clicked.connect(self.quit_clicked)

        txt1 = self.tr("l'élément et ses enfants")
        txt2 = self.tr("Les enfants et les attributs non présents dans le presse-papier")

        bt_maj_txt1 = self.tr("Mettre à jour")
        bt_maj_txt2 = self.tr("ne sont pas supprimés")

        self.ui.update.setToolTip(f"<p style='white-space:pre'><center>{bt_maj_txt1} {txt1} :\n\n"
                                  f"<b>{txt2} <u>{bt_maj_txt2} !")

        bt_remp_txt1 = self.tr("Remplacer")
        bt_remp_txt2 = self.tr("sont supprimés")

        self.ui.replace.setToolTip(f"<p style='white-space:pre'><center>{bt_remp_txt1} {txt1} :\n\n"
                                   f"<b>{txt2} <u>{bt_remp_txt2} !")

        self.reponse = ""

    def show_message_existing(self, message: str, bt_update="", bt_replace="", bt_duplicate="",
                              chk_all=True, checkbox_index=0, checkbox_total=0, checkbox_tooltips="",
                              details=None, default_bouton="bt_maj"):

        texte_chk = self.tr("Appliquer aux éléments suivants")

        self.ui.message.setText(message)

        self.ui.update.setText(f" {bt_update}")
        self.ui.replace.setText(f" {bt_replace}")
        self.ui.duplicate.setText(f" {bt_duplicate}")

        if checkbox_total == 1:
            self.ui.chk_all.setChecked(False)
        else:
            self.ui.chk_all.setChecked(chk_all)

        if checkbox_total == 1 or (checkbox_index == checkbox_total):
            self.ui.chk_all.setEnabled(False)
        else:
            self.ui.chk_all.setEnabled(True)

        if checkbox_total != 1:
            self.ui.chk_all.setText(f"{texte_chk} ({checkbox_index}/{checkbox_total})")
        else:
            self.ui.chk_all.setText(texte_chk)

        self.ui.chk_all.setToolTip(checkbox_tooltips)

        if details is not None:
            texte = "\n".join(details)
            self.ui.details.setText(texte)

        if default_bouton == "bt_maj":
            self.ui.update.setFocus()

        elif default_bouton == "bt_dupliquer":
            self.ui.duplicate.setFocus()

        else:
            self.ui.replace.setFocus()

        self.ui.duplicate.setIcon(get_icon(paste_icon))

        self.exec()

    def update_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.YesAll
        else:
            self.reponse = QMessageBox.Yes

        self.close()

    def replace_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.SaveAll
        else:
            self.reponse = QMessageBox.Save

        self.close()

    def duplicate_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.NoAll
        else:
            self.reponse = QMessageBox.No

        self.close()

    def quit_clicked(self):

        self.reponse = QMessageBox.Cancel
        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if self.reponse == "":
            self.reponse = QMessageBox.Cancel

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class MessageChildren(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MessageChildren()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.ui.ok.clicked.connect(self.yes_clicked)
        self.ui.no.clicked.connect(self.no_clicked)
        self.ui.quit.clicked.connect(self.quit_clicked)

        self.reponse = ""

    def show_message_children(self, message: str, bt_ok="", bt_no="", chk_all=True,
                              checkbox_index=0, checkbox_total=0, checkbox_tooltips="",
                              details=None, default_bouton="ok"):

        text_chk = self.tr("Appliquer aux éléments suivants")

        self.ui.message.setText(message)

        self.ui.ok.setText(bt_ok)
        self.ui.no.setText(bt_no)

        if checkbox_total == 1:
            self.ui.chk_all.setChecked(False)
        else:
            self.ui.chk_all.setChecked(chk_all)

        if checkbox_total == 1 or (checkbox_index == checkbox_total):
            self.ui.chk_all.setEnabled(False)
        else:
            self.ui.chk_all.setEnabled(True)

        if checkbox_total != 1:
            self.ui.chk_all.setText(f"{text_chk} ({checkbox_index}/{checkbox_total})")

        self.ui.chk_all.setToolTip(checkbox_tooltips)

        if details is not None:
            text = "\n".join(details)
            self.ui.details.setText(text)

        if default_bouton == "ok":
            self.ui.ok.setFocus()
        else:
            self.ui.no.setFocus()

        self.exec()

    def yes_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.YesAll
        else:
            self.reponse = QMessageBox.Yes

        self.close()

    def no_clicked(self):

        if self.ui.chk_all.isChecked():
            self.reponse = QMessageBox.NoAll
        else:
            self.reponse = QMessageBox.No

        self.close()

    def quit_clicked(self):

        self.reponse = QMessageBox.Cancel
        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def closeEvent(self, event: QCloseEvent):

        if self.reponse == "":
            self.reponse = QMessageBox.Cancel

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass


class MessageLocation(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MessageLocation()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.ui.tree.doubleClicked.connect(self.ok_clicked)
        self.ui.ok.clicked.connect(self.ok_clicked)

        self.ui.quit.clicked.connect(self.close)

        self.ui.tree.expandAll()

        self.child_txt = ""
        self.parent_txt = ""

        self.reponse = QMessageBox.Cancel

    def show_message_location(self, message: str,
                              parent_txt="", parent_type="",
                              child_txt="", child_type=""):

        self.ui.message.setText(message)

        self.parent_txt = parent_txt
        self.child_txt = child_txt

        self.ui.tree.topLevelItem(0).setText(0, parent_txt)
        self.ui.tree.topLevelItem(0).setIcon(0, get_icon(f":/Images/{parent_type}.png"))

        a = self.tr("Ajouter dans")
        b = self.tr("Frère")
        c = self.tr("Sera frère de")
        d = self.tr("Ajouter après")
        e = self.tr("Enfant")
        f = self.tr("Sera enfant de")
        g = self.tr("Ajouter comme 1er enfant")

        self.ui.tree.topLevelItem(0).child(1).setText(0, f"{a} '{parent_txt}' ({b})")
        self.ui.tree.topLevelItem(0).child(1).setToolTip(0, f"{c} '{parent_txt}' --> "
                                                            f"{d} '{child_txt}'")

        self.ui.tree.topLevelItem(0).child(0).setText(0, child_txt)
        self.ui.tree.topLevelItem(0).child(0).setIcon(0, get_icon(f":/Images/{child_type}.png"))

        self.ui.tree.topLevelItem(0).child(0).child(0).setText(0, f"{a} '{child_txt}' ({e})")
        self.ui.tree.topLevelItem(0).child(0).child(0).setToolTip(0, f"{f} '{child_txt}' --> "
                                                                     f"{g}")

        self.ui.tree.setCurrentItem(self.ui.tree.topLevelItem(0).child(0).child(0))

        self.exec()

    def ok_clicked(self):

        current_item = self.ui.tree.currentItem()

        if current_item is None:
            return None

        current_text = current_item.toolTip(0)

        if self.tr("Sera enfant de") in current_text:
            self.reponse = QMessageBox.Yes
        else:
            self.reponse = QMessageBox.No

        self.close()

    @staticmethod
    def a___________________end______():
        pass
