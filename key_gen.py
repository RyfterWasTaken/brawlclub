import logging
from base64 import b64decode as base64_b64decode
from datetime import datetime
from json import loads as json_loads
import aiohttp

LOG = logging.getLogger(__name__)
KEY_MINIMUM, KEY_MAXIMUM = 1, 10

async def get_key(email, password):
    _keys = []
    keys = None
    key_names: str = "club_bot/auto_generated"
    key_scopes: str = "brawlstars"
    print("Getting key")
    async with aiohttp.ClientSession() as client:
        body = {"email": email, "password": password}
        resp = await client.post("https://developer.brawlstars.com/api/login", json=body)
        if resp.status == 403:
            LOG.error("Invalid credentials used when attempting to log in")
            await client.close()
            raise
        ip = json_loads(base64_b64decode((await resp.json())["temporaryAPIToken"].split(".")[1] + "====").decode("utf-8"))["limits"][1]["cidrs"][0].split("/")[0]     
        
        resp = await client.post("https://developer.brawlstars.com/api/apikey/list")
        keys = (await resp.json())["keys"]
        _keys.extend(key for key in keys if key["name"] == key_names)

        for key in _keys:
            if ip in key["cidrRanges"]:
                return key["key"]
            else:
                await client.post("https://developer.brawlstars.com/api/apikey/revoke", json={"id": key["id"]}) 

        data = {
            "name": key_names,
            "description": "Created on {}".format(datetime.now().strftime("%c")),
            "cidrRanges": [ip],
            "scopes": [key_scopes],
        }

        resp = await client.post("https://developer.brawlstars.com/api/apikey/create", json=data)
        data = await resp.json()
        return data["key"]["key"]
