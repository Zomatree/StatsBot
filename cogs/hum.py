import discord
import asyncio
from discord.ext import commands
import json

class member:
    def __init__(self, memberobject : discord.Member):
        self.member = memberobject
        self.score = 0
        self.hand = []

class game:
    def __init__(self, *players):
        self.players = players
        self.cards = {"white": [], "black": []}


class hum:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = asyncio.run(self.load())

    def load(self):
        return json.load(open("cogs.data.json", "r"))

    @commands.group(invoke_without_command = True)
    async def cah(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help()

    @cah.command()
    async def start(self, ctx):
        embed = discord.Embed(title = "say `join` to join the game of Cards against humanitys")
        await ctx.send(embed = embed)
        players = {}
        players[(ctx.author.id)] = member(ctx.author)
        async def a():
            while True:
                message = await self.bot.wait_for("message", check = lambda message: message.channel == ctx.channel and message.content.lower() == "join", timeout = 30)
                players[(message.author.id)] = member(message.author)
                await ctx.send(f"{message.author.mention} has joined!")
        async def b():
            await asyncio.sleep(30)

        await asyncio.wait([a, b], return_when=asyncio.FIRST_COMPLETED)
        await ctx.send()
        if len(players) < 3: 
            return await ctx.send("Not enough players")
        
        # -----game--------
        
        




        

