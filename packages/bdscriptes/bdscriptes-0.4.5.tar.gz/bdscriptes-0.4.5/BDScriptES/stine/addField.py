def execute(code, ctx=None, args=None):
    """
    Procesa múltiples $addField[Name;Valor;en línea True/False opcional por defecto en False;indice opcional]
    y devuelve una lista de tuplas con los campos (name, value, inline, index).
    """
    print(f"Procesando código: {code}")  # Debug
    add_fields = []
    start = 0

    while True:
        start_idx = code.find("$addField[", start)
        if start_idx == -1:
            break

        if start_idx > 0 and code[start_idx - 1].isalnum():
            raise ValueError(f"❌ Formato inválido cerca de '{code[start_idx-1:start_idx+11]}...' (Se esperaba '$addField[...]')")

        end_idx = code.find("]", start_idx)
        if end_idx == -1:
            raise ValueError("❌ '$addField[' no está cerrado con ']'")

        content = code[start_idx + len("$addField["):end_idx]
        parts = content.split(";")
        
        if len(parts) < 2:
            raise ValueError("❌ '$addField[]' debe contener al menos el nombre y el valor.")

        name = parts[0].strip()
        value = parts[1].strip()

        # Validar si el parámetro 'en línea' está presente y es válido
        inline = False  # Valor por defecto
        if len(parts) > 2:
            inline_part = parts[2].strip().lower()
            if inline_part == "true":
                inline = True
            elif inline_part != "false":
                raise ValueError("❌ El valor de 'en línea' debe ser True o False.")

        # Procesar el índice si está presente
        index = int(parts[3].strip()) if len(parts) > 3 and parts[3].strip().isdigit() else 1

        if not name or not value:
            raise ValueError("❌ '$addField[]' debe contener un nombre y un valor.")

        add_fields.append((name, value, inline, index))  # Agrega el campo con su nombre, valor, inline e índice
        start = end_idx + 1  # Continuar la búsqueda después del último cierre de ']'

    print(f"Campos agregados procesados: {add_fields}")  # Debug
    return add_fields
