def execute(code, ctx=None, args=None):
    """
    Procesa múltiples $title[texto;indice opcional] y devuelve una lista de tuplas con los títulos y sus índices.
    """
    print(f"Procesando código: {code}")  # Debug
    titles = []
    start = 0

    while True:
        start_idx = code.find("$title[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Formato inválido cerca de '{code[start_idx-1:start_idx+10]}...' (Se esperaba '$title[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$title[' no está cerrado con ']'")

        content = code[start_idx + len("$title["):end_idx]
        parts = content.split(";")
        title = parts[0].strip()
        index = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 1

        if not title:
            raise ValueError("❌ '$title[]' debe contener un texto.")

        titles.append((title, index))  # Agrega el título con su índice
        start = end_idx + 1  # Continuar la búsqueda después del último cierre de ']'

    print(f"Títulos procesados: {titles}")  # Debug
    return titles
