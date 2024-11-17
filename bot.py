import discord
import asyncio
import os
from dotenv import load_dotenv
from club_bot import ClubBot
from my_requests import sc_request


load_dotenv()  
scid_token = os.getenv('SCIDTOKEN')

webhook_url = "https://discord.com/api/webhooks/1307513820494696509/vnB0QyMhRah6ePYIhw7HAVQaz69NA0OOaSh5KF-lhPOzbWzGj28OCkJhuYqBc53Jc2cV"

async def main():
    clubs = [ClubBot(scid_token, webhook_url)]
    for club in clubs:
        await club.login()

    while True:
        for club in clubs: 
            await club.process()
            await asyncio.sleep(1)

asyncio.run(main())