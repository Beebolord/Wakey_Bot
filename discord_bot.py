import discord
import asyncio
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
HOUR = int(os.getenv("HOUR"))
MINUTE = int(os.getenv("MINUTE"))
DELAY = int(os.getenv("DELAY"))

# Discord client setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()
job_added = False

EXCLUDED_USER_IDS = {
    359363342168752139,
    1259906519621959825,
    317849297381097473
}

@client.event
async def on_ready():
    global job_added
    logging.info(f"🤖 Bot connected as {client.user}")

    if not job_added:
        scheduler.add_job(send_daily_checkin, 'cron', hour=HOUR, minute=MINUTE)
        scheduler.start()
        job_added = True

async def send_daily_checkin():
    guild = client.get_guild(GUILD_ID)
    if guild is None:
        logging.warning(f"Could not find guild with ID {GUILD_ID}")
        return

    channel = guild.get_channel(CHANNEL_ID)
    if channel is None:
        logging.warning(f"Could not find channel with ID {CHANNEL_ID} in guild {guild.name}")
        return

    # Send the daily check-in message
    msg = await channel.send("@everyone 👋 Daily check-in! Please react with ✅")
    await msg.add_reaction("✅")
    logging.info(f"Sent daily check-in message (ID: {msg.id}) in #{channel.name}")

    await asyncio.sleep(DELAY)

    # Fetch the message again to get updated reactions
    msg = await channel.fetch_message(msg.id)

    reacted_users = set()
    for reaction in msg.reactions:
        if str(reaction.emoji) == "✅":
            async for user in reaction.users():
                if not user.bot:
                    reacted_users.add(user.id)

    non_reactors = []
    for member in channel.members:
        if (
            not member.bot
            and member.id not in reacted_users
            and member.id not in EXCLUDED_USER_IDS
        ):
            non_reactors.append(member)

    if non_reactors:
        names = []
        for member in non_reactors:
            names.append(member.display_name)
            try:
                await member.send("⏰ You missed the daily check-in!")
            except discord.Forbidden:
                logging.warning(f"Cannot DM {member.display_name}")

        names_str = ", ".join(names)
        await channel.send(f"⚠️ The following members did not react to the daily check-in: @{names_str}")
    else:
        await channel.send("🎉 Everyone reacted to the check-in!")

# Run the bot
if __name__ == '__main__':
    client.run(TOKEN)
