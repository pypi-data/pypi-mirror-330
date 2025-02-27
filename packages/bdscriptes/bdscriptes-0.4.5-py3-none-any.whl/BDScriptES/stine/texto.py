import re
def execute(code, ctx=None, args=None):
    """
    Extrae y retorna todo el texto fuera de funciones.
    """
    # Expresión regular para detectar funciones del tipo `$funcion[...]`
    patron = re.compile(r'\$\w+\[.*?\]')
    
    # Reemplazar las funciones con una cadena vacía y limpiar espacios adicionales
    texto_sin_funciones = patron.sub('', code).strip()
    
    return texto_sin_funciones if texto_sin_funciones else None