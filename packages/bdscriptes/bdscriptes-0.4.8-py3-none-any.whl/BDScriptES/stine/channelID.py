def execute(code, ctx=None, args=None):
    """
    Reemplaza $channelID con el ID del canal donde se ejecuta el comando.
    """
    return code.replace("$channelID", str(ctx.channel.id))