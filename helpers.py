from regex_patterns import pattern_celular, pattern_corchetes
from constants import arr_no, arr_yes
import pandas as pd


def array_to_string(arr):
    string = ''
    for (i, item) in enumerate(arr):
        if i > 0:
            string += "\n" + item
        else:
            string += item
    return string


def get_last_index(dataframe: pd.DataFrame):
    """Return the last index of a Pandas Dataframe

    Args:
        dataframe (pd.DataFrame): Is the dataframe to get the last index
    """
    return dataframe[len(dataframe) - 1:].index[0]


def clean_testimony(testimony):
    phone = get_phone_number(testimony)
    warranty = get_warranty_status(testimony, True)
    match_corchetes = pattern_corchetes.search(testimony)
    if match_corchetes:
        testimony = testimony.replace(match_corchetes.group(
            1), '').replace(warranty, '').replace(phone, '')
    else:
        testimony = testimony.replace(warranty, '').replace(phone, '')
    return testimony.replace('[]', '').replace('#', '', 1).strip()


def get_phone_number(strnig):
    match_celular = pattern_celular.search(strnig)
    if match_celular:
        numero_celular = match_celular.group(1)
        numero_celular = numero_celular.replace(' ', '')
        return numero_celular
    return 'Sin celular'


def get_warranty_status(string, raw: bool):
    match_corchetes = pattern_corchetes.search(string)
    string_split = string.split(' ')
    if match_corchetes:
        garantia = string_split[-2]

    else:
        garantia = string_split[-1]
    '''Determina si la orden de servicio es garantía y lo añade a un array de elementos
    '''
    if raw and (garantia in arr_no or garantia in arr_yes):
        return garantia
    else:
        if garantia in arr_no:
            return 'No es garantía'
        elif garantia in arr_yes:
            return 'Es garantía'
        else:
            return ''
