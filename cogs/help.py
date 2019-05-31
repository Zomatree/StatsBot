import discord
from discord.ext import commands
import asyncio

class Embedinator:
    def __init__(self, bot, member=None, **kwargs):
        self.bot = bot
        self.member = member
        self.max_fields = kwargs.get("max_fields", 25)
        self.base_embed = discord.Embed(**kwargs)
        self.embed_list = [self.base_embed.copy()]
        self.current = 0
        self.buttons = ["◀", "▶", "⏹"]

    @property
    def last_page(self):
        return self.embed_list[-1]

    def add_page(self):
        self.embed_list.append(self.base_embed.copy())
        if len(self.embed_list) > 1:
            self.set_footer()

    def add_field(self, *, name, value, inline=True):
        if len(self.last_page.fields) >= self.max_fields:
            self.add_page()
        self.last_page.add_field(name=name, value=value, inline=inline)

    async def send(self, destination):
        self.message = await destination.send(embed=self.embed_list[0])
        if len(self.embed_list) > 1:
            await self.handle()

    async def edit(self):
        await self.message.edit(embed=self.embed_list[self.current])

    async def handle(self):
        if len(self.embed_list) > 1:
            for button in self.buttons:
                await self.message.add_reaction(button)
        else:
            await self.message.add_reaction(self.buttons[-1])

        async for reaction, user in self.wait():
            await self.handle_reaction(reaction, user)

        await self.cleanup()

    async def wait(self):
        while True:
            done, pending = await asyncio.wait(
                [
                    self.bot.wait_for("reaction_add", check=self.check_reaction),
                    self.bot.wait_for("reaction_remove", check=self.check_reaction),
                    self.bot.wait_for("message_delete", check=self.check_delete),
                ],
                timeout=60.0,
                return_when=asyncio.FIRST_COMPLETED,
            )

            for future in pending:
                future.cancel()
            if done:
                result = done.pop().result()
                if isinstance(result, discord.Message):
                    return
                else:
                    yield result
            else:
                return

    def check_reaction(self, reaction, user):
        return (
            reaction.message.id == self.message.id
            and str(reaction.emoji) in self.buttons
            and (self.member is None or user.id == self.member.id)
        )

    def check_delete(self, message):
        return message.id == self.message.id

    async def handle_reaction(self, reaction, user):
        if str(reaction.emoji) == "⏹":
            await self.cleanup()
        if str(reaction.emoji) == "▶":
            self.current += 1
            if self.current == len(self.embed_list):
                self.current = 0
            await self.edit()
        if str(reaction.emoji) == "◀":
            self.current -= 1
            if self.current == -1:
                self.current = len(self.embed_list) - 1
            await self.edit()

    async def cleanup(self):
        try:
            await self.message.delete()
        except discord.NotFound:
            pass

    def set_footer(self):
        i = 1
        for embed in self.embed_list:
            embed.set_footer(text=f"{i}/{len(self.embed_list)}")
            i += 1

    def set_author(self, **kwargs):
        self.base_embed.set_author(**kwargs)
        for embed in self.embed_list:
            embed.set_author(**kwargs)

class SoraHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={"hidden": True})
        self.colour = 0xFFFF00

    async def send_command_help(self, command):
        embed = self.create_embed()
        embed.title = self.get_command_name(command)
        embed.description = command.short_doc or "No description"
        embed.set_footer(text=f"Category: {command.cog_name}")
        destination = self.get_destination()
        await destination.send(embed=embed)

    # todo: fix layout whenever I actually add some group commands
    async def send_group_help(self, group):
        embedinator = self.create_embedinator(
            title=self.get_command_name(group), description=group.short_doc or "No description", max_fields=4
        )

        filtered = await self.filter_commands(group.commands)
        if filtered:
            for command in filtered:
                self.add_command_field(embedinator, command)

        await self.send_embedinator(embedinator)

    async def send_cog_help(self, cog):
        embedinator = self.create_embedinator(
            title=f"Category: {cog.qualified_name}", description=cog.description or "No description", max_fields=5
        )

        filtered = await self.filter_commands(cog.get_commands())
        if filtered:
            for command in filtered:
                self.add_command_field(embedinator, command)

        await self.send_embedinator(embedinator)

    async def send_bot_help(self, mapping):
        embedinator = self.create_embedinator(
            description=self.get_opening_note())

        for cog, cog_commands in mapping.items():
            filtered = await self.filter_commands(cog_commands)
            if filtered:
                if len(embedinator.last_page.fields) != 0:
                    embedinator.add_page()

                embedinator.add_field(
                    name=f"Category: {cog.qualified_name}", value=cog.description or "No description", inline=False
                )

                for command in filtered:
                    self.add_command_field(embedinator, command)

        await self.send_embedinator(embedinator)

    def get_destination(self):
        return self.context

    def command_not_found(self, string):
        return f'Command or category "{string}" not found.'

    def subcommand_not_found(self, command, string):
        return f'Subcommand "{string}" not found.'

    def get_opening_note(self):
        command_name = self.context.invoked_with
        return "Use `{0}{1} <command/category>` for more info.".format(self.clean_prefix, command_name)

    def get_command_name(self, command):
        name = f"**{command.name}**"
        if any(command.aliases):
            name = f'{name}, {"".join([f"**{c}**, " for c in command.aliases])}'

        name = f"{name} {command.signature}"
        return name

    def create_embed(self):
        embed = discord.Embed(colour=self.colour)
        embed.set_author(name=self.context.author.display_name,
                         icon_url=self.context.author.avatar_url)

        return embed

    def create_embedinator(self, **kwargs):
        embedinator = Embedinator(
            self.context.bot, self.context.author, **kwargs, colour=self.colour)

        embedinator.set_author(
            name=self.context.bot.user.name, icon_url=self.context.bot.user.avatar_url)

        return embedinator

    def add_command_field(self, embedinator, command):
        name = self.get_command_name(command)
        embedinator.add_field(name=name, value=command.short_doc, inline=False)

    async def send_embedinator(self, embedinator):
        await embedinator.send(self.get_destination())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = SoraHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))