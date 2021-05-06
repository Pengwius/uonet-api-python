import json
from cryptography.fernet import Fernet

def decode_cookies(cookies: bytes, sessionkey: str):
    with open("db.json", "r") as f:
        db = json.loads(f.read())
    
    key = db["users"][sessionkey]["key"]

    rkey = Fernet(key)

    cookies = rkey.decrypt(cookies)
    cookies = json.loads(cookies.decode("utf-8"))
    
    return cookies