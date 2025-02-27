import discord
from discord.ext import commands
import os
import importlib
from BDScriptES.utils.handler_error import handle_error  # Manejador de errores
from BDScriptES.stine.conditions import execute as execute_conditions  # Motor de condiciones

class Cliente(commands.Bot):
    def __init__(self, prefijo, ignorar_prefijo=False):
        intents = discord.Intents().all()
        intents.message_content = True
        intents.reactions = True

        super().__init__(command_prefix=prefijo if isinstance(prefijo, list) else [prefijo],
                         intents=intents, case_insensitive=ignorar_prefijo)
        self.commands_registry = {}
        self.function_handlers = {}
        self.event_handlers = {
            'on_message': {},
            'on_raw_reaction_add': {},
            'on_raw_reaction_remove': {},
        }
        self.load_functions()

    def load_functions(self):
        folder = "BDScriptES/stine"
        for filename in os.listdir(folder):
            if filename.endswith(".py"):
                module_name = f"{folder}.{filename[:-3]}"
                module = importlib.import_module(module_name)
                self.function_handlers[filename[:-3]] = module

    def nuevo_comando(self, nombre, tipo, codigo, alias=None):




        self.commands_registry[nombre] = {
            "tipo": tipo,
            "codigo": codigo,
            "alias": alias or [],
        }

        async def command_function(ctx, *args):
            try:
                await self.ejecutar_codigo(ctx, codigo, *args)
            except Exception as e:
                await handle_error(ctx, e)

        command = commands.Command(
            command_function,
            name=nombre,
            aliases=alias or [],
        )
        self.add_command(command)

    async def ejecutar_codigo(self, ctx, codigo, *args, canal_id=None):
        try:
            print(f"Procesando código: {codigo}")

            # Ejecutar condiciones primero
            codigo = execute_conditions(codigo, ctx)
            embeds = {}

            # Procesar `$loop` primero
            if "loop" in self.function_handlers:
                loop_module = self.function_handlers["loop"]
                if hasattr(loop_module, "execute"):
                    prev_codigo = None
                    contador = 0  # Seguridad para evitar bucle infinito

                    while "$loop[" in codigo and prev_codigo != codigo:
                        prev_codigo = codigo
                        codigo = loop_module.execute(codigo)

                        contador += 1
                        print(f"Iteración {contador} - Resultado de loop: {codigo}")

                        if contador > 100:
                            print("⚠️ Se alcanzó el límite de iteraciones del loop.")
                            break

            # Procesar otras funciones después
            for func_name, module in self.function_handlers.items():
                if func_name in ["loop", "conditions"]:  # Ya se procesó
                    continue

                if hasattr(module, "execute"):
                    prev_codigo = None

                    # Procesar funciones sin `[` (como `$guildID`)
                    while f"${func_name}" in codigo and f"${func_name}[" not in codigo:
                        resultado = module.execute(codigo, ctx, args)
                        if resultado:
                            codigo = resultado  # Reemplazamos directamente

                    # Procesar funciones con `[` primero
                    while f"${func_name}[" in codigo and prev_codigo != codigo:
                        prev_codigo = codigo
                        resultado = module.execute(codigo, ctx, args)

                        if resultado:
                            if isinstance(resultado, str):
                                codigo = resultado  # Reemplazamos el código
                            else:
                                for res in resultado:
                                    text, index = res if isinstance(res, tuple) else (res, 1)
                                    index = int(index) if index else 1
                                    if index not in embeds:
                                        embeds[index] = discord.Embed()

                                    # Procesamiento de embeds
                                    if func_name == "title":
                                        embeds[index].title = text
                                    elif func_name == "description":
                                        embeds[index].description = text
                                    elif func_name == "addField":
                                        name, value, inline, idx = text.split(';')
                                        inline = inline.lower() == 'true'
                                        idx = int(idx) if idx else 1
                                        embeds[idx].add_field(name=name, value=value, inline=inline)
                                    elif func_name == "thumbnail":
                                        embeds[index].set_thumbnail(url=text)
                                    elif func_name == "footer":
                                        embeds[index].set_footer(text=text)
                                    elif func_name == "footerIcon":
                                        embeds[index].set_footer(icon_url=text)
                                    elif func_name == "image":
                                        embeds[index].set_image(url=text)
                                    elif func_name == "author":
                                        name, icon_url, url = text.split(';')
                                        embeds[index].set_author(name=name, icon_url=icon_url, url=url)
                                    elif func_name == "color":
                                        embeds[index].color = discord.Color(int(text.lstrip('#'), 16))

            # Enviar los embeds generados
            if embeds:
                for index in sorted(embeds.keys()):
                    embed = embeds[index]
                    if canal_id is None:
                       await ctx.send(embed=embed)
                    else:
                        await canal_id.send(embed=embed)


            # Enviar texto fuera de embeds
            texto_fuera_de_funciones = codigo
            for func_name in self.function_handlers:
                while f"${func_name}[" in texto_fuera_de_funciones:
                    start_idx = texto_fuera_de_funciones.find(f"${func_name}[")
                    end_idx = texto_fuera_de_funciones.find("]", start_idx) + 1
                    if end_idx > 0:
                        texto_fuera_de_funciones = texto_fuera_de_funciones[:start_idx] + texto_fuera_de_funciones[end_idx:]

