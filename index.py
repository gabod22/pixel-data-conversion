from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QFileDialog,
    QLineEdit,
    QApplication,
)
from PySide6.QtCore import QThreadPool, QThread, QTimer, QSize, Qt
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap


from ui.mainwindow_ui import Ui_MainWindow
from process_dialog import ProcessDialog

import pandas as pd
import sys
from os import path


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.process_dialog = None
        dirname = path.dirname(__file__)
        self.exe_dirname = path.dirname(sys.executable)

        icon = QIcon()
        icon.addFile(path.join(dirname, "icono.ico"), QSize(), QIcon.Normal, QIcon.Off)
        print(dirname)
        self.setWindowIcon(icon)

        self.ui.BtnSearchOSFile.clicked.connect(
            lambda: self.select_file(self.ui.TextOSFilePath)
        )
        self.ui.BtnsSearchOCFile.clicked.connect(
            lambda: self.select_file(self.ui.TextOCFilePath)
        )
        self.ui.BtnSearchProductsFile.clicked.connect(
            lambda: self.select_file(self.ui.TextProductsFilePath)
        )
        self.ui.BtnProcessFiles.clicked.connect(self.start_process_dialog)

        # self.ui.TextOSFilePath.setText(
        #     "D:/pixel-data-conversion/Clon Lista de ordenes de servicios - 2024-02-16.xlsx"
        # )
        # self.ui.TextOCFilePath.setText(
        #     "D:/pixel-data-conversion/Ordenes de compras - 2024-02-16.xlsx"
        # )
        # self.ui.TextProductsFilePath.setText("D:/pixel-data-conversion/Productos.xlsx")

    def select_file(self, line_edit: QLineEdit):
        (fname, _) = QFileDialog.getOpenFileName(
            self, "Open file", self.exe_dirname, "Excel (*.xlsx *.xls)"
        )
        print(fname)
        line_edit.setText(fname)

    def keyPressEvent(self, event) -> None:
        super().keyPressEvent(event)
        try:
            # Check keyboard input(Ctrl + V) to accomplish of paste
            if event.key() == Qt.Key.Key_V and (
                event.modifiers() & Qt.KeyboardModifier.ControlModifier
            ):
                selection = self.ui.TableServices.selectedIndexes()

                if selection:
                    # Get the first selected cell position
                    row_anchor = selection[0].row()
                    column_anchor = selection[0].column()

                    # Create clipboard object to read data from clipboard
                    clipboard = QApplication.clipboard()
                    # Get data list from clipboard
                    rows = clipboard.text().split("\n")

                    # Add more rows if current row count doesn't match the new row count needed
                    if self.ui.TableServices.rowCount() < row_anchor + len(rows) - 1:
                        self.ui.TableServices.setRowCount(row_anchor + len(rows) - 1)

                    # Show data in table widget which gets from Excel file
                    for index_row, row in enumerate(rows):
                        values = row.split("\t")
                        for index_col, value in enumerate(values):
                            item = QTableWidgetItem(value)
                            self.ui.TableServices.setItem(
                                row_anchor + index_row, column_anchor + index_col, item
                            )

            # Check keyboard input(Ctrl + C) to accomplish copy
            # Check keyboard input(Ctrl + X) to accomplish cut
            if (event.key() == Qt.Key.Key_C or event.key() == Qt.Key.Key_X) and (
                event.modifiers() & Qt.KeyboardModifier.ControlModifier
            ):
                # get the selection section data
                copied_cell = sorted(self.ui.TableServices.selectedIndexes())
                # Define a variable to save selected data
                copy_text = ""
                max_column = copied_cell[-1].column()
                for cell in copied_cell:
                    # Get each cell text
                    cell_item = self.ui.TableServices.item(cell.row(), cell.column())
                    if cell_item:
                        copy_text += cell_item.text()
                        # Clear data in table widget when it cuts data
                        if event.key() == Qt.Key.Key_X:
                            cell_item.setText("")

                    else:
                        copy_text += ""

                    # Format the copied data for paste into Excel file
                    if cell.column() == max_column:
                        copy_text += "\n"
                    else:
                        copy_text += "\t"

                # Save data into clipboard
                QApplication.clipboard().setText(copy_text)

        except Exception as e:
            print(e)
            pass

    def start_process_dialog(self):
        self.process_dialog = ProcessDialog(self)
        self.process_dialog.show()


if __name__ == "__main__":
    # freeze_support()
    app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec())
