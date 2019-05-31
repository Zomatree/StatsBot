import asyncio
import discord
from discord.ext import commands
import json

minidb = []

async def get_pre(bot, message):
    if message.id in minidb:
        return ""
    else:
        return  ">>>"

bot = commands.Bot(command_prefix=get_pre)

command_cog = [
    "loop",
    "stats",
    "help"
]

async def is_owner(user): return user.id == 285130711348805632

bot.is_owner = is_owner

@bot.event
async def on_ready():
    print("ready")

@bot.event
async def on_message(message):
    if message.content.endswith(bot.user.mention):
        minidb.append(message.id)
        message.content = " ".join(message.content.split(" ")[:-1])
    await bot.process_commands(message)


if __name__ == "__main__":
    bot.load_extension("jishaku")
    for cog in command_cog:
        try:
            bot.load_extension("cogs." + cog)
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            print(f"failed to load extension {cog}\n{exc}")


bot.run("MzgwNDIzNTAyODEwOTcyMTYy.XMnRqQ.fuRPffxE8fJb9RmARiR86OXcRgA")