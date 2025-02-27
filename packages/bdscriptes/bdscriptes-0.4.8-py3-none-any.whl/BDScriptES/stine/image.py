def execute(code, ctx=None, args=None):
    """
    Procesa múltiples $image[url;indice opcional] y devuelve una lista de tuplas con las URLs y sus índices.
    """
    print(f"Procesando código: {code}")  # Debug
    images = []
    start = 0

    while True:
        start_idx = code.find("$image[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Formato inválido cerca de '{code[start_idx-1:start_idx+10]}...' (Se esperaba '$image[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$image[' no está cerrado con ']'")

        content = code[start_idx + len("$image["):end_idx]
        parts = content.split(";")
        url = parts[0].strip()
        index = int(parts[1].strip()) if len(parts) > 1 and parts[1].strip().isdigit() else 1

        if not url:
            raise ValueError("❌ '$image[]' debe contener una URL.")

        images.append((url, index))  # Agrega la URL con su índice
        start = end_idx + 1  # Continuar la búsqueda después del último cierre de ']'

    print(f"Imágenes procesadas: {images}")  # Debug
    return images
