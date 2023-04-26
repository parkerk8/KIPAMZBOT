import os
import discord
from discord.ext import commands
import amazon_sku_tracker

from common import send_discord_notification

# Retrieve the bot token from an environment variable named "DISCORD_BOT_TOKEN"
secret_key = os.environ["DISCORD_BOT_TOKEN"]

# Configure Discord client to use only the necessary intents to conserve resources
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True

# Initialize the bot object with the specified command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Define the command to add a storefront URL to the list of websites being tracked by the Amazon SKU tracker
@bot.command(name='add_storefront')
async def add_storefront(ctx, storefront_url: str):
    print(f"Processing !add_storefront command for {storefront_url}")
    if storefront_url not in amazon_sku_tracker.storefront_links:
        amazon_sku_tracker.storefront_links.append(storefront_url)
        # Check for new SKUs and save them as the initial SKUs
        initial_skus = amazon_sku_tracker.check_for_new_skus(storefront_url)
        amazon_sku_tracker.save_new_skus_as_old(storefront_url, initial_skus)
        response = f"Added new storefront: {storefront_url}"
    else:
        response = f"Storefront {storefront_url} is already being tracked."
    await ctx.send(response)

@bot.command(name='check_skus')
async def check_skus(ctx):
    print(f"Processing !check_skus command")
    found_new_skus = False
    for url in amazon_sku_tracker.storefront_links:
        new_skus = amazon_sku_tracker.check_for_new_skus(url)
        if new_skus:
            print(f"Found new SKUs for URL {url}: {', '.join(new_skus)}")
            await amazon_sku_tracker.send_discord_notification(ctx.channel, new_skus)
            found_new_skus = True
    if not found_new_skus:
        print("No new SKUs found for any tracked storefronts.")
        await ctx.channel.send("No new SKUs found for any tracked storefronts.")

# Define an event handler to be called once the bot is ready
@bot.event
async def on_ready():
    print("Bot is ready.")

# Define an event handler to log and display command errors to the channel where the command was issued
@bot.event
async def on_command_error(ctx, error):
    print(f"Error occurred while processing command: {error}")
    await ctx.send(f"An error occurred: {error}")

# Begin the bot's execution
print("Bot is starting...")
bot.run(secret_key)
