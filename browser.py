#!/usr/bin/python3
# -*- coding: utf-8 -*

import os.path

import clr
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog

from tools import find_folder_path, settings_get, find_filename, settings_save_value

try:
    clr.AddReference("System.Windows.Forms")

    from System.Windows.Forms import OpenFileDialog, SaveFileDialog, FileDialogCustomPlace, DialogResult

    load_ok = True

except Exception as error2:
    print(f"browser -- get_common_dialog_path -- {error2}")
    load_ok = False


def browser_file(parent: QObject, title: str, datas_filters: dict, registry: list, shortcuts_list: list,
                 current_path="", default_path="",
                 file_name="", use_setting_first=True, use_save=False) -> str:
    """

    :param parent: Objet parent
    :param title: Title of dialog
    :param datas_filters:  {"Images" : [".png", ".jpg"], "Pdf" : [".pdf"]}
    :param registry: [file_setting_name, setting_name]
    :param shortcuts_list: shortcut paths list
    :param current_path: current_path
    :param default_path: default_path
    :param file_name: file_name
    :param use_setting_first: True = searh in the registry + current + default // False = current + registry + default
    :param use_save: bool : False = for select file // True = For save file
    :return: Path of select file or empty text
    """

    if not isinstance(title, str) or not isinstance(current_path, str) or not isinstance(default_path, str):
        print(f"browser -- browser_file -- not isinstance(title, str)")
        return ""

    if not isinstance(datas_filters, dict) or not isinstance(registry, list) or not isinstance(shortcuts_list, list):
        print(f"browser -- browser_file -- not isinstance(title, str)")
        return ""

    if not isinstance(file_name, str) or not isinstance(use_setting_first, bool) or not isinstance(use_save, bool):
        print(f"browser -- browser_file -- not isinstance(file_name, str)")
        return ""

    current_folder = find_folder_path(current_path)

    default_folder = find_folder_path(default_path)

    if len(registry) != 2:
        settings_folder = default_folder
    else:
        settings_folder = settings_get(file_name=registry[0], info_name=registry[1])

        if settings_folder is None:
            settings_folder = default_folder

    target_folder = ""

    if not use_setting_first:

        if current_folder != "" and current_folder != "\\" and os.path.exists(current_folder):

            target_folder = f"{current_folder}{file_name}"

        else:

            if settings_folder != "" and settings_folder != "\\" and os.path.exists(settings_folder):

                target_folder = f"{settings_folder}{file_name}"

            else:

                if default_folder != "" and default_folder != "\\" and os.path.exists(default_folder):
                    target_folder = f"{default_folder}{file_name}"

    else:

        if settings_folder != "" and settings_folder != "\\" and os.path.exists(settings_folder):

            target_folder = f"{settings_folder}{file_name}"

        else:

            if current_folder != "" and current_folder != "\\" and os.path.exists(current_folder):

                target_folder = f"{current_folder}{file_name}"

            else:

                if default_folder != "" and default_folder != "\\" and os.path.exists(default_folder):
                    target_folder = f"{default_folder}{file_name}"

    if load_ok == "":

        file_path = browser_file_classic(parent=parent,
                                         title=title,
                                         datas_filters=datas_filters,
                                         target_folder=target_folder,
                                         use_save=use_save)
    else:

        file_path = browser_file_new(title=title,
                                     datas_filters=datas_filters,
                                     shortcuts_list=shortcuts_list,
                                     target_folder=target_folder,
                                     use_save=use_save)

    if file_name == file_path:
        return ""

    if file_path == "":
        return ""

    folder_current = find_folder_path(file_path)

    if folder_current != "" and folder_current != "\\":
        if len(registry) == 2:
            settings_save_value(file_name=registry[0], key_name=registry[1], value=folder_current)

    file_path: str = file_path.replace("/", "\\")

    return file_path

    # if accepter_tous:
    #     return chemin_fichier
    #
    # if use_save:
    #
    #     if len(liste_extensions) == 0:
    #         return chemin_fichier
    #
    #     extension_actuelle = liste_extensions[0]
    #
    #     if chemin_fichier.endswith(extension_actuelle):
    #         return chemin_fichier
    #
    #     chemin_fichier += extension_actuelle
    #     return chemin_fichier
    #
    # for extension in liste_extensions:
    #
    #     extension: str
    #     fichier_upper = chemin_fichier.upper()
    #
    #     if fichier_upper.endswith(extension.upper()):
    #         return chemin_fichier
    #
    # afficher_message(titre=parent.tr("Erreur extension de fichier"),
    #                  message=parent.tr("L'extension du fichier est non valide !"),
    #                  icone_avertissement=True)
    #
    # return ""


def browser_file_classic(parent: QObject, title: str, datas_filters: dict, target_folder: str, use_save=False) -> str:
    extensions_list = list()
    filters_list = list()

    for filter_title, extensions in datas_filters.items():

        for extension in extensions:

            if extension == ".*":
                extensions_list.clear()
                break

            if extension in extensions_list:
                continue

            extensions_list.append(extension)

        extensions: list
        extension_str = f'*{" *".join(extensions)}'
        filters_list.append(f'{filter_title} ({extension_str})')

    filter_str = ";;".join(filters_list)

    if not use_save:

        file_path, _filter = QFileDialog.getOpenFileName(parent=parent,
                                                         caption=title,
                                                         directory=target_folder,
                                                         filter=filter_str)
    else:

        file_path, _filter = QFileDialog.getSaveFileName(parent=parent,
                                                         caption=title,
                                                         directory=target_folder,
                                                         filter=filter_str)

    if not isinstance(file_path, str):
        return ""

    if file_path == "":
        return ""

    return file_path


def browser_file_new(title: str, datas_filters: dict, shortcuts_list: list, target_folder: str, use_save=False) -> str:
    filter_extensions = list()

    for title_filter, extensions in datas_filters.items():

        if not isinstance(extensions, list):
            print(f"browser -- browser_file2 -- not isinstance(extensions, list)")
            continue

        filter_extensions.append(f"{title_filter} (*{';*'.join(extensions)})|*{';*'.join(extensions)}")

    filters = "|".join(filter_extensions)

    # ------------------------------------------
    try:

        if use_save:
            dlg = SaveFileDialog()
        else:
            dlg = OpenFileDialog()

        dlg.CheckFileExists = not use_save

        dlg.Title = title
        dlg.Filter = filters

        dlg.InitialDirectory = find_folder_path(target_folder)

        dlg.FileName = find_filename(target_folder)

        for path in shortcuts_list:
            dlg.CustomPlaces.Add(FileDialogCustomPlace(path))

        result = dlg.ShowDialog()

        if result == DialogResult.Cancel:
            return ""

        filename = dlg.FileName

        if not isinstance(filename, str):
            return ""

        return filename

    except Exception as error:
        print(f"browser -- browser_file2 -- error : {error}")
        return ""
