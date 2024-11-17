import aiohttp
import asyncio
from hilo_conversion import get_tag
from my_requests import hp_request, sc_request

CLUB_ROLES = {
    1: "Member",
    3: "Senior",
    2: "President",
    4: "Vice-President"
}

class ClubBot:
    def __init__(self, scid_token, webhook_url):
        self.scid_token = scid_token
        self.webhook_url = webhook_url
        self.meowToken = ""

    async def login(self):
        async with aiohttp.ClientSession() as client:
            headers = {
                "authorization": f"Bearer {self.scid_token}",
                "User-Agent": f"scid/1.4.16-f (iOS 16.7.8; laser-prod; iPhone10,3"
            }
            response = await client.get("https://security.id.supercell.com/api/security/v1/sessionToken", headers=headers, timeout=20.0)
            data = await response.json()
            print(data)
            if data["ok"]:
                form_data = {"scid_token": data["token"], "application": "laser-prod"}
                await client.post("https://id.supercell.com/api/ingame/account/tokenLogin.confirm",
                                                headers={"content-type": "application/x-www-form-urlencoded; charset=utf-8"},
                                                data=form_data)
                response = await hp_request(f"bot/{data["token"]}/doLogin")
                while True:
                    try:
                        # TODO: Remove hardcoded value when AllianceInfo works
                        self.name = "testii"
                        self.meowToken = response["meowToken"]
                        print(f"Logged in: {response}")
                        return
                    except:
                        print(f"Couldn't login: error code {response["status"]}, Retrying in 10s")
                        await asyncio.sleep(10)
                    
    async def process(self):
        response = await hp_request(f"bot/{self.meowToken}/getUpdates")
        if response["state"]==0:
            for message in response["response"]:
                await self.process_message(message)
        
    async def process_message(self, message):
        tag = get_tag(message["AccountId"])
        # TODO: Remove hardcoded value when AccountId works
        tag = "GC2GPURJ8"
        data = await sc_request(f"players/%23{tag}")
        player_name = message["PlayerName"]
        role = CLUB_ROLES[message["PlayerRole"]]
        content = message["Message"]
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

