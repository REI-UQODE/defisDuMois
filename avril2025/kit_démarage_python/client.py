#!/usr/bin/python3
import json
import subprocess
import os
import sys
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

import requests
from bot import Bot

class État:
    bot_nom : str = None
    serveur_rep : str = None
    adresse : str = "http://127.0.0.1:5000"
    
    bot : Bot = Bot()
    dernier_tour : dict[str:any] = None

def analyser_arguments():
    if "--help" in sys.argv or "-h" in sys.argv or "-?" in sys.argv:
        print(
"""
USAGE client.py <nom> [ARGS]

<nom>   Nom du bot à donner au serveur

ARGS

--help          -h -?   Afficher ce message d'aide

--serveur-rep   -s      Répertoire de l'exécutable du serveur de jeu. Si fournit, lancera 
                        le serveur. Sinon, s'attend à ce que le serveur soit déjà en 
                        exécution.

--adresse       -a      Adresse à laquelle se trouve le serveur de jeu. 
                        Par défaut : 127.0.0.1:5000
"""
        )
        exit()

    if len(sys.argv) < 2:
        print("Nombre d'arguments insufisants. Essayez : \nclient.py --help")
        exit()

    État.bot_nom = sys.argv[1]

    if "--serveur-rep" in sys.argv or "-s" in sys.argv:
        try:
            État.serveur_rep = sys.argv[sys.argv.index("-s" if "-s" in sys.argv else "--serveur-rep") + 1]
            os.path.exists(État.serveur_rep)
        except Exception:
            print("Le chemin vers le serveur est invalide ou inexistant.")
            exit()
    
    if "--adresse" in sys.argv or "-a" in sys.argv:
        État.adresse = sys.argv[sys.argv.index("-a" if "-a" in sys.argv else "--adresse") + 1]
        if not (État.adresse.startswith("http://") or État.adresse.startswith("https://")):
            État.adresse = "http://"+État.adresse
    
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
            réponse = requests.get(url = État.adresse+"/connection", json = {"nom":État.bot_nom})
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
    while True:
        action = État.bot.tour(État.dernier_tour)
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
    analyser_arguments()
    if État.serveur_rep:
        print("Initialisation du serveur")
        init_serveur()
    print("Connection au serveur")
    connecter_serveur()
    boucle()

if __name__ == "__main__":
    main()