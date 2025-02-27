def execute(code, ctx=None, args=None):
    """
    Procesa múltiples $thumbnail[url;indice opcional] y devuelve una lista de tuplas con las URLs y sus índices.
    """
    print(f"Procesando código: {code}")  # Debug
    thumbnails = []
    start = 0

    while True:
        start_idx = code.find("$thumbnail[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Formato inválido cerca de '{code[start_idx-1:start_idx+15]}...' (Se esperaba '$thumbnail[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$thumbnail[' no está cerrado con ']'")

        content = code[start_idx + len("$thumbnail["):end_idx]
        parts = content.split(";")
        url = parts[0].strip()
        index = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 1

        if not url:
            raise ValueError("❌ '$thumbnail[]' debe contener una URL.")

        thumbnails.append((url, index))  # Agrega la URL con su índice
        start = end_idx + 1  # Continuar la búsqueda después del último cierre de ']'

    print(f"Thumbnails procesados: {thumbnails}")  # Debug
    return thumbnails
