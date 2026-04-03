#!/usr/bin/python3
import json
from time import time, sleep
from base64 import b64encode, b64decode
from http.server import HTTPServer, BaseHTTPRequestHandler

import requests

class État:
    joueurs : dict[str:dict[str:any]] = {}
    """
    {
        "<id>":{
            "nom":"<nom>", // Nom du bot
            "adresse":str, // Adresse à laquelle il s'est connecté
            "erreurs":[ // Liste des erreurs obtenues lors du dernier tours
                "<message>",
                ...
            ],
            "action" : [true,false], // Dernier coup (True = Collaboration, False = Trahison)
            "points" : int, // Nombre de points total
            "points_obtenus" : int // Nombre de points obtenus lors du dernier tour
        },
        ...
    }
    """

    def inscrire_joueur(nom : str, adresse : str) -> str:
        joueur_id = b64encode((nom+":"+str(time())).encode()).decode("utf8")
        État.joueurs[joueur_id] = {
            "nom":nom,
            "adresse":adresse,
            "erreurs":[],
            "action":True,
            "points":0,
            "points_obtenus":0
        }
        return joueur_id
    
    def valider_joueur(jeton : str) -> bool:
        return jeton in État.joueurs_ids

class ServeurHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/connection":
            nom : str = None
            adresse : str = None
            try:
                infos = json.loads(self.rfile.read())
                nom = infos["nom"]
                adresse = infos["adresse"]
            except Exception as e:
                self.send_response(400,"Les données n'ont pas pus être analysées.")
                self.end_headers()
                return
            
            # Tester l'adresse fournie
            try:
                réponse = requests.get(url=adresse+"/ping")
                if json.loads(réponse.content.decode())["réponse"] != "pong":
                    self.send_response(400,"Le joueur n'a pas répondu avec {\"réponse\":\"pong\"}.")
                    self.end_headers()
                    return
            except Exception as e:
                self.send_response(400,"Une erreur est survenue lors de la communication avec le joueur.")
                self.end_headers()
                return

            joueur_id = État.inscrire_joueur(nom,adresse)

            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()

            self.wfile.write(json.dumps({"jeton":joueur_id}).encode())
            return
        
        self.send_response(404,"Ce noeud n'existe pas")

async def init_serveur():
    serveur = HTTPServer(('',5000),ServeurHTTP)
    await serveur.serve_forever()

def init():
    init_serveur()

    while len(État.joueurs_ids) < 3:
        sleep(0.5)

def boucle():
    # 250 tours
    for i in range(250):
        # Construire les informations du jeu
        joueurs_infos : dict[str:dict[str:any]] = {}
        joueurs_noms : list[str] = []
        for k in État.joueurs.keys():
            joueurs_noms.append(État.joueurs["nom"])
            joueurs_infos[État.joueurs["nom"]] = {
                "points":État.joueurs[k]["points"],
                "points_obtenus":État.joueurs[k]["points_obtenus"],
                "action":État.joueurs[k]["action"]
            }
        infos = {
            "erreurs":None,
            "joueurs":joueurs_noms,
            "joueurs_info":joueurs_infos,
        }

        # Demander les actions de chaque joueur
        for j in État.joueurs.keys():
            infos["erreurs"] = État.joueurs[k]["erreurs"]
            État.joueurs[k]["erreurs"].clear()
            réponse = requests.get(
                url=État.joueurs[k]["adresse"]+"/tour",
                json=infos
                )

            try:
                action = json.loads(réponse.content.decode())["action"]
            except Exception as e:
                message = "Les données n'ont pas pus être interprétées correctement :\n"+str(e)
                print(message)
                État.joueurs[k]["erreurs"].append(message)
                État.joueurs[k]["points_obtenus"] = 0
                État.joueurs[k]["action"] = None
                continue
            
            if action is not bool:
                message = "L'action donnée n'est pas valide."
                print(message)
                État.joueurs[k]["erreurs"].append(message)
                État.joueurs[k]["points_obtenus"] = 0
                État.joueurs[k]["action"] = None
                continue
            
            État.joueurs[k]["action"] = action
        
        # Exécuter le tour
        for k1 in État.joueurs.keys():
            État.joueurs[k1]["points_obtenus"] = 0
            if État.joueurs[k1]["action"] is not bool:
                message = "Impossible de jouer le tour : l'action donnée n'est pas valide."
                print(message)
                État.joueurs[k]["erreurs"].append(message)
                continue

            for k2 in État.joueurs.keys():
                if k1 == k2:
                    continue

                if État.joueurs[k2]["action"] is not bool:
                    message = "Impossible de jouer le tour : l'action donnée par l'opposant n'est pas valide."
                    print(message)
                    État.joueurs[k]["erreurs"].append(message)
                    continue
                
                if État.joueurs[k1]["action"] and État.joueurs[k2]["action"]:
                    État.joueurs[k1]["points_obtenus"] += 2
                elif État.joueurs[k1]["action"] and not État.joueurs[k2]["action"]:
                    État.joueurs[k1]["points_obtenus"] += 3
                elif not État.joueurs[k1]["action"] and not État.joueurs[k2]["action"]:
                    État.joueurs[k1]["points_obtenus"] += 1
                # else Faux et Faux : points_obtenus += 0

            État.joueurs[k1]["points"] += État.joueurs[k1]["points_obtenus"]

def destruction():
    pass

def main():
    init()
    boucle()
    destruction()

if __name__ == "__main__":
    main()