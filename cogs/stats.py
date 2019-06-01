import matplotlib.pyplot as plt
from matplotlib.colors import ColorConverter as CC
import discord
from discord.ext import commands
import asyncio
import json
from io import BytesIO

class Stat(commands.Cog):
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

            for size, colour in [
                                 (data["online"], CC.to_rgba("#43b581")),
                                 (data["idle"], CC.to_rgba("#faa61a")),
                                 (data["dnd"], CC.to_rgba("#f04747")),
                                 (data["offline"], CC.to_rgba("#747f8d"))]:
                if size:
                    sizes.append(size)
                    labels.append("{:2.1f}%".format((size/total)*100))
                    colors.append(colour)
            
            plt.clf()
            fig, ax1 = plt.subplots()
            wedges, _ = ax1.pie(sizes, labels=labels, shadow = True, colors = colors)

            im = plt.imread(BytesIO(await member.avatar_url_as(format = "png", static_format = "png", size = 1024).read()))
            plt.legend(wedges, labels, loc = "upper right")

            ax2 = fig.add_axes([0.346,0.35,0.32,0.32])
            ax2.imshow(im)
            ax2.axis('off')
            center_mask = plt.Circle((0,0),0.70,fc='white')
            ax1.add_artist(center_mask)
            ax1.axis('equal')

            output_buffer = BytesIO()
            plt.savefig(output_buffer)
            output_buffer.seek(0)
            plt.clf()

            await ctx.send(file = discord.File(output_buffer, "Pie.png"))

def setup(bot):
    bot.add_cog(Stat(bot))
    print("stats loaded")
