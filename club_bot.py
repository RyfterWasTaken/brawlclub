import discord
import aiohttp, httpx, asyncio
from hilo_conversion import get_tag
from my_requests import hp_request, sc_request


CLUB_ROLES = {
    1: "Member",
    3: "Senior",
    2: "President",
    4: "Vice-President"
}

class ClubBot:
    def __init__(self, scid_token, channel_id):
        self.scid_token = scid_token
        self.channel_id = channel_id
        self.webhook_url = ""
        self.meowToken = ""
        self.name = "Unknown"

    async def login(self, bot: discord.Bot, retry = True):
        async with aiohttp.ClientSession() as client:
            headers = {
                "authorization": f"Bearer {self.scid_token}",
                "User-Agent": f"scid/1.4.16-f (iOS 16.7.8; laser-prod; iPhone10,3"
            }
            response = await client.get("https://security.id.supercell.com/api/security/v1/sessionToken", headers=headers, timeout=20.0)
            response = await response.json()
            if response["ok"]:
                form_data = {"scid_token": response["token"], "application": "laser-prod"}
                await client.post("https://id.supercell.com/api/ingame/account/tokenLogin.confirm",
                                                headers={"content-type": "application/x-www-form-urlencoded; charset=utf-8"},
                                                data=form_data)
                
                token = response["token"]
                while True:
                    try:
                        response = await hp_request(f"bot/{token}/doLogin")
                        print(response)
                        if response["state"]==503: raise Exception()
                        self.meowToken = response["meowToken"]

                        print(f"Logged in: {response}")
                        
                        channel = await bot.fetch_channel(self.channel_id)
                        for webhook in await channel.webhooks():
                            if webhook.name == "club-bot webhook":
                                self.webhook_url = webhook.url
                        if not self.webhook_url:
                            webhook = await channel.create_webhook(name = "club-bot webhook")
                            self.webhook_url = webhook.url
                    
                        return

                    except Exception as e:
                        if retry==False:
                            raise Exception("An error occured, please try again later")
                        print(f"Couldn't login: {e}, retrying in 10s")
                        await asyncio.sleep(10)
                    
                        


    async def process(self):
        response = await hp_request(f"bot/{self.meowToken}/getUpdates")
        for message in response["response"]:
            if message["messageType"]=="AllianceData":
                self.name = message["payload"]["AllianceHeaderEntry"]["Name"]
            else: print(message)
                # await self.process_message(message)
        
    async def process_message(self, message):
        # TODO: Remove hardcoded value when AccountId works
        # tag = get_tag(message["AccountId"])
        tag = "GC2GPURJ8"
        player_name = message["PlayerName"]
        role = CLUB_ROLES[message["PlayerRole"]]
        content = message["Message"]

        data = await sc_request(f"players/%23{tag}")
        print(f"{player_name} ({role} of {self.name}) sent {content}")
        data = {
            "content": "",
            "username": player_name,
            "avatar_url": f"https://cdn.brawlify.com/profile-icons/regular/{data["icon"]["id"]}.png",
            "embeds": [{
                    "description": content,
                    "footer": {"text": f"{self.name} - {role}"}
                }]
            }
        
        async with aiohttp.ClientSession() as client:
            await client.post(self.webhook_url, json=data)

