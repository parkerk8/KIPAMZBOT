import discord
import os
from discord.ext import commands
import amazon_sku_tracker

DISCORD_BOT_TOKEN =   my_secret = os.environ['BOT_TOKEN']
# Replace with your bot token


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='add_storefront')
async def add_storefront(ctx, storefront_url: str):
    if storefront_url not in amazon_sku_tracker.storefront_links:
        amazon_sku_tracker.storefront_links.append(storefront_url)
        response = f"Added new storefront: {storefront_url}"
    else:
        response = f"Storefront {storefront_url} is already being tracked."
    await ctx.send(response)
    else:
        response = f"Storefront {storefront_url} is already being tracked."
    await ctx.send(response)

@bot.event
async def on_ready():
    print("Bot is ready.")

print("Bot is starting...")
bot.run(DISCORD_BOT_TOKEN)
import os
import discord
from discord.ext import commands, tasks
import amazon_sku_tracker

DISCORD_BOT_TOKEN = "MTA3NjIxMTIwNjUzMDAyNzY5MA.GW5FGG.ie82903vt1jjTnQZegQBlQGEbiZstZT9bzs0XU"  # Get your bot token from an environment variable

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='add_storefront')
async def add_storefront(ctx, storefront_url: str):
    if storefront_url not in amazon_sku_tracker.storefront_links:
        amazon_sku_tracker.storefront_links.append(storefront_url)
        response = f"Added new storefront: {storefront_url}"
    else:
        response = f"Storefront {storefront_url} is already being tracked."
    await ctx.send(response)

@tasks.loop(seconds=60)  # Adjust the interval to your preference
async def sku_tracking_job():
    # Replace CHANNEL_ID with the ID of the Discord channel you want to send notifications to
    channel = bot.get_channel(509234451033620484)
    if channel:
        await amazon_sku_tracker.job(channel)
    else:
        print("Failed to find the Discord channel.")

@bot.event
async def on_ready():
    print("Bot is ready.")
    sku_tracking_job.start()

print("Bot is starting...")
bot.run(DISCORD_BOT_TOKEN)
