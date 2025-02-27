import discord
import re

def execute(code, ctx=None, args=None):
    """
    Procesa la función $deleteMessage[channel_id;message_id].
    - Extrae los valores y ejecuta `delete_message` de forma asíncrona.
    - Usa solo `ctx`, sin `bot`.
    """

    while "$deleteMessage[" in code:
        start = code.find("$deleteMessage[") + len("$deleteMessage[")
        end = code.find("]", start)

        if end == -1:
            raise ValueError("❌ Error: Falta cerrar los corchetes en $deleteMessage.")

        params = code[start:end].split(";")

        if len(params) != 2:
            raise ValueError("❌ Error: Se requieren exactamente dos argumentos en $deleteMessage[channel_id;message_id].")

        channel_id, message_id = params

        if not channel_id.isdigit() or not message_id.isdigit():
            raise ValueError("❌ Error: Tanto channel_id como message_id deben ser números enteros válidos.")

        # Llamar a la función async para eliminar el mensaje
        ctx.bot.loop.create_task(delete_message(ctx, int(channel_id), int(message_id)))

        # Reemplazar la función en el código
        code = code[:start - len("$deleteMessage[")] + code[end + 1:]

    return code

async def delete_message(ctx, channel_id, message_id):
    """
    Elimina un mensaje de un canal específico usando solo `ctx`.
    """
    channel = ctx.guild.get_channel(channel_id)
    if channel is None:
        return  # No se encontró el canal, no se ejecuta nada

    try:
        message = await channel.fetch_message(message_id)
        await message.delete()
    except discord.NotFound:
        ValueError("No encontro el mensaje")  # No se encontró el mensaje, ignorar
    except discord.Forbidden:
        ValueError("Sin permisos")  # Sin permisos, ignorar
    except discord.HTTPException as E:
        ValueError("Error: ", E)
