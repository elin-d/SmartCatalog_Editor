#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.QtCore import QCoreApplication

from main_datas import folder_code_list, material_code_list, component_code_list, link_code_list, attribute_code_list, \
    folder_code, material_code, component_code, link_code, attribute_code, language_code


def get_favorites_allplan_dict():
    return {".sgsfnfx": QCoreApplication.translate("gestion_langues", "arêtier"),
            ".rkfanfx": QCoreApplication.translate("gestion_langues", "caisson de store"),
            ".scfanfx": QCoreApplication.translate("gestion_langues", "cheminée"),
            ".swefnfx": QCoreApplication.translate("gestion_langues", "chevêtre"),
            ".spafnfx": QCoreApplication.translate("gestion_langues", "chevron"),
            ".dhfanfx": QCoreApplication.translate("gestion_langues", "couverture"),
            ".defanfx": QCoreApplication.translate("gestion_langues", "dalle"),
            ".ibtfnfx": QCoreApplication.translate("gestion_langues", "élément d'installation"),
            ".sabfnfx": QCoreApplication.translate("gestion_langues", "élément quelconque"),
            ".szafnfx": QCoreApplication.translate("gestion_langues", "entrait moisé"),
            ".skbfnfx": QCoreApplication.translate("gestion_langues", "entrait simple"),
            ".gafanfx": QCoreApplication.translate("gestion_langues", "étage"),
            ".srfanfx": QCoreApplication.translate("gestion_langues", "linteau"),
            ".wafanfx": QCoreApplication.translate("gestion_langues", "mur"),
            ".spffnfx": QCoreApplication.translate("gestion_langues", "panne"),
            ".sspfnfx": QCoreApplication.translate("gestion_langues", "panne-chevron"),
            ".rafanfx": QCoreApplication.translate("gestion_langues", "pièces"),
            ".bffanfx": QCoreApplication.translate("gestion_langues", "pièces - sol"),
            ".sffanfx": QCoreApplication.translate("gestion_langues", "pièces - mur"),
            ".lefanfx": QCoreApplication.translate("gestion_langues", "pièces - plinthe"),
            ".dffanfx": QCoreApplication.translate("gestion_langues", "pièces - plafond"),
            ".spofnfx": QCoreApplication.translate("gestion_langues", "poinçon"),
            ".stfanfx": QCoreApplication.translate("gestion_langues", "poteau"),
            ".uzfanfx": QCoreApplication.translate("gestion_langues", "poutre"),
            ".pfufnfx": QCoreApplication.translate("gestion_langues", "radier général"),
            ".aufanfx": QCoreApplication.translate("gestion_langues", "second-œuvre"),
            ".efufnfx": QCoreApplication.translate("gestion_langues", "semelle isolée"),
            ".sbafnfx": QCoreApplication.translate("gestion_langues", "solive"),
            ".akfanfx": QCoreApplication.translate("gestion_langues", "talon")}


def search_code_in_english(current_code: str) -> str:
    current_code_lower = current_code.lower()

    if current_code_lower in folder_code_list:
        return folder_code

    if current_code_lower in material_code_list:
        return material_code

    if current_code_lower in component_code_list:
        return component_code

    if current_code_lower in link_code_list:
        return link_code

    if current_code.endswith("_"):
        current_code = current_code[:-1]

    if current_code in attribute_code_list:
        return attribute_code

    return current_code


def get_code_langue(langue: str) -> str:
    return language_code.get(langue, "1033")
