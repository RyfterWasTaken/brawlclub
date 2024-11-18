from base64 import b64decode as base64_b64decode
from datetime import datetime
from json import loads as json_loads
import requests
from datetime import datetime

def get_key(email, password):
    _keys = []
    keys = None
    key_names = "club_bot/auto_generated"
    key_scopes = "brawlstars"
    print("Getting key")

    with requests.Session() as client:
        body = {"email": email, "password": password}
        response = client.post("https://developer.brawlstars.com/api/login", json=body)
        if response.status_code == 403:
            raise ValueError("Invalid brawl stars developer credentials")
        ip = json_loads(base64_b64decode((response.json())["temporaryAPIToken"].split(".")[1] + "====").decode("utf-8"))["limits"][1]["cidrs"][0].split("/")[0]     

        response = client.post("https://developer.brawlstars.com/api/apikey/list")
        keys = response.json()["keys"]
        _keys.extend(key for key in keys if key["name"] == key_names)

        for key in _keys:
            if ip in key["cidrRanges"]:
                return key["key"]
            else:
                client.post("https://developer.brawlstars.com/api/apikey/revoke", json={"id": key["id"]}) 

        data = {
            "name": key_names,
            "description": "Created on {}".format(datetime.now().strftime("%c")),
            "cidrRanges": [ip],
            "scopes": [key_scopes],
        }

        response = client.post("https://developer.brawlstars.com/api/apikey/create", json=data)
        data = response.json()
        return data["key"]["key"]

