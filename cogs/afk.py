import discord
from discord.ext import commands
import asyncio


class afk:
    def __init__(self, bot):
        self.bot = bot
        self.db = {}

    def is_afk(self):
        async def predicate(ctx):
            if not self.db[str(ctx.message.channel.server.id)]:
                self.db[str(ctx.message.channel.server.id)] = {}
            if str(ctx.author.id) in self.db[str(ctx.message.channel.server.id)]:
                return True
            else:
                return False
        return commands.check(predicate)

    @commands.command()
    @commands.check(is_afk)
    async def afk(self, ctx, *, reason):
        await ctx.send(f"{ctx.author.mention} is now AFK, reason is `{reason}`")
        self.db[str(ctx.message.channel.server.id)][str(ctx.author.id)] = reason
        await ctx.author.edit(nick = f"[AFK] - {ctx.author.display_name}")

    @afk.error
    async def on_afk_error(self, ctx, error: Exception):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.mention} is no longer AFK")
            del self.db[str(ctx.message.channel.server.id)][str(ctx.author.id)]
            split = ctx.author.display_name.split(" ")
            username = split[:2]
            ctx.author.edit(nick = " ".join(username))
        else:
            print(error)


def setup(bot):
    bot.add_cog(afk(bot))