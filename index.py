import sys
import pandas as pd
import re
from constants import items_cols
from helpers import get_phone_number, get_warranty_status, clean_testimony, array_to_string, get_last_index

detailed_service_orders = pd.read_excel(
    'servicios_enero.xlsx')
detailed_purchase_orders = pd.read_excel('oc.xlsx')

products_workbook_df = pd.read_excel('Productos.xlsx')


def procesar_oc():
    items_oc = {}
    simplified_purchase_orders = detailed_purchase_orders.dropna(
        subset=['Folio'], inplace=False)
    purchase_orders_last_index = get_last_index(detailed_purchase_orders)
    purchase_order_indexs = simplified_purchase_orders.index.append(
        pd.Index([purchase_orders_last_index]))

    for inx in range(len(purchase_order_indexs)-1):
        purchase_orders_items = pd.DataFrame(detailed_purchase_orders.iloc[purchase_order_indexs[inx]+2:purchase_order_indexs[inx+1]-1, [
            1, 2, 3, 4, 5, 6, 7, 8]])
        purchase_orders_items.columns = items_cols

        folio = simplified_purchase_orders['Folio'].iloc[inx]

        items_oc[folio] = purchase_orders_items

        # print(purchase_orders_items)
    print(items_oc)
    return items_oc


def procesar_os():
    insumos_col = []
    costos_col = []
    purchase_orders = procesar_oc()
    products_cost_df = products_workbook_df[['SKU', 'Costo']]
    # Clean the table
    simplified_service_orders = detailed_service_orders.dropna(
        subset=['Folio'], inplace=False)

    simplified_service_orders.drop(simplified_service_orders.columns[simplified_service_orders.columns.str.contains(
        'unnamed', case=False)], axis=1, inplace=True)
    simplified_service_orders.drop('Ultima modificación', axis=1, inplace=True)

    simplified_service_orders.rename(
        columns={'Dispositivos Asignados': 'Testimonio', 'Entrego': 'Orden de compra'}, inplace=True)

    ordenes_servicio_last_index = get_last_index(detailed_service_orders)

    # Create contact column
    contact_column = simplified_service_orders.apply(
        lambda row: get_phone_number(row['Testimonio']), axis=1)
    simplified_service_orders.insert(3, 'Contacto', contact_column)
    # Create warranty column
    warranty = simplified_service_orders.apply(
        lambda row: get_warranty_status(row['Testimonio'], False), axis=1)
    simplified_service_orders.insert(5, '¿Garantía?', warranty)
    # Create testimony column
    simplified_service_orders['Testimonio'] = simplified_service_orders.apply(
        lambda row: clean_testimony(row['Testimonio']), axis=1)

    simplified_service_orders['Importe total'] = simplified_service_orders.apply(
        lambda row: round(float(row['Importe total']), 2), axis=1)

    service_orders_indexs = simplified_service_orders.index.append(
        pd.Index([ordenes_servicio_last_index]))

    # Process sub table
    for inx in range(len(service_orders_indexs)-1):
        service_order_items = pd.DataFrame(detailed_service_orders.iloc[service_orders_indexs[inx]+2:service_orders_indexs[inx+1]-1, [
            1, 2, 3, 4, 5, 6, 7, 8]])
        service_order_items.columns = items_cols

        oc = simplified_service_orders['Orden de compra'].iloc[inx]

        items_merge_costs = service_order_items.merge(
            products_cost_df, how='left', on='SKU')

        products_cost = list(items_merge_costs[[
            'SKU', 'Cantidad', 'Descripcion', 'Costo']].to_dict('list').values())

        if (type(oc) != float) and (oc in purchase_orders):
            print(oc)
            elements = []
            oc_items_df = purchase_orders[oc]
            oc_items = list(oc_items_df[[
                'SKU', 'Cantidad', 'Descripcion', 'Importe']].to_dict('list').values())
            for i, item in enumerate(products_cost):
                item += oc_items[i]
                elements.append(item)
            products_cost = elements
            print(products_cost)
            print('\n')

        products_cost_string = [f'{sku} - {quantity} - {producto} - {round(costo, 2)}' for sku, quantity, producto,
                                costo in zip(products_cost[0], products_cost[1], products_cost[2], products_cost[3])]

        total_cost = round(sum(products_cost[3]), 2)
        string = array_to_string(products_cost_string)
        # print(string)
        insumos_col.append(string)
        costos_col.append(total_cost)

    simplified_service_orders.insert(4, "Insumos", insumos_col)
    simplified_service_orders.insert(5, "Costo total", costos_col)

    save_excel(simplified_service_orders, 'only_services', 'Servicios')


def proces_sub_table():
    pass


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
