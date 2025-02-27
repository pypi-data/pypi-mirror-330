def execute(code, ctx=None, args=None):
    """
    Procesa múltiples $footer[Texto;indice opcional] y devuelve una lista de tuplas con los textos y sus índices.
    """
    print(f"Procesando código: {code}")  # Debug
    footers = []
    start = 0

    while True:
        start_idx = code.find("$footer[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Formato inválido cerca de '{code[start_idx-1:start_idx+10]}...' (Se esperaba '$footer[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$footer[' no está cerrado con ']'")

        content = code[start_idx + len("$footer["):end_idx]
        parts = content.split(";")
        text = parts[0].strip()
        index = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 1

        if not text:
            raise ValueError("❌ '$footer[]' debe contener un texto.")

        footers.append((text, index))  # Agrega el texto con su índice
        start = end_idx + 1  # Continuar la búsqueda después del último cierre de ']'

    print(f"Textos de pie procesados: {footers}")  # Debug
    return footers
