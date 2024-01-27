import re

# Lista de strings proporcionados
strings = [
    "#4271067882 VIN SI CARGADOR DELL G15 SE LE REALIZO UN PREDIAGNOSTICO DE CAMBIO DE ENTILADO NO [NO]",
    "#4422498123 thinkpad x270 No enciende, parpadea el led de encendido y luego se apagar, le entró virus, se trato de limpiar pero luego fallo no [no]",
    "#442 350 0838 Lenovo T480 cambio de bateria si [pendiente]",
    "#442 350 0838 HP ELITEBOOK 840 G3 No enciende la computadora NO [pendiente]",
    "#442 350 0838 HP ELITEBOOK 840 G3 El teclado no le funciona NO [pendiente]",
    "#4424266609 NA HP 24\" AIO TOUCH REVISAR RUIDO EN VENTILADOR Y REALIZAR MANTENIMIENTO  EQUIPO NO SE HA ABIERTO DESDE QUE SE COMPRÓ  1TB NO [141718]",
    "#4421130676 VIN NO DEJA CARGADOR LENOVO T470S REALIZAR MANTENIMIENTO SIN FORMATEO NO"
]

# Definir un patrón de expresión regular para extraer el número de celular
pattern = re.compile(r'#?(\d{3}\s?\d{3}\s?\d{4})')

# Iterar sobre los strings y extraer el número de celular
for text in strings:
    match = pattern.search(text)
    if match:
        numero_celular = match.group(1)
        print("Número de Celular:", numero_celular)
    else:
        print("No se encontró un número de celular en el texto.")
