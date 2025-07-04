import discord
import asyncio
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import time
import pytz

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)



load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
HOUR = int(os.getenv("HOUR"))
MINUTE=  int(os.getenv("MINUTE"))
DELAY=  int(os.getenv("DELAY"))
logging.info(f"TOKEN present: {'Yes' if TOKEN else 'No'}")
logging.info(f"GUILD_ID: {GUILD_ID}")
logging.info(f"CHANNEL_ID: {CHANNEL_ID}")
logging.info(f"HOUR: {HOUR}, MINUTE: {MINUTE}, DELAY: {DELAY}")


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

eastern = pytz.timezone("America/Toronto")
client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()
job_added = False

@client.event
async def on_ready():
    global job_added
    logging.info(f"🤖 Bot connected as {client.user}")
#done
    day = time.localtime().tm_wday
    hour = 0
    if day == 4:
        hour = 9
    else:
        hour = 10

    if not job_added:
        scheduler.add_job(send_daily_checkin, 'cron', hour=hour, minute=30, day_of_week='mon-fri')  # Adjust time
        scheduler.start()
        job_added = True


EXCLUDED_USER_IDS = {
    365602126790918145,
    189186215331758080,
    484116229871894528,
    359363342168752139,

}
send_lock = asyncio.Lock()

async def send_daily_checkin():
    async with (send_lock):
        guild = client.get_guild(GUILD_ID)
        if guild is None:
            print(f"Could not find guild with ID {GUILD_ID}")
            return

        channel = guild.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Could not find channel with ID {CHANNEL_ID} in guild {guild.name}")
            return

        # Send the daily check-in message
        msg = await channel.send("@everyone 👋 Daily check-in! Please react with ✅")
        await msg.add_reaction("✅")
        print(f"Sent daily check-in message (ID: {msg.id}) in #{channel.name}")

        # Wait 8 seconds (you had 8, not 3600)
        await asyncio.sleep(DELAY)

        # Fetch the message again to update reaction info
        msg = await channel.fetch_message(msg.id)

        reacted_users = set()
        for reaction in msg.reactions:
            if str(reaction.emoji) == "✅":
                async for user in reaction.users():
                    if not user.bot:
                        reacted_users.add(user.id)

        print(f"Users who reacted with ✅: {len(reacted_users)}")

        # Check members who have access to the channel and haven't reacted
        non_reactors = []
        for member in channel.members:
            if(
                not member.bot
                and member.id not in reacted_users and
                member.id not in EXCLUDED_USER_IDS
            ):
                non_reactors.append(member)


        if non_reactors:
            print("Users who did NOT react:")
            names = []
            for member in non_reactors:
                print(f"- {member.display_name} ({member.id})")
                names.append(member.display_name)
                try:
                    print("will send txt")
                except discord.Forbidden:
                    print(f"Cannot DM {member.display_name}")

            # Send a message in the channel listing who didn't react
            names_str = ", ".join(names)
            await channel.send(f"⚠️ The following members did not react to the daily check-in: @{names_str}")

        else:
            print("Everyone reacted! No DMs sent.")
            await channel.send("🎉 Everyone reacted to the daily check-in! Good job!")


if __name__ == '__main__':
    client.run(TOKEN)