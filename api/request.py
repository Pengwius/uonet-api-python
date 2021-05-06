import requests
import json

def _post(url: str, headers: dict, cookies: dict, payload: dict, student: dict):
    cookies.update({
            "biezacyRokSzkolny": f"{student['DziennikRokSzkolny']}",
            "idBiezacyDziennik": f"{student['IdDziennik']}",
            "idBiezacyDziennikPrzedszkole": f"{student['IdPrzedszkoleDziennik']}",
            "idBiezacyUczen": f"{student['IdUczen']}"
        })

    response = requests.post(url=url, headers=headers, cookies=cookies, json=payload)

    return response.json()