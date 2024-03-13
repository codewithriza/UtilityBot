# ticket.py

from discord.ext import commands
import discord

id_category = 123456789012345678  # Replace with your actual category ID
id_channel_ticket_logs = 123456789012345678  # Replace with your actual ticket logs channel ID
id_staff_role = 123456789012345678  # Replace with your actual staff role ID
embed_color = discord.Color.blurple()  # Change color as needed


class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx):
        category = discord.utils.get(ctx.guild.categories, id=id_category)
        if not category:
            try:
                category = await ctx.guild.create_category("Tickets", overwrites=None, reason="Ticket system setup")
            except discord.Forbidden:
                await ctx.send("I don't have permission to create a category. Please configure the bot properly.")
                return

        ticket_logs_channel = ctx.guild.get_channel(id_channel_ticket_logs)
        if not ticket_logs_channel:
            try:
                ticket_logs_channel = await ctx.guild.create_text_channel("ticket-logs", category=category, overwrites=None, reason="Ticket system setup")
            except discord.Forbidden:
                await ctx.send("I don't have permission to create a text channel for ticket logs. Please configure the bot properly.")
                return

        staff_role = discord.utils.get(ctx.guild.roles, id=id_staff_role)
        if not staff_role:
            try:
                staff_role = await ctx.guild.create_role(name="Staff", reason="Ticket system setup")
            except discord.Forbidden:
                await ctx.send("I don't have permission to create a role for staff. Please configure the bot properly.")
                return

        for channel in category.channels:
            await channel.set_permissions(staff_role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True)

        read_me_channel_id = 1215370063687712808  # ID of the "read me" channel
        read_me_channel = self.bot.get_channel(read_me_channel_id)
        file_path = 'img.png'
        embed = discord.Embed(
            title='Tickets',
            description=f'Welcome to {ctx.guild.name}! If you face any issues, click on the "Create ticket" button for support. See you around!',
            color=embed_color
        )
        embed.set_image(url=f'attachment://{file_path}')
        message = await read_me_channel.send(embed=embed, file=discord.File(file_path, filename='img.png'), view=TicketView())


def setup(bot):
    bot.add_cog(Ticket(bot))


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketButton())

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)


class TicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.green,
            label='Create a ticket',
            emoji='🔧'
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=id_category)
        channel = await guild.create_text_channel(name=f'ticket-{interaction.user}', category=category)

        await channel.set_permissions(guild.default_role, send_messages=False, read_messages=False)
        await channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        staff_role = guild.get_role(id_staff_role)
        await channel.set_permissions(staff_role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True, manage_messages=True)

        embed = discord.Embed(title=f'Ticket - Hi {interaction.user.name}!', description=f'In this ticket we have an answer to your 🔧.\n\nIf you can\'t get someone to help you, press the button `🔔 Call staff`.', color=embed_color)
        embed.set_thumbnail(url=interaction.user.avatar.url)
        await channel.send(embed=embed, view=TicketActionsView())


class TicketActionsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketCallStaffButton())


class TicketCallStaffButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.red,
            label='Call staff',
            emoji='🔔'
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # Your code for calling staff here

