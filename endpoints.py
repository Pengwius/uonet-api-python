from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import requests
from cryptography.fernet import Fernet
from datetime import datetime
import models
import authentication
from decode_cookies import decode_cookies

#api
from api.login import sender
from api.request import _post

app = FastAPI()

SESSION_EXPIRES_TIME = 1200

@app.post("/login/")
async def login(data: models.LoginModel):
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
        key = Fernet.generate_key().decode('utf-8')
        session_key = Fernet.generate_key().decode('utf-8')

        user = {
            "key": key,
            "expiration_date": datetime.now().timestamp()+SESSION_EXPIRES_TIME
        }

        f = open("db.json", "r")
        db = f.read()
        f.close()

        db_json = json.loads(db)
        db_json["users"].update({session_key: user})

        f = open("db.json", "w")
        json.dump(db_json, f)
        f.close()

        
        rkey = Fernet(bytes(key, 'utf-8'))
            
        sender_return['s'] = json.dumps(sender_return['s'])
        sender_return['s'] = sender_return['s'].encode()
        sender_return['s'] = rkey.encrypt(sender_return['s'])
        sender_return['s'] = sender_return['s'].decode('utf-8')
        data_response = {'success': True, 'data': sender_return}
        response = JSONResponse(content=data_response)
        response.set_cookie(key="sessionkey", value=session_key)

    return response

@app.post("/grades/")
async def grades(request: Request):
    auth = authentication.authenticate(request)
    if auth["status_code"] == 200:
        body = await request.json()

        register_id = body["register_id"]
        school_url = body["school_url"]
        student = body["student"]
        cookies = bytes(body["cookies"], "utf-8")

        sessionkey = request.cookies.get("sessionkey")

        cookies = decode_cookies(cookies, sessionkey)

        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            "User-Agent": "wulkanowy-api-python"
        }
        
        grades = _post(f"{school_url}/Oceny.mvc/Get", headers, cookies, {'okres': register_id}, student)

        return grades
    else:
        raise HTTPException(
            status_code=auth["status_code"],
            detail=auth["details"]
        )

@app.post("/homeworks/")
async def homeworks(request: Request):
    auth = authentication.authenticate(request)
    if auth["status_code"] == 200:
        body = await request.json()

        register_id = body["register_id"]
        school_url = body["school_url"]
        student = body["student"]
        date = body["date"]
        school_year = body["school_year"]
        cookies = bytes(body["cookies"], "utf-8")

        sessionkey = request.cookies.get("sessionkey")

        cookies = decode_cookies(cookies, sessionkey)

        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            "User-Agent": "wulkanowy-api-python"
        }
        
        homeworks = _post(f"{school_url}/Homework.mvc/Get", headers, cookies, {'schoolYear': school_year, 'date': date, 'statusFilter': '-1'}, student)

        return homeworks
    else:
        raise HTTPException(
            status_code=auth["status_code"],
            detail=auth["details"]
        )

@app.post("/timetable/")
async def timetable(request: Request):
    auth = authentication.authenticate(request)
    if auth["status_code"] == 200:
        body = await request.json()

        register_id = body["register_id"]
        school_url = body["school_url"]
        student = body["student"]
        date = body["date"]
        cookies = bytes(body["cookies"], "utf-8")

        sessionkey = request.cookies.get("sessionkey")

        cookies = decode_cookies(cookies, sessionkey)

        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            "User-Agent": "wulkanowy-api-python"
        }
        
        timetable = _post(f"{school_url}/PlanZajec.mvc/Get", headers, cookies, {'data': date}, student)

        return timetable
    else:
        raise HTTPException(
            status_code=auth["status_code"],
            detail=auth["details"]
        )