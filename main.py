import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # Load Cogs
    bot.load_extension('cogs.ticket')


# Your token here
bot.run('BOT_TOKEN')
