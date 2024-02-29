from PySide6.QtCore import QThreadPool, QThread, Qt
from PySide6.QtWidgets import QDialog, QTableWidgetItem
import pandas as pd
from ui.process_dialog_ui import Ui_ProcessDialog
from modules.worker import Worker
from tabulate import tabulate

from constants import items_cols, services_colums, purshace_columns
from modules.helpers import (
    get_phone_number,
    get_warranty_status,
    clean_testimony,
    array_to_string,
    get_last_index,
    check_oc_pattern,
    replace_nan,
    add_to_table,
)


class ProcessDialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.parent = parent
        self.ui = Ui_ProcessDialog()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()
        self.ui.BtnAccept.setEnabled(False)
        self.ui.BtnCancel.setEnabled(False)
        self.ui.BtnAccept.clicked.connect(lambda: self.close())
        self.thread_process_files()

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
        detailed_service_orders = pd.read_excel(
            filepath, converters={"Unnamed: 3": str}
        )
        # print(detailed_service_orders)
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

    def thread_process_files(self):
        worker = Worker(self.process_files)
        # worker.signals.result.connect(self.printDiksInfo)
        worker.signals.finished.connect(self.enable_close)
        worker.signals.progress.connect(self.ui.TextProcessLog.appendPlainText)
        self.threadpool.start(worker)

    def enable_close(self):
        self.ui.BtnAccept.setEnabled(True)

    def process_files(self, progress_callback, on_error, show_dialog):
        progress_callback.emit("Iniciando procesamiento de los archivos")
        insumos_col = []
        costos_col = []
        progress_callback.emit("Obteniendo la ubicacion de los archivos")
        os_path = self.parent.ui.TextOSFilePath.text()
        oc_path = self.parent.ui.TextOCFilePath.text()
        products_path = self.parent.ui.TextProductsFilePath.text()

        if os_path == "" or oc_path == "" or products_path == "":
            on_error.emit(("error", "Falta la ubicación de algún documento"))

        progress_callback.emit("Importando ordenes de servicio")
        detailed_service_orders = self.process_os(os_path)
        progress_callback.emit("Importando ordenes de compra")
        purchase_orders = self.procesar_oc(oc_path)
        progress_callback.emit("Importando productos")
        products_cost_df = self.process_products(products_path)
        # Clean the table
        progress_callback.emit("Simplificando excel de ordenes de servicio")
        simplified_service_orders = detailed_service_orders.dropna(
            subset=["Folio"], inplace=False
        )
        progress_callback.emit("Modificando columndas")
        simplified_service_orders.drop(
            simplified_service_orders.columns[
                simplified_service_orders.columns.str.contains("unnamed", case=False)
            ],
            axis=1,
            inplace=True,
        )

        ordenes_servicio_last_index = get_last_index(detailed_service_orders)
        progress_callback.emit("Obteniendo telefono")
        # Create contact column
        contact_column = simplified_service_orders.apply(
            lambda row: get_phone_number(row["Testimonio"]), axis=1
        )
        simplified_service_orders.insert(3, "Contacto", contact_column)
        # Create warranty column
        progress_callback.emit("Obteniendo garantía")
        warranty = simplified_service_orders.apply(
            lambda row: get_warranty_status(row["Testimonio"]), axis=1
        )
        simplified_service_orders.insert(5, "¿Garantía?", warranty)
        # Create testimony column
        progress_callback.emit("Obteniendo testimonio")
        simplified_service_orders["Testimonio"] = simplified_service_orders.apply(
            lambda row: clean_testimony(row["Testimonio"]), axis=1
        )
        progress_callback.emit("Modificando el importe total")
        simplified_service_orders["Importe total"] = simplified_service_orders.apply(
            lambda row: round(float(row["Importe total"]), 2), axis=1
        )

        service_orders_indexs = simplified_service_orders.index.append(
            pd.Index([ordenes_servicio_last_index])
        )

        # Process sub table
        progress_callback.emit("Procesando los elementos de la orden de servicio")
        for inx in range(len(service_orders_indexs) - 1):
            os = str(detailed_service_orders["Folio"].iloc[service_orders_indexs[inx]])
            progress_callback.emit("Procesando orden: " + os)
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

            service_order_items["Cantidad"] = service_order_items["Cantidad"].astype(
                float
            )

            # print(os)
            # for i in service_order_items.index:
            #     print(
            #         service_order_items["Cantidad"][i],
            #         type(service_order_items["Cantidad"][i]),
            #     )

            oc_full_text = str(simplified_service_orders["Orden de compra"].iloc[inx])
            oc_full_text = oc_full_text.replace(" ", "").replace("/", ",")
            oc_list = oc_full_text.split(",")

            items_merge_costs = service_order_items.merge(
                products_cost_df, how="left", on="SKU"
            )
            items_merge_costs = items_merge_costs[
                items_merge_costs["SKU"].str.contains("Gar001|Gar002") == False
            ]

            # print(tabulate(items_merge_costs, headers="keys", tablefmt="psql"))
            items_merge_costs["Sub Costo Total"] = items_merge_costs.apply(
                lambda row: float(row["Cantidad"]) * float(row["Costo"]), axis=1
            )
            # print("despeus")
            # print(tabulate(items_merge_costs, headers="keys", tablefmt="psql"))
            # print(items_merge_costs.style)
            if oc_list != [""]:
                print(oc_list)
                for oc in oc_list:
                    if oc in purchase_orders:
                        progress_callback.emit("Agregando información de la OC:" + oc)
                        items_merge_costs = items_merge_costs[
                            items_merge_costs["SKU"].str.contains("REF COMODÍN|SERV006")
                            == False
                        ]

                        oc_items_df = purchase_orders[oc]
                        oc_items_df["Sub Costo Total"] = oc_items_df["Importe"]
                        oc_items_df["oc"] = oc_items_df.apply(lambda row: oc, axis=1)
                        progress_callback.emit(
                            "Agregando la info nueva a la orden de servicio"
                        )
                        items_merge_costs = pd.concat([items_merge_costs, oc_items_df])

                    else:
                        items_merge_costs["oc"] = items_merge_costs.apply(
                            lambda row: "", axis=1
                        )
                        progress_callback.emit("No se encontró la orden " + oc)
                        print("No encontré la orden ", oc)
            else:
                items_merge_costs["oc"] = items_merge_costs.apply(
                    lambda row: "", axis=1
                )
            products_cost = list(
                items_merge_costs[
                    ["SKU", "Cantidad", "Descripcion", "Sub Costo Total", "oc"]
                ]
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

            total_cost = round(sum(products_cost[3]), 2)
            string = array_to_string(products_cost_string)
            string.replace("\n", "Error:C")
            insumos_col.append(string)
            costos_col.append(total_cost)

        simplified_service_orders.insert(4, "Insumos", insumos_col)
        simplified_service_orders.insert(5, "Costo total", costos_col)
        simplified_service_orders = simplified_service_orders.reset_index(drop=True)
        progress_callback.emit("Agregando resultado a la tabla")
        add_to_table(self, simplified_service_orders, self.parent.ui.TableServices)

        # self.save_excel(simplified_service_orders, "only_services", "Servicios")
