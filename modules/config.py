import os
from dotenv import load_dotenv

load_dotenv()  

bot_token = os.getenv('BOTTOKEN')

hp_key = os.getenv('HPKEY')

dev_email = os.getenv('DEVEMAIL')
dev_pass = os.getenv('DEVPASSWORD')

class _db:
    host = os.getenv('DBHOST')
    port = int(os.getenv('DBPORT'))
    name = os.getenv('DBNAME')
    user = os.getenv('DBUSERNAME')
    password = os.getenv('DBPASSWORD')
db = _db()




