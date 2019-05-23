import matplotlib.pyplot as plt
from matplotlib.colors import ColorConverter as CC
import discord
from discord.ext import commands
import asyncio
import json
from io import BytesIO

class stat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx, member: discord.Member = None):
        """makes a pie chart on the users presense"""
        with open("j.json", "r") as f:
            if not member: member = ctx.author
            data = json.load(f)
            data = data[str(member.id)]
            total = data["online"] + data["offline"] + data["idle"] + data["dnd"]
            labels = []
            colors = []
            sizes = []

            for size, colour in [(data["online"], CC.to_rgba("#43b581")), (data["idle"], CC.to_rgba("#faa61a")),(data["dnd"], CC.to_rgba("#f04747")),(data["offline"], CC.to_rgba("#747f8d"))]:
                if size: sizes.append(size); labels.append("{:2.1f}%".format((size/total)*100)); colors.append(colour)

            plt.clf()
            _, ax1 = plt.subplots()
            wedges, _, _ = ax1.pie(sizes, colors=colors, autopct='%1.1f%%', shadow=True, pctdistance = 0.85)
            #buffer = BytesIO()
            #await member.avatar_url_as(format = "png").save(buffer,seek_begin = True)
            #buffer.seek(0)
            #centre_circle = plt.imread(buffer.read(), "png")
            #fig = plt.gcf()
            #fig.gca().add_artist(centre_circle)

            my_circle=plt.Circle( (0,0), 0.7, color='white', linewidth=10)
            p=plt.gcf()
            p.gca().add_artist(my_circle)
            plt.legend(wedges, labels, loc = "best")
            ax1.axis('equal')  
            plt.tight_layout()
            output_buffer = BytesIO()
            plt.savefig(output_buffer)
            output_buffer.seek(0)
            await ctx.send(file = discord.File(output_buffer, "Pie.png"))

def setup(bot):
    bot.add_cog(stat(bot))
    print("stats loaded")
