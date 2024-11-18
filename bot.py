import os, re
import discord
import asyncio
from dotenv import load_dotenv
from sc_login import request_login
from club_bot import ClubBot
from views import LoginButton

load_dotenv()  
scid_token = os.getenv('SCIDTOKEN')
bot_token = os.getenv('BOTTOKEN')
# TODO: Remove hardcoded value
channel = 1301319087896658042 
clubs = []

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    # TODO: Remove hardcoded value
    print("Bot ready")
    # clubs = [ClubBot(scid_token, channel)]
    clubs: list[ClubBot] = []
    # for club in clubs:
        # await club.login(bot)

    # while True:
    #     for club in clubs: 
    #         await club.process()
    #         await asyncio.sleep(1)


# @bot.command(
#     name="add-club-bridge",
#     description="Adds a club bridge to the current channel",
# )
# async def club_bridge(ctx: discord.ApplicationContext,
#                       email: discord.Option(description="Enter the email of the club bot account", type=str)): # type: ignore
#     print(f"recieved {email}")
#     await ctx.respond("hello")

@bot.slash_command(name="add-club-bridge", description="Adds a club bridge to the current channel") 
async def add_club_bridge(ctx: discord.ApplicationContext, 
                          email: discord.Option(description="Enter the email of the club bot account", type=str)): # type: ignore 
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" , email):
        await ctx.respond(f"{email} is not a valid email adress", ephemeral=True)
        return
    placeholder = await ctx.respond("Loading...", ephemeral=True)
    response = await request_login(email)
    print(f"{response.status}: {await response.text()}")
    desc = f"You should recieve an email shortly at `{email}`, press the button below to enter the pin \n### WARNING\n-# This could result in the account getting banned(very rare), and gives the bot full control of the account. \n-# Make sure to use a disposable account. The bot is not responsible for any loss of accounts"
    await placeholder.edit_original_response(content="", embed=discord.Embed(description=desc), view=LoginButton(email, clubs, ctx.channel_id))

bot.run(bot_token)
