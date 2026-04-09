#!/usr/bin/python3
import json
import subprocess
import os
import sys
import time
import requests

from bot import Bot

class État:
    bot_nom : str = Bot.NOM
    serveur_rep : str = Bot.SERVEUR_REP
    adresse : str = Bot.ADRESSE
    
    bot : Bot = Bot()
    dernier_tour : dict[str:any] = None
    jeton : str = None
    
def init_serveur():
    try:
        if os.name == "nt":
            try:
                subprocess.Popen(["python",État.serveur_rep])
            except Exception:
                subprocess.Popen(["py",État.serveur_rep])
        else:
            subprocess.Popen(["python3",État.serveur_rep,"-n","2"])
    except Exception:
        print("Le serveur n'a pas pus être créé")
        exit()

def connecter_serveur():
    while True:
        try:
            réponse = requests.get(url = État.adresse+"/connection", params = {"nom":État.bot_nom})
            if réponse.status_code != 200:
                print(str(réponse.status_code)+": "+réponse.reason)
                time.sleep(1)
                continue
            État.jeton = json.loads(réponse.content.decode())["jeton"]
            break
        except Exception as e:
            print(e)
            time.sleep(1)

def boucle():
    # Attendre le début de la partie
    action = État.bot.tour(État.dernier_tour)
    while True:
        réponse = requests.post(
                url=État.adresse+"/tour",
                headers={"Authorization":"Bearer "+État.jeton},
                json={"action":action}
            )
        if réponse.status_code == 503:
            print(str(réponse.status_code)+": "+réponse.reason)
            time.sleep(0.1)
            continue

        if réponse.status_code != 200:
            print(str(réponse.status_code)+": "+réponse.reason)
        État.dernier_tour = json.loads(réponse.content.decode())
        break

    for i in range(250):
        print("Tour "+str(i))
        try:
            action = État.bot.tour(État.dernier_tour)
            réponse = requests.post(
                    url=État.adresse+"/tour",
                    headers={"Authorization":"Bearer "+État.jeton},
                    json={"action":action}
                )
            if réponse.status_code != 200:
                print(str(réponse.status_code)+": "+réponse.reason)
                continue
            État.dernier_tour = json.loads(réponse.content.decode())
        except Exception as e:
            print(e)

def main():
    if État.serveur_rep:
        print("Initialisation du serveur")
        init_serveur()
    print("Connection au serveur")
    connecter_serveur()
    boucle()

if __name__ == "__main__":
    main()