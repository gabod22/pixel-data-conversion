import pandas as pd
import re
from regex_patterns import pattern_celular, pattern_corchetes, pattern_purchase
from constants import arr_no, arr_yes


def array_to_string(arr):
    string = ''
    for (i, item) in enumerate(arr):
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
    return dataframe[len(dataframe) - 1:].index[0]


def clean_testimony(testimony):
    testimony = testimony.replace('#', '', 1)
    match_corchetes = pattern_corchetes.search(testimony)

    string_split = testimony.split(' ')
    if match_corchetes:
        del string_split[-2:]
    else:
        if string_split[-1] in arr_no or string_split[-1] in arr_yes:
            del string_split[-1]

    testimony = ' '.join(string_split)

    testimony = re.sub('^[\d\s]+', '', testimony)
    testimony = re.sub('VIN', '', testimony)
    result = testimony.replace('[]', '').strip().capitalize()
    return result


def get_phone_number(strnig, raw: bool = False):
    match_celular = pattern_celular.search(strnig)
    if match_celular:
        numero_celular = match_celular.group(1)
        if not raw:
            numero_celular = numero_celular.replace(' ', '')
        return numero_celular

    return 'Sin celular'


def check_oc_pattern(string):
    string = str(string)
    match_oc = pattern_purchase.search(string)
    if match_oc:
        return True
    return False


def get_warranty_status(string, raw: bool = False):
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
