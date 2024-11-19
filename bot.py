import os, re
import discord
from discord.ext import tasks
from club_bot import ClubBot
from views import LoginButton
from dotenv import load_dotenv
from sc_login import request_login
from loading import loading

load_dotenv()  
scid_token = os.getenv('SCIDTOKEN')
bot_token = os.getenv('BOTTOKEN')

clubs: list[ClubBot] = []
index = 0

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print("Bot ready")
    saved_clubs = []
    for club in saved_clubs:
        await club.login(bot)
        clubs.append(club)

    if not check_club_messages.is_running:
        check_club_messages.start()

# @bot.event()
# async def on_message(message):
#     # TODO: Execute discord message processing
#     """Some code"""
#     return

@bot.slash_command(name="add-club-bridge", description="Adds a club bridge to the current channel") 
async def add_club_bridge(ctx: discord.ApplicationContext, 
                          email: discord.Option(description="Enter the email of the club bot account", type=str)): # type: ignore 
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" , email):
        await ctx.respond(f"{email} is not a valid email adress", ephemeral=True)
        return
    interaction_response = await ctx.respond(embed=loading(), ephemeral=True)
    response = await request_login(email)
    print(f"{response.status_code}: {response.text}")
    desc = f"You should recieve an email shortly at `{email}`, press the button below to enter the pin\n### WARNING\n-# This could result in the account getting banned(very rare), and gives the bot full control of the account. \n-# Make sure to use a disposable account. The bot is not responsible for any loss of accounts"
    await interaction_response.edit_original_response(content="", embed=discord.Embed(description=desc), view=LoginButton(email, clubs, ctx.channel_id, interaction_response))


@tasks.loop(seconds=2.0)
async def check_club_messages():
    global index
    await bot.wait_until_ready()
    print(clubs)
    if index>len(clubs):
        index=0

    if clubs:    
        club = clubs[index]
        await club.process()
        print(f"Processed {club.name}")

bot.run(bot_token)
