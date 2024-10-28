import os
from discord.ext import commands


class SeriesProgress(commands.Cog):
        def __init__(self, bot, db):
            self.bot = bot
            self.db = db


        def format_series_name(self, name):
            accents = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}
            for key, value in accents.items():
                name = name.replace(key, value)
            return name


        @commands.command(name="add-serie", help="Añade una nueva serie a la lista.")
        async def add_series(self, ctx, series_name=None, season=None, episode=None):
            if series_name and season and episode:
                with open(self.db, 'a', encoding="utf-8") as series_list:
                    line = f"· {self.format_series_name(series_name.upper())} | T. {season} - Ep. {episode}\n"
                    series_list.write(line)

                await ctx.send("¡La serie se ha añadido correctamente!")
            else:
                await ctx.send("El formato del comando es: '!add-serie <<nombre_serie>> <<número_temporada>> <<número_episodio>>'.")
                 

        @commands.command(name="delete-serie", help="Elimina una serie existente en la lista.")
        async def delete_series(self, ctx, series_name=None):
            if series_name:
                deleted = False
                series_name = self.format_series_name(series_name.upper())
                temp_file = self.db.replace("progress", "progress_temp")
                with open(self.db, 'r', encoding="utf-8") as series_list:
                    with open(temp_file, 'w', encoding="utf-8") as temp_series_list:
                        for line in series_list:
                            if series_name not in line:
                                temp_series_list.write(line)
                            else:
                                deleted = True

                if deleted:
                    os.remove(self.db)
                    os.rename(temp_file, self.db)
                    await ctx.send("¡La serie se ha eliminado correctamente!")
                else:
                    os.remove(temp_file)
                    await ctx.send("No hay una serie con ese nombre en el listado. Comprueba que has escrito el nombre exactamente igual que el que hay en el listado: '!show-series-list'.")
                
            else:
                await ctx.send("El formato del comando es: '!delete-serie <<nombre_serie>>'")


        @commands.command(name="update-serie", help="Actualizar la temporada y el capítulo de una serie.")
        async def update_series(self, ctx, series_name=None, season=None, episode=None):
            if series_name:
                updated = False
                series_name = self.format_series_name(series_name.upper())
                temp_file = self.db.replace("progress", "progress_temp")
                with open(self.db, 'r', encoding="utf-8") as series_list:
                    with open(temp_file, 'w', encoding="utf-8") as temp_series_list:
                        for line in series_list:
                            if series_name not in line:
                                temp_series_list.write(line)
                            else:
                                new_line = f"· {series_name} | T. {season} - Ep. {episode}\n"
                                temp_series_list.write(new_line)
                                updated = True

                if updated:
                    os.remove(self.db)
                    os.rename(temp_file, self.db)
                    await ctx.send("¡La serie se ha actualizado correctamente!")
                else:
                    os.remove(temp_file)
                    await ctx.send("No hay una serie con ese nombre en el listado. Comprueba que has escrito el nombre exactamente igual que el que hay en el listado: '!show-series-list'.")
                
            else:
                await ctx.send("El formato del comando es: '!update-serie <<nombre_serie>>'")


        @commands.command(name="show-series-list", help="Mostrar el listado de todas las series registradas.")
        async def show_all_series(self, ctx):
            if os.path.isfile(self.db):
                with open(self.db, 'r', encoding="utf-8") as series_list:
                    first_line = series_list.readline()
                    if not first_line or first_line == '\n' or first_line == "":
                        await ctx.send("No hay ninguna serie en la lista.")
                    else:
                        series_list.seek(0)
                        await ctx.send("".join(series_list.readlines()))
            else:
                await ctx.send("No hay creada una lista en la que guardar las series. Contacta con el creador del bot.")


        @commands.command(name="show-serie", help="Mostrar la temporada y el capítulo registrados de una serie.")
        async def show_one_series(self, ctx, series_name=None):
            if series_name:
                if os.path.isfile(self.db):
                    series_name = self.format_series_name(series_name.upper())
                    print(series_name)
                    with open(self.db, 'r', encoding="utf-8") as series_list:
                        first_line = series_list.readline()
                        if not first_line or first_line == '\n' or first_line == "":
                            await ctx.send("No hay ninguna serie en la lista.")
                        else:
                            series_list.seek(0)
                            for line in series_list:
                                if series_name in line:
                                    await ctx.send(line)
                                    return
                            
                            await ctx.send("No hay una serie con ese nombre en el listado. Comprueba que has escrito el nombre exactamente igual que el que hay en el listado: '!show-series-list'.")
        
                else:
                    await ctx.send("No hay creada una lista en el que guardar las series. Contacta con el creador del bot.")
            
            else:
                await ctx.send("El formato del comando es: '!show-serie <<nombre_serie>>'")
