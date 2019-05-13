import json
import asyncio
import discord
from discord.ext import commands
from discord.ext import tasks

class userloop(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bgloop.start()

    @tasks.loop(minutes = 1)
    async def bgloop(self):
        with open("j.json", "r") as f:
            fe = json.load(f)
            for user in set(self.bot.get_all_members()):
                if str(user.id) not in fe:
                    fe[str(user.id)] = {
                        "online": 0,
                        "offline": 0,
                        "idle": 0,
                        "dnd": 0}
                else:
                    if user.status is discord.Status.online:
                        fe[str(user.id)]["online"] += 1
                    elif user.status is discord.Status.offline:
                        fe[str(user.id)]["offline"] += 1
                    elif user.status is discord.Status.idle:
                        fe[str(user.id)]["idle"] += 1
                    elif user.status is discord.Status.dnd:
                        fe[str(user.id)]["dnd"] += 1
        with open("j.json", "w") as f:
            fe = json.dumps(fe)
            f.write(fe)

def setup(bot):
    bot.add_cog(userloop(bot))
    print("loop file loaded")
