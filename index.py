from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QFileDialog,
    QLineEdit,
    QTableWidget,
    QApplication,
)
from PySide6.QtCore import QThreadPool, QThread, QTimer, QSize, Qt
from PySide6.QtGui import QCloseEvent, QIcon, QPixmap

from modules.pandas import PandasModel

from ui.mainwindow_ui import Ui_MainWindow

import pandas as pd
import sys
from constants import items_cols, services_colums, purshace_columns
from helpers import (
    get_phone_number,
    get_warranty_status,
    clean_testimony,
    array_to_string,
    get_last_index,
    check_oc_pattern,
    replace_nan,
)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.BtnSearchOSFile.clicked.connect(
            lambda: self.select_file(self.ui.TextOSFilePath)
        )
        self.ui.BtnsSearchOCFile.clicked.connect(
            lambda: self.select_file(self.ui.TextOCFilePath)
        )
        self.ui.BtnSearchProductsFile.clicked.connect(
            lambda: self.select_file(self.ui.TextProductsFilePath)
        )
        self.ui.BtnProcessFiles.clicked.connect(self.process_files)

        # self.ui.TextOSFilePath.setText(
        #     "D:/pixel-data-conversion/Clon Lista de ordenes de servicios - 2024-02-16.xlsx"
        # )
        # self.ui.TextOCFilePath.setText(
        #     "D:/pixel-data-conversion/Ordenes de compras - 2024-02-16.xlsx"
        # )
        # self.ui.TextProductsFilePath.setText("D:/pixel-data-conversion/Productos.xlsx")

    def select_file(self, line_edit: QLineEdit):
        (fname, _) = QFileDialog.getOpenFileName(
            self, "Open file", "c:\\", "Excel (*.xlsx *.xls)"
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

    def procesar_oc(self, filepath):
        items_oc = {}
        detailed_purchase_orders = pd.read_excel(filepath)
        detailed_purchase_orders.drop(detailed_purchase_orders.index[0:7], inplace=True)
        detailed_purchase_orders = detailed_purchase_orders.reset_index(drop=True)
        detailed_purchase_orders = detailed_purchase_orders.set_axis(
            purshace_columns, axis=1
        )
        simplified_purchase_orders = detailed_purchase_orders.dropna(
            subset=["Folio"], inplace=False
        )
        purchase_orders_last_index = get_last_index(detailed_purchase_orders)
        purchase_order_indexs = simplified_purchase_orders.index.append(
            pd.Index([purchase_orders_last_index])
        )

        for inx in range(len(purchase_order_indexs) - 1):
            purchase_orders_items = pd.DataFrame(
                detailed_purchase_orders.iloc[
                    purchase_order_indexs[inx] + 2 : purchase_order_indexs[inx + 1] - 1,
                    [1, 2, 3, 4, 5, 6, 7, 8],
                ]
            )
            purchase_orders_items.columns = items_cols

            folio = simplified_purchase_orders["Folio"].iloc[inx]
            items_oc[folio] = purchase_orders_items

        return items_oc

    def process_products(self, filepath):
        products_workbook_df = pd.read_excel(filepath)
        products_cost_df = products_workbook_df[["SKU", "Costo"]]
        return products_cost_df

    def process_os(self, filepath):
        detailed_service_orders = pd.read_excel(filepath)
        detailed_service_orders.drop(detailed_service_orders.index[0:7], inplace=True)
        detailed_service_orders = detailed_service_orders.set_axis(
            services_colums, axis=1
        )
        detailed_service_orders = detailed_service_orders.reset_index(drop=True)
        # Limpiando el texto de las ordenes de servicio.
        detailed_service_orders["Orden de compra"] = detailed_service_orders.apply(
            lambda row: (
                row["Orden de compra"]
                if check_oc_pattern(row["Orden de compra"])
                else ""
            ),
            axis=1,
        )

        detailed_service_orders["Ultima modificación"] = detailed_service_orders.apply(
            lambda row: (
                row["Ultima modificación"]
                if not type(row["Ultima modificación"]) == float
                else ""
            ),
            axis=1,
        )
        return detailed_service_orders

    def process_files(self):
        insumos_col = []
        costos_col = []
        os_path = self.ui.TextOSFilePath.text()
        oc_path = self.ui.TextOCFilePath.text()
        products_path = self.ui.TextProductsFilePath.text()

        if os_path == "" or oc_path == "" or products_path == "":
            return

        detailed_service_orders = self.process_os(os_path)
        purchase_orders = self.procesar_oc(oc_path)
        products_cost_df = self.process_products(products_path)
        # Clean the table
        simplified_service_orders = detailed_service_orders.dropna(
            subset=["Folio"], inplace=False
        )

        simplified_service_orders.drop(
            simplified_service_orders.columns[
                simplified_service_orders.columns.str.contains("unnamed", case=False)
            ],
            axis=1,
            inplace=True,
        )

        ordenes_servicio_last_index = get_last_index(detailed_service_orders)

        # Create contact column
        contact_column = simplified_service_orders.apply(
            lambda row: get_phone_number(row["Testimonio"]), axis=1
        )
        simplified_service_orders.insert(3, "Contacto", contact_column)
        # Create warranty column
        warranty = simplified_service_orders.apply(
            lambda row: get_warranty_status(row["Testimonio"]), axis=1
        )
        simplified_service_orders.insert(5, "¿Garantía?", warranty)
        # Create testimony column
        simplified_service_orders["Testimonio"] = simplified_service_orders.apply(
            lambda row: clean_testimony(row["Testimonio"]), axis=1
        )

        simplified_service_orders["Importe total"] = simplified_service_orders.apply(
            lambda row: round(float(row["Importe total"]), 2), axis=1
        )

        service_orders_indexs = simplified_service_orders.index.append(
            pd.Index([ordenes_servicio_last_index])
        )

        # Process sub table
        for inx in range(len(service_orders_indexs) - 1):
            service_order_items = pd.DataFrame(
                detailed_service_orders.iloc[
                    service_orders_indexs[inx] + 2 : service_orders_indexs[inx + 1] - 1,
                    [1, 2, 3, 4, 5, 6, 7, 8],
                ]
            )
            service_order_items.columns = items_cols
            substring = "No hay registro"
            filter = service_order_items["SKU"].str.contains(substring)
            service_order_items = service_order_items[~filter]

            oc_full_text = str(simplified_service_orders["Orden de compra"].iloc[inx])
            oc_full_text = oc_full_text.replace(" ", "").replace("/", ",")
            oc_list = oc_full_text.split(",")

            items_merge_costs = service_order_items.merge(
                products_cost_df, how="left", on="SKU"
            )
            items_merge_costs = items_merge_costs[
                items_merge_costs["SKU"].str.contains("Gar001|Gar002|S0005") == False
            ]
            if oc_list != [""]:
                print(oc_list)
                for oc in oc_list:
                    if oc in purchase_orders:
                        items_merge_costs = items_merge_costs[
                            items_merge_costs["SKU"].str.contains("REF COMODÍN|SERV006")
                            == False
                        ]

                        oc_items_df = purchase_orders[oc]
                        oc_items_df["Costo"] = oc_items_df["Importe"]
                        oc_items_df["oc"] = oc_items_df.apply(lambda row: oc, axis=1)
                        items_merge_costs = pd.concat([items_merge_costs, oc_items_df])
                        print(items_merge_costs)

                    else:
                        print("No encontré la orden ", oc)

                products_cost = list(
                    items_merge_costs[["SKU", "Cantidad", "Descripcion", "Costo", "oc"]]
                    .to_dict("list")
                    .values()
                )
                products_cost_string = [
                    f"{sku} - {quantity} - {producto} - {round(costo, 2)} {replace_nan(oc)}".replace(
                        "\n", ""
                    ).replace(
                        "\r", ""
                    )
                    for sku, quantity, producto, costo, oc in zip(
                        products_cost[0],
                        products_cost[1],
                        products_cost[2],
                        products_cost[3],
                        products_cost[4],
                    )
                ]
            else:
                products_cost = list(
                    items_merge_costs[["SKU", "Cantidad", "Descripcion", "Costo"]]
                    .to_dict("list")
                    .values()
                )

                products_cost_string = [
                    f"{sku} - {quantity} - {producto} - {round(costo, 2)}".replace(
                        "\n", ""
                    )
                    for sku, quantity, producto, costo in zip(
                        products_cost[0],
                        products_cost[1],
                        products_cost[2],
                        products_cost[3],
                    )
                ]

            total_cost = round(sum(products_cost[3]), 2)
            string = array_to_string(products_cost_string)
            string.replace("\n", "Error:C")
            insumos_col.append(string)
            costos_col.append(total_cost)

        simplified_service_orders.insert(4, "Insumos", insumos_col)
        simplified_service_orders.insert(5, "Costo total", costos_col)
        simplified_service_orders = simplified_service_orders.reset_index(drop=True)
        self.add_to_table(simplified_service_orders)
        self.save_excel(simplified_service_orders, "only_services", "Servicios")

    def add_to_table(self, df):

        model = PandasModel(parent=self, dataframe=df)
        self.ui.TableServices.horizontalHeader().setStretchLastSection(True)
        self.ui.TableServices.setAlternatingRowColors(True)
        self.ui.TableServices.setSelectionBehavior(QTableWidget.SelectRows)
        print(type(model))
        self.ui.TableServices.setRowCount(model.rowCount())
        self.ui.TableServices.setColumnCount(model.columnCount())
        # Populate the table with data (using QTableWidgetItem)
        for row in range(model.rowCount()):
            for col in range(model.columnCount()):
                item = QTableWidgetItem(model.cell(row, col))
                self.ui.TableServices.setItem(row, col, item)

    def save_excel(self, df: pd.DataFrame, book_name: str, sheet_name: str):
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(book_name + ".xlsx", engine="xlsxwriter")
        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        # Add a format.
        text_format = workbook.add_format({"text_wrap": True})
        # Resize columns for clarity and add formatting to column C.
        worksheet.set_column(4, 4, 70, text_format)
        # Close the Pandas Excel writer and output the Excel file.
        writer.close()


if __name__ == "__main__":
    # freeze_support()
    app = QApplication(sys.argv)

    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec())
