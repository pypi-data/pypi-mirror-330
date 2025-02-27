# process_message_user_id.py

def execute(code, ctx=None, args=None):
    """
    Procesa la función $messageUserID.
    Reemplaza $messageUserID con el ID del usuario que ejecutó el comando.
    """
    if "$messageUserID" in code:
        code = code.replace("$messageUserID", str(ctx.message.id))
    return code