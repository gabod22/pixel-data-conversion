from regex_patterns import pattern_celular, pattern_corchetes
from constants import arr_no, arr_yes


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
        # dispositivo = dispositivo.replace(numero_celular, '')
        return numero_celular
    return 'Sin celular'


def get_warranty_status(string, raw: bool):
    match_corchetes = pattern_corchetes.search(string)
    string_split = string.split(' ')
    if match_corchetes:
        garantia = string_split[-2]

    else:
        garantia = string_split[-1]
    print(garantia)
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
