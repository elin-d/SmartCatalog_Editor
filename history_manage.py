#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from main_datas import attribute_add_icon, delete_icon, get_icon, cut_icon, move_up_icon, move_down_icon, refresh_icon
from main_datas import merge_icon
from hierarchy_qs import folder_code

index_action = Qt.UserRole + 2

ajouter_ele = "ajouter_ele"
couper_ele = "couper_ele"
supprimer_ele = "supprimer_ele"
deplacer_ele = "deplacer_ele"
deplacer_material = "deplacer_material"

modif_icone = "modif_icone"

ajouter_attr = "ajouter_attr"
modifier_attr = "modifier_attr"
supprimer_attr = "supprimer_attr"

library_synchro_code = "library_synchro"

user_data_type = Qt.UserRole + 1

nb_max = 50


class ActionInfo:
    def __init__(self, action_type, nom_action: str, id_action: int, data=None):
        self.action_type = action_type
        self.data = data
        self.nom_action = nom_action
        self.id = id_action


class ActionCreationElement(ActionInfo):
    def __init__(self, id_action: int, nom_action: str, qs_parent: QStandardItem, qs_actuel, index_ele: int,
                 liste_ele: list):
        super().__init__(action_type=ajouter_ele, nom_action=nom_action, id_action=id_action)

        type_actuel: str = qs_actuel.data(user_data_type)

        if type_actuel == folder_code:
            icone = get_icon(qs_actuel.icon_path)
        else:
            icone = get_icon(f":/Images/{type_actuel.lower()}.png")

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "action_type": self.action_type,
                     "icone": icone,
                     "qs_parent": qs_parent,
                     "qs_actuel": qs_actuel,
                     "index_ele": index_ele,
                     "liste_ele": liste_ele}


class ActionCouperEle(ActionInfo):
    def __init__(self, id_action: int, nom_action: str,
                 qs_parent_actuel: QStandardItem, qs_parent_futur: QStandardItem,
                 qs_actuel: QStandardItem,
                 row_actuel: int, row_futur: int, liste_ele: list):
        super().__init__(action_type=couper_ele, nom_action=nom_action, id_action=id_action)

        icone = get_icon(cut_icon)

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "action_type": self.action_type,
                     "icone": icone,
                     "qs_parent_actuel": qs_parent_actuel,
                     "qs_parent_futur": qs_parent_futur,
                     "qs_actuel": qs_actuel,
                     "row_actuel": row_actuel,
                     "row_futur": row_futur,
                     "liste_ele": liste_ele}


class ActionSuppressionElement(ActionInfo):
    def __init__(self, id_action: int, nom_action: str, qs_parent: QStandardItem, qs_actuel, index_ele: int,
                 liste_ele: list):
        super().__init__(action_type=supprimer_ele, nom_action=nom_action, id_action=id_action)

        icone = get_icon(delete_icon)

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "action_type": self.action_type,
                     "icone": icone,
                     "qs_parent": qs_parent,
                     "qs_actuel": qs_actuel,
                     "index_ele": index_ele,
                     "liste_ele": liste_ele}


class ActionDeplacerEle(ActionInfo):
    def __init__(self, id_action: int, nom_action: str, qs_parent: QStandardItem, qs_actuel: QStandardItem,
                 row_actuel: int, row_futur: int):
        super().__init__(action_type=deplacer_ele, nom_action=nom_action, id_action=id_action)

        if row_futur > row_actuel:

            icone = get_icon(move_up_icon)
        else:
            icone = get_icon(move_down_icon)

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "action_type": self.action_type,
                     "icone": icone,
                     "qs_parent": qs_parent,
                     "qs_actuel": qs_actuel,
                     "row_actuel": row_actuel,
                     "row_futur": row_futur}


class ActionMoveMaterial(ActionInfo):
    def __init__(self, id_action: int, nom_action: str, qs_parent: QStandardItem, qs_new_list: list):
        super().__init__(action_type=deplacer_material, nom_action=nom_action, id_action=id_action)

        icone = get_icon(merge_icon)

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "action_type": self.action_type,
                     "icone": icone,
                     "qs_parent": qs_parent,
                     "qs_new_list": qs_new_list}


