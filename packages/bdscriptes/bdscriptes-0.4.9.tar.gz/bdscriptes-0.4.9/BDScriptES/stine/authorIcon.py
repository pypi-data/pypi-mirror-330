def execute(code, ctx=None, args=None):
    """
    Procesa múltiples $authorIcon[url;indice opcional] y devuelve una lista de tuplas con las URLs y sus índices.
    """
    print(f"Procesando código: {code}")  # Debug
    author_icons = []
    start = 0

    while True:
        start_idx = code.find("$authorIcon[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Formato inválido cerca de '{code[start_idx-1:start_idx+15]}...' (Se esperaba '$authorIcon[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$authorIcon[' no está cerrado con ']'")

        content = code[start_idx + len("$authorIcon["):end_idx]
        parts = content.split(";")
        url = parts[0].strip()
        index = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 1

        if not url:
            raise ValueError("❌ '$authorIcon[]' debe contener una URL.")

        author_icons.append((url, index))  # Agrega la URL con su índice
        start = end_idx + 1  # Continuar la búsqueda después del último cierre de ']'

    print(f"Íconos de autor procesados: {author_icons}")  # Debug
    return author_icons
