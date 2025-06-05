import discord
import asyncio
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()  # Load .env file locally; on Render use environment variables
TOKEN="MTM3OTkyNTAwMjU2NDAxNDIxMQ.Gbh-Uv.-Ov1ufrx2GDGXOuj3e2r-Pr59py6uZoBvwKXBU"
GUILD_ID=938189546288447518
CHANNEL_ID=938189546288447521
#TOKEN = os.getenv("BOT_TOKEN")
#GUILD_ID = int(os.getenv("GUILD_ID"))
#CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler()
job_added = False

@client.event
async def on_ready():
    global job_added
    print(f"🤖 Bot connected as {client.user}")
    if not job_added:
        scheduler.add_job(send_daily_checkin, 'cron', hour=22, minute=12)  # Adjust as needed
        scheduler.start()
        job_added = True

send_lock = asyncio.Lock()

async def send_daily_checkin():
    async with send_lock:
        guild = client.get_guild(GUILD_ID)
        if guild is None:
            print(f"Could not find guild with ID {GUILD_ID}")
            return

        channel = guild.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Could not find channel with ID {CHANNEL_ID} in guild {guild.name}")
            return

        msg = await channel.send("👋 Daily check-in! Please react with ✅")
        await msg.add_reaction("✅")
        print(f"Sent daily check-in message (ID: {msg.id}) in #{channel.name}")

        await asyncio.sleep(8)  # Wait time before checking reactions

        msg = await channel.fetch_message(msg.id)

        reacted_users = set()
        for reaction in msg.reactions:
            if str(reaction.emoji) == "✅":
                async for user in reaction.users():
                    if not user.bot:
                        reacted_users.add(user.id)

        print(f"Users who reacted with ✅: {len(reacted_users)}")

        non_reactors = []
        async for member in guild.fetch_members(limit=None):
            if not member.bot and member.id not in reacted_users:
                non_reactors.append(member)

        if non_reactors:
            print("Users who did NOT react:")
            for member in non_reactors:
                print(f"- {member.display_name} ({member.id})")
                try:
                    await member.send("⏰ You missed the daily check-in!")
                except discord.Forbidden:
                    print(f"Cannot DM {member.display_name}")
        else:
            print("Everyone reacted! No DMs sent.")


if __name__ == "__main__":
    # This makes it runnable locally and on Render as a background worker
    client.run(TOKEN)
