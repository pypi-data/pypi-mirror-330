import traceback
import discord
value = None
async def handle_error(ctx, error):
    """
    Maneja errores en el bot y los envía al canal o los imprime en la consola.
    """
    error_message = f"⚠️ **Error:** {str(error)}"

    # Imprime el error detallado en la consola
    traceback.print_exc()
    value = ctx
    # Enviar el error al canal de Discord si hay contexto (ctx)
    if ctx:
        embed = discord.Embed(title="❌ Error", description=error_message, color=discord.Color.red())
        await ctx.send(embed=embed)
