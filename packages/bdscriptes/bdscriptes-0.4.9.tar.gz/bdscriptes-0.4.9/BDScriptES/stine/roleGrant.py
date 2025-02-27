import discord
import re

def execute(code, ctx=None, args=None):
    """
    Procesa la función $roleGrant[+ID rol;ID usuario;...].
    
    - '+' agrega el rol.
    - '-' quita el rol.
    """
    pattern = r"\$roleGrant\[([+-])(\d+);([\d;]+)]"
    matches = re.findall(pattern, code)

    for sign, role_id, users in matches:
        ctx.bot.loop.create_task(grant_or_remove_role(ctx, sign, int(role_id), users.split(";")))

    return re.sub(pattern, "", code)  # Elimina la función del código para continuar con el procesamiento

async def grant_or_remove_role(ctx, sign, role_id, user_ids):
    """
    Asigna o quita un rol en segundo plano basado en `sign` (+ para agregar, - para quitar).
    """
    role = discord.utils.get(ctx.guild.roles, id=role_id)
    if not role:
        await ctx.send(f"❌ No se encontró el rol con ID `{role_id}`.")
        return

    for user_id in user_ids:
        member = ctx.guild.get_member(int(user_id))
        if not member:
            await ctx.send(f"❌ No se encontró el usuario `{user_id}` en el servidor.")
            continue

        try:
            if sign == "+":
                await member.add_roles(role)
            elif sign == "-":
                await member.remove_roles(role)
        except discord.Forbidden:
            await ctx.send(f"❌ No tengo permisos para modificar roles.")
        except Exception as e:
            await ctx.send(f"❌ Error al modificar roles: {e}")
