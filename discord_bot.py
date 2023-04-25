import os
import discord
from discord.ext import commands, tasks
import amazon_sku_tracker

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
        response = f"Added new storefront: {storefront_url}"
    else:
        response = f"Storefront {storefront_url} is already being tracked."
    await ctx.send(response)

@tasks.loop(seconds=60)  # Adjust the interval to your preference
async def sku_tracking_job():
    # Replace CHANNEL_ID with the ID of the Discord channel you want to send notifications to
    channel = bot.get_channel(509234451033620482)
    if channel:
        await amazon_sku_tracker.job(channel)
    else:
        print("Failed to find the Discord channel.")

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

sku_tracking_job.start()
