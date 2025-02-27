def execute(code, ctx=None, args=None):
    """
    Procesa múltiples $color[Color;indice opcional] y devuelve una lista de tuplas con los colores y sus índices.
    """
    print(f"Procesando código: {code}")  # Debug
    colors = []
    start = 0

    while True:
        start_idx = code.find("$color[", start)
        if start_idx == -1:
            break

        # Verifica que el formato sea correcto
        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Formato inválido cerca de '{code[start_idx-1:start_idx+10]}...' (Se esperaba '$color[...]')")

        # Encuentra el cierre del corchete
        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$color[' no está cerrado con ']'")

        content = code[start_idx + len("$color["):end_idx]
        parts = content.split(";")
        color = parts[0].strip()  # El color debe ser el primer elemento

        # Validar color (permitiendo # si está presente)
        if color.startswith("#"):
            color = color[1:]  # Eliminar el '#' si está presente
        if len(color) != 6 or not all(c in "0123456789ABCDEFabcdef" for c in color):
            raise ValueError(f"❌ Color '{color}' no es un código hexadecimal válido.")

        color = f"#{color.upper()}"  # Asegurarse de que esté en formato #RRGGBB

        # Verificar el índice opcional
        index = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 1

        colors.append((color, index))  # Agregar color con su índice
        start = end_idx + 1  # Continuar la búsqueda después del último cierre de ']'

    print(f"Colores procesados: {colors}")  # Debug
    return colors
