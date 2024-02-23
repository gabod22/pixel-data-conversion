import re
pattern_celular = re.compile(r'(\d{3}\s?\d{3}\s?\d{4})')
pattern_corchetes = re.compile(r'\[(.*?)\]')
pattern_purchase = re.compile(r'(PO[0-9]{5}){1,}(?:,)|(PO[0-9]{5}){1,}')
