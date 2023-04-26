async def send_discord_notification(channel, new_skus):
    message = f"New SKUs found: {', '.join(new_skus)}"
    await channel.send(message)