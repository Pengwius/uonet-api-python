from fastapi import FastAPI, Response, Request, HTTPException

def authenticate(request: Request):
    cookie_authorization: str = request.cookies.get("sessionkey")
    if(cookie_authorization == None):
        return {"status_code": 403, "details": "Invalid authentication - user not logged in"}
    else:
        return {"status_code": 200, "details": "OK"}