import os
import aiohttp
import asyncio
from key_gen import get_key
from dotenv import load_dotenv

load_dotenv()  

hp_key = os.getenv('HPKEY')

dev_email = os.getenv('DEVEMAIL')
dev_pass = os.getenv('DEVPASSWORD')
sc_key = ""

async def init():
    global sc_key
    sc_key = await get_key(dev_email, dev_pass)
    
asyncio.run(init())


async def hp_request(endpoint):
    try:
        async with aiohttp.ClientSession() as client:
            response = await client.get(f"https://api.hpdevfox.ru/{endpoint}?api_key={hp_key}", timeout=20.0)
            try:
                return await response.json()
            except Exception as e: 
                return {
                    "state": response.status_code,
                    "details": response.text,
                    "exception": e
                }
    except aiohttp.ClientError as timeout:
        return {
            "state": 408,
            "details": timeout,
        }
    except Exception as e:
        return {
            "state": 520,
            "details": e
        }

async def sc_request(endpoint):
    try:
        async with aiohttp.ClientSession() as client:
            headers = {
                "content/type": "application/json",
                "Authorization": f"Bearer {sc_key}"
            }
            response = await client.get(f"https://api.brawlstars.com/v1/{endpoint}", headers=headers, timeout=20.0)
            try:
                return await response.json()
            except Exception as e: 
                return {
                    "status": response.status,
                    "details": await response.text(),
                    "exception": e
                }
    except aiohttp.ClientError as timeout:
        return {
            "state": 408,
            "details": timeout,
        }
    except Exception as e:
        return {
            "state": 520,
            "details": e
        }
    