class ActionModifIcone(ActionInfo):
    def __init__(self, id_action: int, nom_action: str, qs_actuel: QStandardItem, ancien_icone: str, nouvel_icone: str):
        super().__init__(action_type=modif_icone, nom_action=nom_action, id_action=id_action)

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "action_type": self.action_type,
                     "icone": get_icon(nouvel_icone),
                     "qs_actuel": qs_actuel,
                     "ancien_icone": ancien_icone,
                     "nouvel_icone": nouvel_icone}


class ActionAjouterAttribut(ActionInfo):
    def __init__(self, id_action: int, nom_action: str, qs_parent: QStandardItem, index_attribut: int, liste_ele: list,
                 dict_comp: dict, type_attribut=""):
        super().__init__(action_type=ajouter_attr, nom_action=nom_action, id_action=id_action)

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "action_type": self.action_type,
                     "icone": get_icon(attribute_add_icon),
                     "qs_parent": qs_parent,
                     "index_attribut": index_attribut,
                     "liste_ele": liste_ele,
                     "dict_comp": dict_comp,
                     "type_attribut": type_attribut}


class ActionModifierAttribut(ActionInfo):
    def __init__(self, id_action: int, nom_action: str, tooltips: str,
                 qs_parent: QStandardItem, qs_actuel: QStandardItem, index_ele: int,
                 liste_ele: list, ancienne_valeur: str, nouvelle_valeur: str, ancien_index: str, nouvel_index: str,
                 dict_comp=None, type_attribut=""):
        super().__init__(action_type=modifier_attr, nom_action=nom_action, id_action=id_action)

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "action_type": self.action_type,
                     "icone": get_icon(attribute_add_icon),
                     "tooltips": tooltips,
                     "qs_parent": qs_parent,
                     "qs_actuel": qs_actuel,
                     "index_ele": index_ele,
                     "liste_ele": liste_ele,
                     "ancienne_valeur": ancienne_valeur,
                     "nouvelle_valeur": nouvelle_valeur,
                     "ancien_index": ancien_index,
                     "nouvel_index": nouvel_index,
                     "dict_comp": dict_comp,
                     "type_attribut": type_attribut}


class ActionSupprimerAttribut(ActionInfo):
    def __init__(self, id_action: int, nom_action: str, qs_parent: QStandardItem, index_attribut: int, liste_ele: list,
                 dict_comp: dict):
        super().__init__(action_type=supprimer_attr, nom_action=nom_action, id_action=id_action)

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "action_type": self.action_type,
                     "icone": get_icon(delete_icon),
                     "qs_parent": qs_parent,
                     "index_attribut": index_attribut,
                     "liste_ele": liste_ele,
                     "dict_comp": dict_comp}


class ActionLibrarySynchro(ActionInfo):
    def __init__(self, id_action: int, nom_action: str, library_synchro_list: list):
        super().__init__(action_type=library_synchro_code, nom_action=nom_action, id_action=id_action)

        self.data = {"id_action": id_action,
                     "nom_action": nom_action,
                     "icone": get_icon(refresh_icon),
                     "action_type": self.action_type,
                     "library_synchro_list": library_synchro_list}


