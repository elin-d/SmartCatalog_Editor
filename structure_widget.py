#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.Qt import *

from main_datas import structure_setting_file
from tools import get_look_treeview, move_window_tool, settings_read, settings_save
from ui_structure import Ui_Structure


class WidgetStructure(QWidget):

    layer_modif = pyqtSignal(str, str)
    remp_modif = pyqtSignal(str, str)

    def __init__(self, asc):
        super().__init__()

        # -----------------------------------------------
        # Parent
        # -----------------------------------------------

        self.asc = asc

        # -----------------------------------------------
        # Création de l'interface
        # -----------------------------------------------

        self.ui = Ui_Structure()
        self.ui.setupUi(self)

        # -----------------------------------------------
        # read settings
        # -----------------------------------------------

        structure_config = settings_read(structure_setting_file)

        self.ismaximized_on = structure_config.get("ismaximized_on", False)
        self.resize(structure_config.get("width", 800), structure_config.get("height", 600))

        # -----------------------------------------------
        # Variables
        # -----------------------------------------------

        self.change_made = False

        self.current_mode = ""
        self.numero_actuel = ""

        self.expanded_indexes = list()
        self.selected_index = None

        self.search_clear_active = False

        self.model_combo = QStandardItemModel()
        self.qcompleter_style = QCompleter()
        self.qcompleter_style.setModel(self.model_combo)
        self.qcompleter_style.setCompletionColumn(1)
        self.qcompleter_style.setCompletionMode(QCompleter.PopupCompletion)
        self.qcompleter_style.setFilterMode(Qt.MatchContains)
        self.qcompleter_style.setCaseSensitivity(Qt.CaseInsensitive)
        self.qcompleter_style.popup().setIconSize(QSize(200, 18))

        self.ui.search.setCompleter(self.qcompleter_style)

        # -----------------------------------------------
        # hierarchy & model & filter
        # -----------------------------------------------

        get_look_treeview(self.ui.tree)

        self.model_tree = QStandardItemModel()

        self.filter_tree = QSortFilterProxyModel()
        self.filter_tree.setSourceModel(self.model_tree)
        self.filter_tree.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filter_tree.setDynamicSortFilter(True)
        self.filter_tree.setRecursiveFilteringEnabled(True)

        self.ui.tree.setModel(self.filter_tree)

        # -----------------------------------------------
        # Signals
        # -----------------------------------------------

        self.ui.search_clear.clicked.connect(self.search_clear)
        self.ui.expand_all.clicked.connect(self.expand_all)
        self.ui.collapse_all.clicked.connect(self.collapse_all)

        self.ui.none.clicked.connect(self.none_selected)
        self.ui.tree.selectionModel().selectionChanged.connect(self.change_event)
        self.ui.tree.doubleClicked.connect(self.doubleclicks)

        self.ui.tree.collapsed.connect(self.save_before_search)
        self.ui.tree.expanded.connect(self.save_before_search)

        self.ui.search.textChanged.connect(self.search_text_changed)

        self.ui.choose.clicked.connect(self.close)
        self.ui.quit.clicked.connect(self.structure_quit)

    @staticmethod
    def a___________________loading______():
        pass

    def widget_structure_show(self,
                              current_mode: str,
                              current_model: QStandardItemModel,
                              current_combo_model: QStandardItemModel,
                              curennt_index: str):
        """
        Permet de charger la liste des styles de surfaces
        :return: None
        """

        # ----------- Reset variables

        self.expanded_indexes = list()
        self.selected_index = None

        # ----------- current mode

        self.current_mode = current_mode

        if current_mode == "layer":
            self.setWindowTitle(self.tr("Layers"))
            self.ui.none.setText(self.tr("Standard"))
        elif current_mode == "remp":
            self.setWindowTitle(self.tr("Style de surface"))
            self.ui.none.setText(self.tr("Aucun"))
        else:
            return

        # ----------- define current_index

        self.numero_actuel = curennt_index

        # ----------- define model & filters to tree

        self.model_tree = current_model
        self.filter_tree.setSourceModel(self.model_tree)

        # ----------- define model to combo

        self.model_combo = current_combo_model

        self.qcompleter_style.setModel(self.model_combo)

        if self.model_tree.rowCount() == 0:
            return

        # ----------- header manage

        header = self.ui.tree.header()

        if header is not None:
            self.ui.tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        # ----------- show widget

        move_window_tool(widget_parent=self.asc, widget_current=self, always_center=True)

        if self.ismaximized_on:

            self.showMaximized()
        else:
            self.show()

        # ----------- define current index

        if self.numero_actuel == "-1" or self.numero_actuel == "0":
            self.ui.tree.setCurrentIndex(self.ui.tree.model().index(0, 0))
            self.ui.search.setFocus()
            self.change_made = False
            return

        recherche = self.model_tree.match(self.model_tree.index(0, 1), Qt.DisplayRole,
                                          self.numero_actuel, 1,
                                          Qt.MatchRecursive)

        if len(recherche) == 0 or len(recherche) > 1:
            self.ui.search.setFocus()
            return

        item_filtre: QModelIndex = recherche[0]

        if item_filtre is None:
            self.ui.search.setFocus()
            return

        item_a_selectionner = self.filter_tree.mapFromSource(item_filtre)

        if item_a_selectionner is None:
            self.ui.search.setFocus()
            return

        item_parent: QModelIndex = item_a_selectionner.parent()

        if item_parent is None:
            self.ui.search.setFocus()
            return

        if self.model_tree.columnCount() == 3:

            grd_parent: QModelIndex = item_parent.parent()

            if grd_parent is None:
                self.ui.search.setFocus()
                return

            item_grd_parent = item_parent.parent()

            self.ui.tree.blockSignals(True)
            self.ui.tree.setExpanded(item_grd_parent, True)
            self.ui.tree.blockSignals(False)

        self.ui.tree.setCurrentIndex(item_a_selectionner)

        self.ui.tree.setExpanded(item_parent, True)

        self.ui.tree.scrollTo(item_a_selectionner, QAbstractItemView.PositionAtCenter)

        self.ui.search.setFocus()

        self.change_made = False

    @staticmethod
    def a___________________change______________():
        pass

    def change_event(self):

        if not self.isVisible():
            return

        self.change_made = True

        if self.ui.search.text() != "":
            return

        if self.search_clear_active:
            return

        print("structure_widget -- change_event")

        selected_item = self.ui.tree.selectionModel().selectedIndexes()

        if len(selected_item) == 0:
            self.selected_index = None
            return

        current_index = selected_item[0]

        if not isinstance(current_index, QModelIndex):
            self.selected_index = None
            return

        self.selected_index = current_index

        print(f"structure_widget -- change_event -- end -- current_index == {current_index.data()}")

    @staticmethod
    def a___________________expand______________():
        pass

    def expand_all(self):

        self.ui.tree.blockSignals(True)

        self.ui.tree.expandAll()

        self.ui.tree.blockSignals(False)

        self.expanded_indexes.clear()

        self.save_expanded_indexes(self.ui.tree.rootIndex())

        if self.ui.tree.currentIndex().isValid():
            self.ui.tree.blockSignals(True)
            self.ui.tree.scrollTo(self.ui.tree.currentIndex(), QAbstractItemView.PositionAtCenter)
            self.ui.tree.blockSignals(False)

    def collapse_all(self):

        self.ui.tree.blockSignals(True)

        self.ui.tree.collapseAll()

        self.ui.tree.blockSignals(False)

        self.selected_index = None

        self.expanded_indexes.clear()

        self.save_expanded_indexes(self.ui.tree.rootIndex())

        self.ui.tree.setCurrentIndex(QModelIndex())

    @staticmethod
    def a___________________search______________():
        pass

    def search_text_changed(self, texte: str):

        print("structure_widget -- search_text_changed")

        try:
            int(texte)
            self.filter_tree.setFilterKeyColumn(1)
        except Exception:
            self.filter_tree.setFilterKeyColumn(0)

        self.filter_tree.setFilterRegExp(texte)

        if len(texte) >= 1 and self.filter_tree.rowCount() > 0:
            self.ui.tree.expandAll()

        if self.ui.tree.currentIndex().isValid():
            self.ui.tree.blockSignals(True)
            self.ui.tree.scrollTo(self.ui.tree.currentIndex(), QAbstractItemView.PositionAtCenter)
            self.ui.tree.blockSignals(False)

    @staticmethod
    def a___________________search_save______________():
        pass

    def save_before_search(self):

        if not self.isVisible():
            return

        if self.ui.search.text() != "":
            return

        if self.search_clear_active:
            return

        print("structure_widget -- save_before_search")

        self.expanded_indexes.clear()

        self.save_expanded_indexes(self.ui.tree.rootIndex())

    def save_expanded_indexes(self, parent_index=QModelIndex()):

        model = self.ui.tree.model()
        rows = model.rowCount(parent_index)

        for row in range(rows):

            index: QModelIndex = model.index(row, 0, parent_index)

            if not model.hasChildren(index):
                continue

            if self.ui.tree.isExpanded(index):
                self.expanded_indexes.append(index)
                self.save_expanded_indexes(index)
        return

    @staticmethod
    def a___________________none_selected______________():
        pass

    def none_selected(self):
        self.selected_index = self.ui.tree.model().index(0, 0)
        self.search_clear()

    @staticmethod
    def a___________________search_clear______________():
        pass

    def search_clear(self):

        print("structure_widget -- search_clear")

        # search -> clear active
        self.ui.tree.blockSignals(True)
        self.search_clear_active = True

        # Clear text -> reset filter
        self.ui.search.clear()

        # collapse all items
        self.ui.tree.collapseAll()

        # restore expanded items before search
        self.restore_expanded_after_search()

        # active signals
        self.ui.tree.blockSignals(False)

        # emit signal -> refresh tree model
        self.ui.tree.expanded.emit(QModelIndex())

        # restore the current item
        self.restore_current_after_search()

        # end off clear search
        self.search_clear_active = False

        # New focus on search line
        self.ui.search.setFocus()

    def restore_expanded_after_search(self):

        if not self.search_clear_active:
            return

        print("structure_widget -- restore_after_search")

        model = self.ui.tree.model()

        for p_index in self.expanded_indexes:

            current_row = p_index.row()
            current_col = p_index.column()
            current_parent = p_index.parent()

            if not isinstance(current_parent, QModelIndex):
                continue

            expanded_index = model.index(current_row,
                                         current_col,
                                         current_parent)

            # print(f"structure_widget -- restore_expanded_after_search -- {expanded_index.data()}")

            if expanded_index.isValid():
                self.ui.tree.setExpanded(expanded_index, True)

    def restore_current_after_search(self):

        if not self.search_clear_active:
            return

        print(f"structure_widget -- restore_current_after_search - start")

        selected_item = self.ui.tree.selectionModel().selectedIndexes()

        if len(selected_item) != 0:

            current_index = selected_item[0]

            if isinstance(current_index, QModelIndex):
                self.selected_index = current_index
                self.ui.tree.blockSignals(True)
                self.ui.tree.scrollTo(current_index, QAbstractItemView.PositionAtCenter)
                self.ui.tree.blockSignals(False)
                self.save_before_search()
                return

        model = self.ui.tree.model()

        if not isinstance(self.selected_index, QModelIndex):
            return

        current_parent = self.selected_index.parent()

        if isinstance(current_parent, QModelIndex):
            print(f"structure_widget -- restore_current_after_search -- parent = {current_parent.data()}")

        selected_index = model.index(self.selected_index.row(),
                                     self.selected_index.column(),
                                     self.selected_index.parent())

        print(f"structure_widget -- restore_current_after_search -- {selected_index.data()}")

        self.ui.tree.setCurrentIndex(selected_index)

        self.ui.tree.blockSignals(True)
        self.ui.tree.scrollTo(self.selected_index, QAbstractItemView.PositionAtCenter)

        self.ui.tree.blockSignals(False)

        self.save_before_search()

    @staticmethod
    def a___________________save______________():
        pass

    def structure_quit(self):

        self.change_made = False
        self.close()

    def structure_save(self):

        liste_item_select: list = self.ui.tree.selectionModel().selectedIndexes()

        if len(liste_item_select) == 0:
            return

        valeur: str = liste_item_select[0].data()
        numero: str = liste_item_select[1].data()

        if numero == "":
            return

        if self.current_mode == "layer":
            self.layer_modif.emit(numero, valeur)
            return

        if self.current_mode == "remp":
            self.remp_modif.emit(numero, valeur)

    def structure_save_setting(self):

        datas_config = settings_read(file_name=structure_setting_file)

        if self.isMaximized():
            screennumber = QApplication.desktop().screenNumber(self)
            screen = QApplication.desktop().screenGeometry(screennumber)

            if isinstance(screen, QRect):
                datas_config["height"] = screen.height()
                datas_config["width"] = screen.width()
                datas_config["ismaximized_on"] = True

                settings_save(file_name=structure_setting_file, config_datas=datas_config)
                return

        datas_config["height"] = self.size().height()
        datas_config["width"] = self.size().width()
        datas_config["ismaximized_on"] = False

        settings_save(file_name=structure_setting_file, config_datas=datas_config)

    def doubleclicks(self):

        current_element: QModelIndex = self.ui.tree.currentIndex()

        if not current_element.isValid():
            return

        flags = current_element.flags()

        if flags == Qt.ItemIsEnabled:
            return

        self.close()

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

    def closeEvent(self, event: QCloseEvent):

        self.structure_save_setting()

        if self.change_made:
            self.structure_save()

        super().closeEvent(event)

    @staticmethod
    def a___________________end______():
        pass
