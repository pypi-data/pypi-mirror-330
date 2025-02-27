def execute(code, ctx=None, args=None):
    """
    Procesa múltiples $description[texto;indice opcional] y devuelve una lista de tuplas con las descripciones y sus índices.
    """
    print(f"Procesando código: {code}")  # Debug
    descriptions = []
    start = 0

    while True:
        start_idx = code.find("$description[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Formato inválido cerca de '{code[start_idx-1:start_idx+15]}...' (Se esperaba '$description[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$description[' no está cerrado con ']'")

        content = code[start_idx + len("$description["):end_idx]
        parts = content.split(";")
        text = parts[0].strip()
        index = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 1

        if not text:
            raise ValueError("❌ '$description[]' debe contener un texto.")

        descriptions.append((text, index))  # Agrega la descripción con su índice
        start = end_idx + 1  # Continuar la búsqueda después del último cierre de ']'

    print(f"Descripciones procesadas: {descriptions}")  # Debug

    return descriptions
