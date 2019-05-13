import asyncio
import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix=">>>")

command_cog = [
    "loop",
    "stats"
]

async def is_owner(user): return user.id == 285130711348805632

bot.is_owner = is_owner

@bot.event
async def on_ready():
    print("ready")

if __name__ == "__main__":
    bot.load_extension("jishaku")
    for cog in command_cog:
        try:
            bot.load_extension("cogs." + cog)
        except Exception as e:
            exc = f"{type(e).__name__}: {e}"
            print(f"failed to load extension {cog}\n{exc}")


bot.run("MzgwNDIzNTAyODEwOTcyMTYy.XMnRqQ.fuRPffxE8fJb9RmARiR86OXcRgA")