import sys
import pandas as pd

workbook = pd.read_excel(
    'servicios.xlsx')
workbook.head()

items_cols = ["SKU", "Descripcion", "Cantidad", "Precio unitario",
              "Impuestos", "Porcentaje de descuento", "Subtotal", "Importe"]

os = workbook.dropna(subset=['Folio'], inplace=False)
os.drop(['Cliente - Nombre del cliente',
        'Ultima modificación'], axis=1, inplace=True)
os.drop(os.columns[os.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
# print(os.index)
servces_index = os.index
for inx in range(len(servces_index)):
    items = workbook.iloc[servces_index[inx] +
                          2:servces_index[inx+1]-1, [1, 2, 3, 4, 5, 6, 7, 8]]
    itemsDF = pd.DataFrame(items)
    itemsDF.columns = items_cols
    print(servces_index[inx], itemsDF[[
          'Descripcion', 'Importe']])
