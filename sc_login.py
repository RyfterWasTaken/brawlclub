import aiohttp, urllib

async def request_login(email):
    async with aiohttp.ClientSession() as client:
        data = {
            "lang": "en",
            "email": email,
            "remember": "true",
            "game": "laser", 
            "env": "prod",
        }
        encoded_data = urllib.parse.urlencode(data)
        
        return await client.post("https://id.supercell.com/api/ingame/account/login", headers={
            "accept-encoding": "gzip",
            "accept-language": "ru",
            "content-length": str(len(encoded_data)),
            "content-type": "application/x-www-form-urlencoded; charset=utf-8",
            "host": "id.supercell.com",
            "user-agent": "scid/1.4.16-f (Android 15; laser-prod; Pixel)"
        }, data=data)

async def validate_login(email, pin):
    async with aiohttp.ClientSession() as client:
        payload = {"email": email, "pin": pin}
        headers = {"User-Agent": f"scid/1.4.16-f (Android 15; laser-prod; Pixel)", "content-type": "application/x-www-form-urlencoded; charset=utf-8"}
        try:
            response = await client.post("https://id.supercell.com/api/ingame/account/login.validate", headers=headers, data=payload)
            data = await response.json()
            tag = data["data"]["application"]["account"]

            response = await client.post("https://id.supercell.com/api/ingame/account/login.confirm", headers=headers, data=payload)
            data = await response.json()
            if data["ok"] == True:
                token = data["data"]["scidToken"]

                return {
                    "ok": True,
                    "tag": tag,
                    "token": token
                }   
            else: return {"ok": False}
        except Exception as e:
            return {
                "ok": False,
                "details": e
            }

