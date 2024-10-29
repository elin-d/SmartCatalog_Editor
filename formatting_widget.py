#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from main_datas import get_icon, attribute_editable_icon, text_copy_icon
from tools import find_global_point, MyContextMenu


class Formatting(QWidget):
    save_modif_formatage = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.current_code = ""
        self.current_text = ""

    def formatting_show(self, current_parent: QPushButton, current_code="", current_text="",
                        show_code=True, show_search=False):

        self.current_code = current_code
        self.current_text = current_text

        move_x = 300

        menu = MyContextMenu()

        menu.add_title(title=self.tr("Format"))

        menu.add_action(qicon=get_icon(attribute_editable_icon),
                        title=self.tr("Mettre en Majuscule"),
                        action=self.bt_upper_clicked,
                        tooltips=self.current_text.upper())

        menu.add_action(qicon=get_icon(attribute_editable_icon),
                        title=self.tr("Mettre en Minuscule"),
                        action=self.bt_lower_clicked,
                        tooltips=self.current_text.lower())

        menu.add_action(qicon=get_icon(attribute_editable_icon),
                        title=self.tr("Inverser Majuscule et Minuscule"),
                        action=self.bt_swapcase_clicked,
                        tooltips=self.current_text.swapcase())

        menu.add_action(qicon=get_icon(attribute_editable_icon),
                        title=self.tr("Mettre la 1ère lettre en Majuscule"),
                        action=self.bt_capitalize_clicked,
                        tooltips=self.current_text.capitalize())

        menu.add_action(qicon=get_icon(attribute_editable_icon),
                        title=self.tr("Mettre les 1ères lettres en Majuscule"),
                        action=self.bt_title_clicked,
                        tooltips=self.current_text.title())

        if show_code:
            move_x = 368

            menu.add_title(title=self.tr("Code"))

            menu.add_action(qicon=get_icon(text_copy_icon),
                            title=self.tr("Reprendre le texte de l'attribut 'Code'"),
                            action=self.bt_code_clicked,
                            tooltips=self.current_code)

            menu.add_action(qicon=get_icon(text_copy_icon),
                            title=self.tr("Reprendre le texte de l'attribut 'Code' en Majuscule"),
                            action=self.bt_code_upper_clicked,
                            tooltips=self.current_code.upper())

            menu.add_action(qicon=get_icon(text_copy_icon),
                            title=self.tr("Reprendre le texte de l'attribut 'Code' en Minuscule"),
                            action=self.bt_code_lower_clicked,
                            tooltips=self.current_code.lower())

        if show_search:
            move_x = 333

            menu.add_title(title=self.tr("Recherche"))

            menu.add_action(qicon=get_icon(text_copy_icon),
                            title=self.tr("Reprendre la valeur recherchée"),
                            action=self.bt_search_clicked,
                            tooltips=self.current_code)

            menu.add_action(qicon=get_icon(text_copy_icon),
                            title=self.tr("Reprendre la valeur recherchée en Majuscule"),
                            action=self.bt_search_upper_clicked,
                            tooltips=self.current_code.upper())

            menu.add_action(qicon=get_icon(text_copy_icon),
                            title=self.tr("Reprendre la valeur recherchée en Minuscule"),
                            action=self.bt_search_lower_clicked,
                            tooltips=self.current_code.lower())

        point = find_global_point(widget=current_parent)

        point = QPoint(point.x() - move_x + current_parent.width(), point.y())

        menu.exec_(point)

    @staticmethod
    def a___________________modifications______():
        pass

    def bt_upper_clicked(self):

        if not self.verification_text(self.current_text):
            return

        self.save_modification(self.current_text.upper())

    def bt_lower_clicked(self):

        if not self.verification_text(self.current_text):
            return

        self.save_modification(self.current_text.lower())

    def bt_swapcase_clicked(self):

        if not self.verification_text(self.current_text):
            return

        self.save_modification(self.current_text.swapcase())

    def bt_capitalize_clicked(self):

        if not self.verification_text(self.current_text):
            return

        self.save_modification(self.current_text.capitalize())

    def bt_title_clicked(self):

        if not self.verification_text(self.current_text):
            return

        self.save_modification(self.current_text.title())

    @staticmethod
    def a___________________copy_code______():
        pass

    def bt_code_clicked(self):

        if not self.verification_text(self.current_code):
            return

        self.save_modification(self.current_code)

    def bt_code_upper_clicked(self):

        if not self.verification_text(self.current_code):
            return

        self.save_modification(self.current_code.upper())

    def bt_code_lower_clicked(self):

        if not self.verification_text(self.current_code):
            return

        self.save_modification(self.current_code.lower())

    @staticmethod
    def a___________________search_value______():
        pass

    def bt_search_clicked(self):

        if not self.verification_text(self.current_code):
            return

        self.save_modification(self.current_code)

    def bt_search_upper_clicked(self):

        if not self.verification_text(self.current_code):
            return

        self.save_modification(self.current_code.upper())

    def bt_search_lower_clicked(self):

        if not self.verification_text(self.current_code):
            return

        self.save_modification(self.current_code.lower())

    @staticmethod
    def a___________________checking______():
        pass

    def verification_text(self, current_text: str) -> bool:

        if not isinstance(current_text, str):
            self.hide()
            return False
        return True

    @staticmethod
    def a___________________save______():
        pass

    def save_modification(self, current_text: str):
        self.save_modif_formatage.emit(current_text)
        self.hide()

    @staticmethod
    def a___________________end______():
        pass