# Classe pour stocker et gérer les actions
class ActionsData:
    def __init__(self):
        self.dict_actions = dict()
        self.nb_item = 1

    def ajouter_ele(self, nom_action: str, qs_parent: QStandardItem, qs_actuel: QStandardItem,
                    index_ele: int, liste_ele: list):

        action = ActionCreationElement(id_action=self.nb_item,
                                       nom_action=nom_action,
                                       qs_parent=qs_parent,
                                       qs_actuel=qs_actuel,
                                       index_ele=index_ele,
                                       liste_ele=liste_ele)

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def deplacer_ele(self, nom_action: str, qs_parent: QStandardItem, qs_actuel: QStandardItem,
                     row_actuel: int, row_futur: int):

        action = ActionDeplacerEle(id_action=self.nb_item,
                                   nom_action=nom_action,
                                   qs_parent=qs_parent,
                                   qs_actuel=qs_actuel,
                                   row_actuel=row_actuel,
                                   row_futur=row_futur)

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def move_materials(self, nom_action: str, qs_parent: QStandardItem, qs_new_list: list):

        action = ActionMoveMaterial(id_action=self.nb_item,
                                    nom_action=nom_action,
                                    qs_parent=qs_parent,
                                    qs_new_list=qs_new_list)

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def couper_ele(self, nom_action: str, qs_parent_actuel: QStandardItem, qs_parent_futur: QStandardItem,
                   qs_actuel: QStandardItem,
                   row_actuel: int, row_futur: int, liste_ele: list):

        action = ActionCouperEle(id_action=self.nb_item,
                                 nom_action=nom_action,
                                 qs_parent_actuel=qs_parent_actuel,
                                 qs_parent_futur=qs_parent_futur,
                                 qs_actuel=qs_actuel,
                                 row_actuel=row_actuel,
                                 row_futur=row_futur,
                                 liste_ele=liste_ele)

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def suppression_ele(self, nom_action: str, qs_parent: QStandardItem, qs_actuel: QStandardItem,
                        index_ele: int, liste_ele: list):

        action = ActionSuppressionElement(id_action=self.nb_item,
                                          nom_action=nom_action,
                                          qs_parent=qs_parent,
                                          qs_actuel=qs_actuel,
                                          index_ele=index_ele,
                                          liste_ele=liste_ele)

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def modif_icone(self, nom_action: str, qs_actuel: QStandardItem, ancien_icone: str, nouvel_icone: str):

        action = ActionModifIcone(id_action=self.nb_item,
                                  nom_action=nom_action,
                                  qs_actuel=qs_actuel,
                                  ancien_icone=ancien_icone,
                                  nouvel_icone=nouvel_icone)

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def ajouter_attribut(self, nom_action: str, qs_parent: QStandardItem, index_attribut: int, liste_ele: list,
                         dict_comp: dict, type_attribut=""):

        action = ActionAjouterAttribut(id_action=self.nb_item,
                                       nom_action=nom_action,
                                       qs_parent=qs_parent,
                                       index_attribut=index_attribut,
                                       liste_ele=liste_ele,
                                       dict_comp=dict_comp,
                                       type_attribut=type_attribut)

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def modifier_attribut(self, nom_action: str, tooltips: str,
                          qs_parent: QStandardItem, qs_actuel: QStandardItem, index_ele: int,
                          liste_ele: list, ancienne_valeur: str, nouvelle_valeur: str, ancien_index: str,
                          nouvel_index: str, dict_comp=None, type_attribut=""):

        action = ActionModifierAttribut(id_action=self.nb_item,
                                        nom_action=nom_action,
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

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def supprimer_attribut(self, nom_action: str, qs_parent: QStandardItem, index_attribut: int, liste_ele: list,
                           dict_comp: dict):

        action = ActionSupprimerAttribut(id_action=self.nb_item,
                                         nom_action=nom_action,
                                         qs_parent=qs_parent,
                                         index_attribut=index_attribut,
                                         liste_ele=liste_ele,
                                         dict_comp=dict_comp)

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def library_synchro(self, nom_action: str, library_synchro_list: list):

        action = ActionLibrarySynchro(id_action=self.nb_item,
                                      nom_action=nom_action,
                                      library_synchro_list=library_synchro_list)

        self.dict_actions[self.nb_item] = action

        self.gestion_nombre_max()

        self.nb_item += 1

    def creation_liste_action(self) -> list:
        return list(self.dict_actions.keys())

    def supprimer_action(self, nom_action: int):

        if nom_action not in self.dict_actions:
            return

        self.dict_actions.pop(nom_action)
        self.nb_item -= 1

        return

    def gestion_nombre_max(self):

        if self.nb_item > nb_max:
            liste_key = list(self.dict_actions)

            liste_a_sup = liste_key[:len(liste_key) - nb_max]

            for key in liste_a_sup:
                self.dict_actions.pop(key)

    def clear(self):
        self.dict_actions = dict()
        self.nb_item = 1