# Enviar texto fuera de embeds
            texto_fuera_de_funciones = texto_fuera_de_funciones.strip()
            print("text: ", texto_fuera_de_funciones)
            if texto_fuera_de_funciones:
                print("text2: ", texto_fuera_de_funciones)
                if canal_id is None:
                    await ctx.send(texto_fuera_de_funciones)
                else:
                    await canal_id.send(texto_fuera_de_funciones)

        except Exception as e:
            await handle_error(ctx, e)  # Captura cualquier error y lo maneja



    async def on_ready(self):
        print(f"✅ Bot conectado como {self.user}")

    
    def nuevo_evento(self, tipo, codigo, canal_id=None):
        if tipo not in self.event_handlers:
            self.event_handlers[tipo] = {}
        if canal_id not in self.event_handlers[tipo]:
            self.event_handlers[tipo][canal_id] = []
        self.event_handlers[tipo][canal_id].append(codigo)

    async def on_message(self, message):
        if message.author == self.user:
            return

        canal_id = message.channel.id
        if 'on_message' in self.event_handlers:
            # Ejecutar manejadores específicos del canal
            if canal_id in self.event_handlers['on_message']:
                for codigo in self.event_handlers['on_message'][canal_id]:
                    ctx = await self.get_context(message)
                    await self.ejecutar_codigo(ctx, codigo, canal_id=message.channel)
            # Ejecutar manejadores generales (canal_id=None)
            if None in self.event_handlers['on_message']:
                for codigo in self.event_handlers['on_message'][None]:
                    ctx = await self.get_context(message)
                    await self.ejecutar_codigo(ctx, codigo, canal_id=message.channel)

        await self.process_commands(message)

    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.user.id:
            return

        canal_id = payload.channel_id
        if 'on_raw_reaction_add' in self.event_handlers:
            # Ejecutar manejadores específicos del canal
            if canal_id in self.event_handlers['on_raw_reaction_add']:
                await self._handle_reaction_event(payload, canal_id, 'on_raw_reaction_add')
            # Ejecutar manejadores generales (canal_id=None)
            if None in self.event_handlers['on_raw_reaction_add']:
                await self._handle_reaction_event(payload, None, 'on_raw_reaction_add')

    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.user.id:
            return

        canal_id = payload.channel_id
        if 'on_raw_reaction_remove' in self.event_handlers:
            # Ejecutar manejadores específicos del canal
            if canal_id in self.event_handlers['on_raw_reaction_remove']:
                await self._handle_reaction_event(payload, canal_id, 'on_raw_reaction_remove')
            # Ejecutar manejadores generales (canal_id=None)
            if None in self.event_handlers['on_raw_reaction_remove']:
                await self._handle_reaction_event(payload, None, 'on_raw_reaction_remove')



    async def _handle_reaction_event(self, payload, canal_id, event_type):
        channel = self.get_channel(payload.channel_id)
        if channel is None:
            return

        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.NotFound:
            return

        ctx = await self.get_context(message)
        for codigo in self.event_handlers[event_type][canal_id]:
            try:
               await self.ejecutar_codigo(ctx, codigo, canal_id=channel)
            except Exception as e:
                await handle_error(ctx, e)

