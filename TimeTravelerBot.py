import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from rag import query

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
# Default value 0 for all channels allowed
ALLOWED_CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="ms", aliases=["message", "chat"])
async def ms_command(ctx, *, question: str):
    if ALLOWED_CHANNEL_ID != 0 and ctx.channel.id != ALLOWED_CHANNEL_ID:
        return

    async with ctx.typing():
        loop = asyncio.get_event_loop()
        answer = await loop.run_in_executor(None, query, question)

    # Discord has a limit of 2000 chars
    if len(answer) > 1900:
        answer = answer[:1900] + "..."

    await ctx.reply(f"**Time traveler:** \n\n{answer}")


if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN not in .env file!")
        exit(1)
    bot.run(TOKEN)
