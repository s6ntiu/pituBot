import discord
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# API Key desde .env
api_key = os.getenv("OPENROUTER_API_KEY")

# cliente apuntando a OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

chat_sessions = {}

async def setup(bot):
    @bot.command()
    async def startchat(ctx):
        chat_sessions[ctx.channel.id] = [{"role": "system", "content": "Sos un asistente útil y experto"}]
        await ctx.send(" Sesion de Chat iniciada en este canal.")

    @bot.command()
    async def endchat(ctx):
        if ctx.channel.id in chat_sessions:
            del chat_sessions[ctx.channel.id]
            await ctx.send(" Sesion finalizada.")
        else:
            await ctx.send(" No hay sesion activa.")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        await bot.process_commands(message)

        if message.channel.id in chat_sessions:
            history = chat_sessions[message.channel.id]
            history.append({"role": "user", "content": message.content})

            try:
                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",
                    messages=history,
                    temperature=0.8,
                    max_tokens=1000,
                )
                content = response.choices[0].message.content
                history.append({"role": "assistant", "content": content})
                if len(content) > 2000:
                    # Crear archivo de texto temporal
                    with open("txt_response.txt", "w", encoding="utf-8") as f:
                        f.write(content)

                    # Enviar el archivo como adjunto
                    await message.channel.send("La respuesta excede los 2000 caracteres, la mando como txt",
                                               file=discord.File("txt_response.txt"))
                else:
                    await message.channel.send(content)

            except Exception as e:
                await message.channel.send(f" Error: {e}")
