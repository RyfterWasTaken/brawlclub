import os
import aiohttp
from modules.key_gen import get_key
from modules.config import dev_email, dev_pass, hp_key

sc_key = get_key(dev_email, dev_pass)


async def hp_request(endpoint):
    async with aiohttp.ClientSession() as client:
        response = await client.get(f"https://api.hpdevfox.ru/{endpoint}?api_key={hp_key}", timeout=20.0)
        response.raise_for_status()
        try:
            return await response.json()
        except Exception as e: 
            return await response.text()

async def sc_request(endpoint):
    async with aiohttp.ClientSession() as client:
        headers = {
            "content/type": "application/json",
            "Authorization": f"Bearer {sc_key}"
        }
        response = await client.get(f"https://api.brawlstars.com/v1/{endpoint}", headers=headers, timeout=20.0)
        response.raise_for_status()
        try:
            return await response.json()
        except Exception as e: 
            return await response.text()
    
