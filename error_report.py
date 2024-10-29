#!/usr/bin/python3
# -*- coding: utf-8 -*
import datetime
import os.path

from allplan_manage import *
from ui_error_report import Ui_ErrorReport
from tools import afficher_message, find_folder_path, open_folder, open_file, read_file_to_text
from send2trash import send2trash


class ErrorReport(QWidget):

    def __init__(self, asc):
        super().__init__()

        # ---------------------------------------
        # LOADING UI
        # ---------------------------------------

        self.ui = Ui_ErrorReport()
        self.ui.setupUi(self)

        self.setWindowTitle(application_title)

        # ---------------------------------------
        # LOADING PARENT
        # ---------------------------------------

        self.asc = asc
        self.asc.langue_change.connect(lambda main=self: self.ui.retranslateUi(main))

        self.allplan: AllplanDatas = self.asc.allplan

        # ---------------------------------------
        # SIGNAl
        # ---------------------------------------

        self.ui.version_list.currentIndexChanged.connect(self.report_version_changed)

        self.ui.error_edit.clicked.connect(self.report_edit_clicked)
        self.ui.error_open.clicked.connect(self.report_open_clicked)
        self.ui.error_delete.clicked.connect(self.report_delete_clicked)

        self.ui.error_refresh.clicked.connect(self.report_version_changed)

        self.ui.quit.clicked.connect(self.close)

    def report_show(self):

        self.ui.version_list.blockSignals(True)

        version_list = list()

        for version_name, version_obj in self.allplan.version_datas.items():

            if not isinstance(version_obj, AllplanPaths) or not isinstance(version_name, str):
                print("error_report -- report_version_changed -- not isinstance(version_name, str)")
                continue

            if version_name in version_list:
                print("error_report -- report_version_changed -- version_name in version_list")
                continue

            tmp_path = version_obj.tmp_path

            report_path = f"{tmp_path}XML-Validation-Error.log"

            if not os.path.exists(report_path):
                version_list.append(version_name)
                continue

            version_list.append(version_name)

        if len(version_list) == 0:
            afficher_message(titre=self.windowTitle(),
                             message=self.tr("Aucun rapport d'erreurs trouvées."))
            self.ui.version_list.blockSignals(False)
            return False

        version_list.sort(reverse=True)

        self.ui.version_list.clear()
        self.ui.version_list.addItems(version_list)

        if self.allplan.version_allplan_current in version_list:
            index_current = version_list.index(self.allplan.version_allplan_current)

            self.ui.version_list.setCurrentIndex(index_current)

        self.report_version_changed()

        self.ui.version_list.blockSignals(False)

        self.show()

        return True

    @staticmethod
    def a___________________tools______():
        pass

    def report_get_current_path(self) -> str:

        version_current = self.ui.version_list.currentText()

        if version_current not in self.allplan.version_datas:
            print("error_report -- report_get_current_path -- version_current not in self.allplan.version_datas")
            return ""

        version_obj = self.allplan.version_datas[version_current]

        if not isinstance(version_obj, AllplanPaths):
            print("error_report -- report_get_current_path -- not isinstance(version_obj, AllplanPaths)")
            return ""

        tmp_path = version_obj.tmp_path

        report_path = f"{tmp_path}XML-Validation-Error.log"

        if not os.path.exists(report_path):
            return ""

        return report_path

    def report_manage_buttons(self, active: bool):

        self.ui.error_edit.setEnabled(active)
        self.ui.error_open.setEnabled(active)
        self.ui.error_delete.setEnabled(active)
        self.ui.error_refresh.setEnabled(active)

    @staticmethod
    def a___________________version_changed______():
        pass

    def report_version_changed(self):

        self.ui.report.clear()

        report_path = self.report_get_current_path()

        if report_path == "":
            self.ui.report.setPlainText(self.tr("Aucun rapport d'erreurs trouvées."))
            self.ui.error_date.setText(self.tr("Aucun rapport d'erreurs trouvées."))
            self.report_manage_buttons(active=False)

            return

        report_datas = read_file_to_text(file_path=report_path)

        if report_datas == "":

            print(f"error_report -- report_version_changed --report_datas is empty")

            self.ui.report.setPlainText(self.tr("Une erreur est survenue."))
            self.ui.error_date.setText(self.tr("Une erreur est survenue."))
            self.report_manage_buttons(active=False)

            return

        self.report_manage_buttons(active=True)

        self.ui.report.setPlainText(report_datas)

        try:

            timestamp_modification = os.path.getmtime(report_path)

            date_modification = datetime.datetime.fromtimestamp(timestamp_modification)

            date_format = date_modification.strftime('%Y/%m/%d %H:%M')

        except Exception as error:
            print(f"error_report -- report_get_infos -- error : {error}")
            self.ui.error_date.setText(self.tr("Une erreur est survenue."))
            return False

        if not isinstance(date_format, str):
            self.ui.error_date.setText(self.tr("Une erreur est survenue."))
            return False

        txt_modify = self.tr("Date")

        self.ui.error_date.setText(f"{txt_modify} : {date_format}")
        return True

    @staticmethod
    def a___________________buttons______():
        pass

    def report_edit_clicked(self):

        report_path = self.report_get_current_path()

        if report_path == "":
            return

        open_file(file_path=report_path)

    def report_open_clicked(self):

        report_path = self.report_get_current_path()

        if report_path == "":
            return

        folder_path = find_folder_path(file_path=report_path)

        open_folder(folder_path=folder_path)

    def report_delete_clicked(self):

        report_path = self.report_get_current_path()

        if report_path == "":
            return

        if afficher_message(titre=application_title,
                            message=self.tr("Voulez-vous supprimer ce rapport?"),
                            type_bouton=QMessageBox.Ok | QMessageBox.No,
                            defaut_bouton=QMessageBox.Ok,
                            icone_question=True) != QMessageBox.Ok:
            return

        try:
            send2trash(report_path)

        except Exception as error:
            print(f"error_report -- report_delete_clicked -- error : {error}")

        self.report_version_changed()

    @staticmethod
    def a___________________event______():
        pass

    def keyPressEvent(self, event: QKeyEvent):

        if event.key() == Qt.Key_Escape:
            self.close()

        super().keyPressEvent(event)

    @staticmethod
    def a___________________end______():
        pass
