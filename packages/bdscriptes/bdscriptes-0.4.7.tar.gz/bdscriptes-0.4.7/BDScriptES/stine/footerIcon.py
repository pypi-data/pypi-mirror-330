def execute(code, ctx=None, args=None):
    """
    Procesa múltiples $footerIcon[url] y devuelve una lista con las URLs de los íconos del pie de página.
    """
    print(f"Procesando código: {code}")  # Debug
    footer_icons = []
    start = 0

    while True:
        start_idx = code.find("$footerIcon[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Formato inválido cerca de '{code[start_idx-1:start_idx+12]}...' (Se esperaba '$footerIcon[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$footerIcon[' no está cerrado con ']'")

        content = code[start_idx + len("$footerIcon["):end_idx].strip()

        if not content:
            raise ValueError("❌ '$footerIcon[]' debe contener una URL.")

        footer_icons.append(content)  # Agrega la URL del ícono del pie de página
        start = end_idx + 1  # Continuar la búsqueda después del último cierre de ']'

    print(f"Íconos de pie de página procesados: {footer_icons}")  # Debug
    return footer_icons
