import discord
import os
import random
import mysql.connector
from discord.ext import commands
import logging

logging.basicConfig(
    filename="discord.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("SQL_PASSWORD"),
    database="discordbot",
)

cursor = conn.cursor()

async def setup(bot):
    # boton drop
    class View(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=30)
        @discord.ui.button(label="", style=discord.ButtonStyle.secondary, emoji="🦉")
        async def editarembedyregistrar(self, interaction: discord.Interaction, button: discord.ui.Button):
            # obtengo id
            user_id = interaction.user.id
            # obtengo username
            usuario = interaction.user.name

            #si esta registrado
            cursor.execute("SELECT * FROM owners WHERE userid = %s", [user_id])
            resultado = cursor.fetchone()
            if resultado:
                logging.info(f"{user_id} ya registrado")
            else:
                cursor.execute("INSERT INTO OWNERS (name, userid) VALUES (%s, %s)",
                               (usuario, user_id))
                conn.commit()
                logging.info(f"Usuario {usuario} registrado")


            # agarro embed original
            embed = interaction.message.embeds[0]
            embedtitle = embed.title

            # busco si la carta ya tenía owner
            cursor.execute("SELECT owner FROM cartas WHERE name = %s", [embedtitle])
            ownerresult = cursor.fetchone()
            owneranterior = ownerresult[0] if ownerresult and ownerresult[0] else None # es tupla asi que tengo que usar el primer resultado


            message = "mensaje a mandar"
            # si el owner anterior es el mismo que reclama:
            if owneranterior.strip().lower()== usuario.strip().lower():
                message = f"You are already married to **{embedtitle}**"
                for child in self.children: #desactivo boton
                    child.disabled = True
                await interaction.message.edit(view=self) # mando mensaje ya casado
                await interaction.response.send_message(
                    f"{message}",
                )
                return
            else:
                # creo una copia del embed original y la cambio
                embed.color = discord.Color.red()
                embed.set_footer(text=f"Now belongs to {usuario}") # footer owned
                cursor.execute("UPDATE cartas SET owner = %s WHERE name = %s", # update nuevo owner
                               [usuario, embedtitle])
                conn.commit()

            if owneranterior: #si tiene owner pasado
                mensaje = f"**{usuario}** stole **{embedtitle}** from **{owneranterior}**"
            else: # si no tiene owner pasado
                mensaje = f"**{usuario}** has married **{embedtitle}**"


            # desactivar botones
            for child in self.children:
                child.disabled = True

            # actualizo el mensaje original
            await interaction.response.edit_message(embed=embed, view=self)
            # mando mensaje
            await interaction.channel.send(f"{mensaje}", suppress_embeds=True)


    # Dropear
    @bot.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def m(ctx):
        user_id = ctx.author.name  # id del q ejecuta el comando
        cursor.execute("SELECT MAX(id) FROM cartas") # cant personajes
        numeromaximo = cursor.fetchone()[0]
        numero = random.randint(1,numeromaximo)
        cursor.execute("SELECT name FROM cartas WHERE id = %s",
                       [numero]) # nombre de la q toco
        titulo = cursor.fetchone()[0]
        cursor.execute("SELECT series FROM cartas WHERE id = %s",
                       [numero]) # serie
        desc = cursor.fetchone()[0]
        cursor.execute("SELECT image FROM cartas WHERE id = %s",
                       [numero]) # imagen
        image = cursor.fetchone()[0]


        embed = discord.Embed(title=f"{titulo}",
                              description=f"{desc}",
                              color=discord.Color.blue()  
                            )
        embed.set_image(url=f"{image}")

        cursor.execute("SELECT owner FROM cartas WHERE owner IS NOT NULL AND name = %s",
                       [titulo])
        currowner = cursor.fetchone()
        if currowner is not None:
            embed.set_footer(text=f"Currently owned by {currowner[0]}")

        await ctx.send(embed=embed, view=View())

    #Error si intenta dropear antes del cooldown
    @m.error
    async def m_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            tiempo_restante = round(error.retry_after, 1)
            await ctx.send(f"Wait for your cooldown to end! {tiempo_restante} remaining!")

    # Agregar carta
    @bot.command()
    async def agregarcarta(ctx, nombre: str, imagen_url: str, serie: str):
        try:
            # Verificar si ya existe una carta con ese nombre
            cursor.execute("SELECT * FROM cartas WHERE name = %s", (nombre,))
            existe = cursor.fetchone()

            if existe:
                await ctx.send(f"There is already a Character with the name **`{nombre}`**.")
                return

            # Insertar si no existe
            cursor.execute(
                "INSERT INTO cartas (name, image, series) VALUES (%s, %s, %s)",
                (nombre, imagen_url, serie)
            )
            conn.commit()

            await ctx.send(f" Character **{nombre}** from **{serie}** added successfully!")
        except Exception as e:
            await ctx.send(f" Error adding the character `{e}`")



    # inspeccionar character
    @bot.command()
    async def im(ctx, *nombre: str): # * es de args, permite agarrar todo el mensaje como argumento
            nombre = " ".join(nombre) # unimos string que pasa como argumento
            # Verificar si existe una carta con ese nombre
            cursor.execute("SELECT * FROM cartas WHERE name = %s", (nombre,))
            existe = cursor.fetchone()

            if existe:
                cursor.execute("SELECT name FROM cartas WHERE name = %s",
                               [nombre]) # nombre
                titulo = cursor.fetchone()[0]
                cursor.execute("SELECT series FROM cartas WHERE name = %s",
                               [nombre]) # serie
                desc = cursor.fetchone()[0]
                cursor.execute("SELECT image FROM cartas WHERE name = %s",
                               [nombre]) # imagen
                image = cursor.fetchone()[0]
                cursor.execute("SELECT owner FROM cartas WHERE name = %s",
                               [nombre])
                charowner = cursor.fetchone()[0] # owner de la carta
                embed = discord.Embed(title=f"{titulo}",
                                      description=f"{desc}",
                                      color=discord.Color.purple()
                                      )
                embed.set_image(url=f"{image}")
                embed.set_footer(text=f"Currently owned by {charowner}")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Character **{nombre}** not found!")


