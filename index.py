import sys
import pandas as pd
import re

workbook = pd.read_excel(
    'servicios.xlsx')
workbook.head()

arr_garantia = ['Si', 'No', 'Sí', 'NO', 'SI', 'SÍ', 'si','no']

last_workbook_index = workbook[len(workbook) -1:].index[0]
print(last_workbook_index)
items_cols = ["SKU", "Descripcion", "Cantidad", "Precio unitario",
              "Impuestos", "Porcentaje de descuento", "Subtotal", "Importe"]

os = workbook.dropna(subset=['Folio'], inplace=False)
os.drop(['Ultima modificación'], axis=1, inplace=True)
os.drop(os.columns[os.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
# print(os.index)
servces_index = os.index.append(pd.Index([last_workbook_index]))
print(servces_index)
insumos_col = []
celulares_col = []
garantia_col = []
testimonio_col = []
for inx in range(len(servces_index)-1):
    dispositivo = workbook['Dispositivos Asignados'].iloc[servces_index[inx]][1:]

    garantia = ""
    pattern_celular = re.compile(r'(\d{3}\s?\d{3}\s?\d{4})')
    pattern_corchetes = re.compile(r'\[(.*?)\]')

    dispositivo_split = dispositivo.split(' ')
    dispositivo_split
    match_celular = pattern_celular.search(dispositivo)
    match_corchetes = pattern_corchetes.search(dispositivo)
    
    if match_celular:
        numero_celular = match_celular.group(1)
        dispositivo = dispositivo.replace(numero_celular,'')
        print(dispositivo)
        celulares_col.append(numero_celular)
    else:
        # print(servces_index[inx],"No se encontró un número de celular en el texto.")
        celulares_col.append('Sin numero')
    
    if match_corchetes:
        garantia = dispositivo_split[-2]
        dispositivo = dispositivo.replace(match_corchetes.group(1),'')
        dispositivo = dispositivo.replace(garantia,'')

    else:
        garantia = dispositivo_split[-1]
        dispositivo = dispositivo.replace(garantia,'')

    if garantia in arr_garantia:
        garantia_col.append(garantia.upper())
        
    else:
        garantia_col.append('Desconocido')
        

    items = workbook.iloc[servces_index[inx] +
                          2:servces_index[inx+1]-1, [1, 2, 3, 4, 5, 6, 7, 8]]
    itemsDF = pd.DataFrame(items)
    itemsDF.columns = items_cols
    items_cost=servces_index[inx], list(itemsDF[[
          'Descripcion', 'Importe']].to_dict('list').values())
    products_cost = items_cost[1]
    resultado = [f'{producto} - {precio}' for producto, precio in zip(products_cost[0], products_cost[1])]
    string = ""
    for (i,item) in enumerate(resultado):
        if i > 0:
            string = string + "\n" + item
        else:
            string = string + item 
    
    dispositivo = dispositivo.replace('[]','').strip()
    insumos_col.append(string)
    testimonio_col.append(dispositivo)

os.insert(2,"Contacto", celulares_col)
os.insert(4,"Insumos", insumos_col)
os.insert(5,"Garantía?", garantia_col)
os.rename(columns={'Dispositivos Asignados': 'Testimonio'}, inplace=True)
os['Testimonio'] = testimonio_col
# os.drop(['Ultima modificación'], axis=1, inplace=True)

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('only_services.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
os.to_excel(writer, sheet_name='Servicios', index=False)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Servicios']

# Add a format.
text_format = workbook.add_format({'text_wrap' : True})

# Resize columns for clarity and add formatting to column C.
worksheet.set_column(4, 4, 70, text_format)

# Close the Pandas Excel writer and output the Excel file.
writer.close()
