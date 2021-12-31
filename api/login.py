import requests
import json
from bs4 import BeautifulSoup
import datetime

def sender(url, loginName, Password, params_names, fail_phrase, symbol, journal, s):
    data = [params_names[0], loginName, params_names[1], Password]

    sender_return = send(url, data, fail_phrase, journal, symbol, s)
    if sender_return == {'success': False}:
        return {'success': False}
    else:
        return sender_return

def send(url, data, fail, journal, symbol, s):
    ready_data = {data[0]: data[1], data[2]: data[3]}
    page = s.post(url=url, data=ready_data)
    if fail in page.text:
        return {'success': False}
    else:
        if journal == 'http://cufs.fakelog.cf/':
            page = s.get('http://cufs.fakelog.cf/powiatwulkanowy/FS/LS?wa=wsignin1.0&wtrealm=http://uonetplus.fakelog.localhost:300/powiatwulkanowy/LoginEndpoint.aspx&wctx=http://uonetplus.fakelog.localhost:300/powiatwulkanowy/LoginEndpoint.aspx')
        bs = BeautifulSoup(page.text, 'html.parser')
        wa = bs.find('input', {'name': 'wa'})['value']
        cert = bs.find('input', {'name': 'wresult'})['value']
        wctx = bs.find('input', {'name': 'wctx'})['value']

        crtr = s.post(url=wctx, headers={"User-Agent": "Wulkanowy-web :)"}, data={"wa": wa, "wresult": cert, "wctx": wctx})

        if 'nie został zarejestrowany w bazie szkoły, do której się logujesz' in crtr.text:
            return {'success': False}

        bs = BeautifulSoup(crtr.content, 'html.parser')
        for a in bs.find_all('a', title='Uczeń'):
            school_url = a['href']
            break

        if journal == 'http://cufs.fakelog.cf/':
            school_url = 'http://uonetplus-uczen.fakelog.cf/powiatwulkanowy/123458'

        cookies = get_cookies(symbol, school_url, s, journal)

        return cookies

def get_cookies(symbol, school_url, s, journal):
    students = s.post(school_url+'/UczenDziennik.mvc/Get')
    register_id = students.json()['data'][0]['Okresy'][0]['Id']
            
    now = datetime.datetime.now()
    weekday = now.weekday()

    for x in range(7):
        if weekday == x:
            now = now - datetime.timedelta(days=x)

    day = now.day
    month = now.month
    year = now.year

    date = datetime.date(year, month, day).isoformat()

    date = f'{date}T00:00:00'

    school_year = students.json()['data'][0]['DziennikRokSzkolny']

    data = {
        'register_id': register_id,
        'students': students.json(),
        'school_url': school_url,
        'date': str(date),
        'school_year': school_year,
        'symbol': symbol,
        's': s.cookies.get_dict(),
        'journal': journal
    }

    return data