import sys
import pandas as pd
import re
from constants import items_cols
from helpers import get_phone_number, get_warranty_status, clean_testimony

detailed_service_orders = pd.read_excel(
    'servicios_enero.xlsx')
# detailed_purchase_orders = pd.read_excel('oc.xlsx')

products_workbook_df = pd.read_excel('Productos.xlsx')


def procesar_os():

    products_cost_df = products_workbook_df[['SKU', 'Costo']]
    # Clean the table
    simplified_service_orders = detailed_service_orders.dropna(
        subset=['Folio'], inplace=False)
    simplified_service_orders.drop(
        ['Ultima modificación'], axis=1, inplace=True)
    simplified_service_orders.drop(simplified_service_orders.columns[simplified_service_orders.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)

    ordenes_servicio_last_index = get_last_index(detailed_service_orders)
    simplified_service_orders.index.append(
        pd.Index([ordenes_servicio_last_index]))

    simplified_service_orders["Insumos"] = pd.Series()
    simplified_service_orders["Costo total"] = pd.Series()

    simplified_service_orders["Contacto"] = simplified_service_orders.apply(
        lambda row: get_phone_number(row['Dispositivos Asignados']), axis=1)
    simplified_service_orders["Garantía?"] = simplified_service_orders.apply(
        lambda row: get_warranty_status(row['Dispositivos Asignados'], False), axis=1)
    simplified_service_orders["Dispositivos Asignados"] = simplified_service_orders.apply(
        lambda row: clean_testimony(row['Dispositivos Asignados']), axis=1)
    print(simplified_service_orders)
    # for inx, service_order in simplified_service_orders.iterrows():
    #     garantia = ""
    #     (next_inx, next_service_order) = next(
    #         simplified_service_orders.iterrows())
    #     print(inx, next_service_order.index)
    #     dispositivo = service_order['Dispositivos Asignados'][1:]
    #
    #     match_corchetes = pattern_corchetes.search(dispositivo)

    #

    #     dispositivo_split = dispositivo.split(' ')
    #     if match_corchetes:
    #         garantia = dispositivo_split[-2]
    #         dispositivo = dispositivo.replace(match_corchetes.group(1), '')
    #         dispositivo = dispositivo.replace(garantia, '')

    #     else:
    #         garantia = dispositivo_split[-1]
    #         dispositivo = dispositivo.replace(garantia, '')

    #     '''Determina si la orden de servicio es garantía y lo añade a un array de elementos
    #     '''
    #     if garantia in arr_no:
    #         garantia_col.append(False)
    #     elif garantia in arr_yes:
    #         garantia_col.append(True)
    #     else:
    #         garantia_col.append('')

    #     service_order_items = pd.DataFrame(detailed_service_orders.iloc[inx+2:next_inx-2, [
    #         1, 2, 3, 4, 5, 6, 7, 8]])
    #     service_order_items.columns = items_cols
    #     # print(service_order_items)
    #     items_with_costs = service_order_items.merge(
    #         products_cost_df, how='left', on='SKU')
    #     items_cost = inx, list(items_with_costs[[
    #         'Descripcion', 'Costo']].to_dict('list').values())
    #     products_cost = items_cost[1]
    #     resultado = [f'{producto} - {costo}' for producto,
    #                  costo in zip(products_cost[0], products_cost[1])]
    #     string = ""
    #     total_cost = sum(products_cost[1])
    #     for (i, item) in enumerate(resultado):
    #         if i > 0:
    #             string = string + "\n" + item
    #         else:
    #             string = string + item

    #     dispositivo = dispositivo.replace('[]', '').strip()
    #     insumos_col.append(string)
    #     testimonio_col.append(dispositivo)
    #     total_cost_col.append(total_cost)

    simplified_service_orders.rename(
        columns={'Dispositivos Asignados': 'Testimonio'}, inplace=True)
    # simplified_service_orders.drop(['Ultima modificación'], axis=1, inplace=True)
    save_excel(simplified_service_orders, 'only_services', 'Servicios')


def proces_sub_table():
    pass


def get_last_index(dataframe: pd.DataFrame):
    """Return the last index of a Pandas Dataframe

    Args:
        dataframe (pd.DataFrame): Is the dataframe to get the last index
    """
    dataframe[len(dataframe) - 1:].index[0]


def save_excel(df: pd.DataFrame, book_name: str, sheet_name: str):
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(book_name + '.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    # Add a format.
    text_format = workbook.add_format({'text_wrap': True})

    # Resize columns for clarity and add formatting to column C.
    worksheet.set_column(4, 4, 70, text_format)

    # Close the Pandas Excel writer and output the Excel file.
    writer.close()


# if __name__ == 'main':
procesar_os()
