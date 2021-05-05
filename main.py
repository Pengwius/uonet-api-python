from fastapi import FastAPI
import json
import requests
from cryptography.fernet import Fernet

#api
from api.login import sender

#models
from models.LoginModel import LoginModel

app = FastAPI()

@app.post("/login/")
async def login(data: LoginModel):
    loginName = data.login
    Password = data.password
    symbol = data.symbol
    journal = data.journal
    if journal != 'http://cufs.fakelog.cf/':
        link = f'{journal}{symbol}/Account/LogOn?ReturnUrl=%2F{symbol}%2FFS%2FLS%3Fwa%3Dwsignin1.0%26wtrealm%3Dhttps%253a%252f%252fuonetplus.vulcan.net.pl%252f{symbol}%252fLoginEndpoint.aspx%26wctx%3Dhttps%253a%252f%252fuonetplus.vulcan.net.pl%252f{symbol}%252fLoginEndpoint.aspx'
    else:
        link = 'http://cufs.fakelog.cf/powiatwulkanowy/FS/LS?wa=wsignin1.0&wtrealm=http://uonetplus.fakelog.localhost:300/powiatwulkanowy/LoginEndpoint.aspx&wctx=http://uonetplus.fakelog.localhost:300/powiatwulkanowy/LoginEndpoint.aspx'
    s = requests.Session()
    sender_return = sender(link, loginName, Password, ('loginName', 'Password'), 'Zła nazwa użytkownika lub hasło', symbol, journal, s)
    if sender_return == {'success': False}:
        data_response = {
            'success': False
        }
    else:
        session_key = Fernet.generate_key().decode('utf-8')
        rkey = Fernet(bytes(session_key, 'utf-8'))
            
        sender_return['s'] = json.dumps(sender_return['s'])
        sender_return['s'] = sender_return['s'].encode()
        sender_return['s'] = rkey.encrypt(sender_return['s'])
        sender_return['s'] = sender_return['s'].decode('utf-8')
        data_response = {'success': True, 'data': sender_return}
    return data_response