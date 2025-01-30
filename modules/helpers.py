import pandas as pd
import re
from modules.regex_patterns import pattern_celular, pattern_corchetes, pattern_purchase
from constants import arr_no, arr_yes
import math
from modules.pandas import PandasModel
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


def array_to_string(arr):
    string = ""
    for i, item in enumerate(arr):
        if i > 0:
            string += "," + item
        else:
            string += item
    return string


def get_last_index(dataframe: pd.DataFrame):
    """Return the last index of a Pandas Dataframe

    Args:
        dataframe (pd.DataFrame): Is the dataframe to get the last index
    """
    return dataframe[len(dataframe) - 1 :].index[0]


def clean_testimony(testimony):
    testimony = testimony.replace("#", "", 1)
    match_corchetes = pattern_corchetes.search(testimony)

    if match_corchetes:
        testimony = testimony.replace(match_corchetes.group(1), "")
    testimony = testimony.strip()

    string_split = testimony.split(" ")

    if string_split[-1] in arr_no or string_split[-1] in arr_yes:
        del string_split[-1]

    testimony = " ".join(string_split)

    testimony = re.sub("^[\d\s]+", "", testimony)
    testimony = re.sub("VIN", "", testimony)
    testimony = testimony.replace("[]", "").strip().capitalize()
    return testimony


def get_phone_number(strnig, raw: bool = False):
    match_celular = pattern_celular.search(strnig)
    if match_celular:
        numero_celular = match_celular.group(1)
        if not raw:
            numero_celular = numero_celular.replace(" ", "")
        return numero_celular

    return "Sin celular"


def add_to_table(self, df, table: QTableWidget):

    model = PandasModel(parent=self, dataframe=df)
    table.horizontalHeader().setStretchLastSection(True)
    table.setAlternatingRowColors(True)
    table.setSelectionBehavior(QTableWidget.SelectRows)
    print(type(model))
    table.setRowCount(model.rowCount())
    table.setColumnCount(model.columnCount())
    # Populate the table with data (using QTableWidgetItem)
    for row in range(model.rowCount()):
        for col in range(model.columnCount()):
            item = QTableWidgetItem(model.cell(row, col))
            table.setItem(row, col, item)


def check_oc_pattern(string):
    string = str(string)
    match_oc = pattern_purchase.search(string)
    if match_oc:
        return True
    return False


def replace_nan(string):
    if type(string) == float:
        print(string, type(string))
        return ""
    return f"({string})"

def replace_nan2(string):
    if type(string) == float:
        # print(string, type(string))
        return ""
    return f"{string}"



def get_warranty_status(string: str, raw: bool = False):
    match_corchetes = pattern_corchetes.search(string)

    if match_corchetes:
        string = string.replace(match_corchetes.group(1), "")
    string = string.strip()
    string_split = string.split(" ")
    garantia = string_split[-1]
    # print(garantia)
    """Determina si la orden de servicio es garantía y lo añade a un array de elementos
    """
    if raw and (garantia in arr_no or garantia in arr_yes):
        return garantia
    else:
        if garantia in arr_no:
            return "No es garantía"
        elif garantia in arr_yes:
            return "Es garantía"
        else:
            return ""
