#!/usr/bin/python3
import json
import sys
from time import time, sleep
from base64 import b64encode, b64decode
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

class État:
    port : int = 5000

    joueurs : dict[str:dict[str:any]] = {}
    """
    {
        "<id>":{
            "nom":"<nom>", // Nom du bot
            "action" : [true,false], // Dernier coup (True = Collaboration, False = Trahison)
            "points" : int, // Nombre de points total
            "points_obtenus" : int // Nombre de points obtenus lors du dernier tour
            "état_tour" : int // État de traitement de la soumission d'un tour
        },
        ...
    }
    """
    n_joueurs_attente : int = 3
    tours_jeu : int = 0
    infos_jeu : dict[str:any] = None

    def réinitialiser():
        État.joueurs = {}
        État.tours_jeu = 0
        État.infos_jeu = None

    def inscrire_joueur(nom : str) -> str:
        joueur_id = b64encode((nom+":"+str(time())).encode()).decode("utf8")
        État.joueurs[joueur_id] = {
            "nom":nom,
            "action":True,
            "points":0,
            "points_obtenus":0,
            "état_tour" : 0
        }
        return joueur_id

class ServeurHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        # Analyse des paramètres
        paramètres = {}
        if '?' in self.path:
            self.path, mots = self.path.split('?')
            mots = mots.split('&')
            for m in mots:
                k,v = m.split('=')
                paramètres[k] = v

        if self.path == "/connection":
            if len(État.joueurs) >= État.n_joueurs_attente:
                self.send_response(400, "La partie est déjà débutée. Veuillez attendre une nouvelle partie.")
                self.end_headers()
                return

            if "nom" not in paramètres:
                self.send_response(400,"Le paramètre 'nom' doit être spécifié dans l'url")
                self.end_headers()
                return

            nom : str = paramètres["nom"]

            for k in État.joueurs:
                if État.joueurs[k]["nom"] == nom:
                    self.send_response(400,"Le joueur est déjà inscrit.")
                    self.end_headers()
                    return
            
            joueur_id = État.inscrire_joueur(nom)

            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()

            self.wfile.write(json.dumps({"jeton":joueur_id}).encode())
            return
        
        self.send_response(404,"Ce noeud n'existe pas")
        self.end_headers()
    
    def do_POST(self):
        # Analyse des paramètres
        paramètres = {}
        if '?' in self.path:
            self.path, mots = self.path.split('?')
            mots = mots.split('&')
            for m in mots:
                k,v = m.split('=')
                paramètres[k] = v

        if self.path == "/tour":
            jeton : str = None
            try:
                auth = self.headers.get("Authorization").split(" ")
                if auth[0] != "Bearer" or len(auth) != 2 or auth[1] not in État.joueurs:
                    self.send_response(401,"Veuillez vous connecter avant d'essayer de jouer.")
                    self.end_headers()
                    return
                jeton = auth[1]
                
            except Exception:
                self.send_response(401)
                self.end_headers()
                return

            octets_contenu = self.headers.get("Content-Length")
            if not octets_contenu:
                self.send_response(400,"L'en-tête 'Content-Length' doit être spécifié.")
                self.end_headers()
                return
            octets_contenu = int(octets_contenu)
            
            # Attendre la connection avec les autres joueurs
            if len(État.joueurs) < État.n_joueurs_attente:
                self.send_response(503, "En attente de la connection de "+str(État.n_joueurs_attente-len(État.joueurs))+" autres joueurs.")
                self.end_headers()
                return
            
            # Lire la soumission

            action : bool = None
            erreurs : list[str] = []
            try:
                action = json.loads(self.rfile.read(octets_contenu))["action"]
            except Exception as e:
                message = "Les données n'ont pas pus être interprétées correctement :\n"+str(e)
                print(message)
                erreurs.append(message)

            if not isinstance(action,bool):
                message = "L'action donnée n'est pas valide."
                print(message)
                erreurs.append(message)
            
            # Attendre que tous le monde aie finit le tour précédent
            est_prêt = False
            while not est_prêt:
                est_prêt = True
                for k in État.joueurs:
                    if État.joueurs[k]["état_tour"] == 3:
                        est_prêt = False
                        sleep(0.01)
                        break
            
            État.joueurs[jeton]["action"] = action
            État.joueurs[jeton]["état_tour"] = 1
            # print(État.joueurs[jeton]["nom"]+":\tTour "+str(État.tours_jeu)+" : Reçus soumission de "+État.joueurs[jeton]["nom"]+", action : "+str(État.joueurs[jeton]["action"])+", en attente des autres joueurs.")
            # print(État.joueurs)

            # Attendre les soumissions de chacun
            est_prêt = False
            while not est_prêt:
                est_prêt = True
                for k in État.joueurs:
                    if État.joueurs[k]["état_tour"] == 0:
                        est_prêt = False
                        sleep(0.01)
                        break
            
            # print(État.joueurs[jeton]["nom"]+":\tTous les joueurs ont soumis, exécution du tour.")
            
            # Exécuter le tour pour ce joueur
            État.joueurs[jeton]["points_obtenus"] = 0
            if isinstance(État.joueurs[jeton]["action"], bool):
                for k in État.joueurs.keys():
                    if jeton == k:
                        continue

                    if not isinstance(État.joueurs[k]["action"], bool):
                        message = "Impossible de jouer le tour : l'action donnée par l'opposant n'est pas valide."
                        print(message)
                        erreurs.append(message)
                        continue
                    
                    if État.joueurs[jeton]["action"] and État.joueurs[k]["action"]:
                        État.joueurs[jeton]["points_obtenus"] += 2
                    elif État.joueurs[jeton]["action"] and not État.joueurs[k]["action"]:
                        État.joueurs[jeton]["points_obtenus"] += 3
                    elif not État.joueurs[jeton]["action"] and not État.joueurs[k]["action"]:
                        État.joueurs[jeton]["points_obtenus"] += 1
                    # else Faux et Faux : points_obtenus += 0
            else:
                message = "Impossible de jouer le tour : l'action donnée n'est pas valide."
                print(message)
                erreurs.append(message)

            # print(État.joueurs[jeton]["nom"]+":\tGains : "+str(État.joueurs[jeton]["points_obtenus"])+"pts\tAvant :"+str(État.joueurs[jeton]["points"])+"pts")

            État.joueurs[jeton]["points"] += État.joueurs[jeton]["points_obtenus"]
            État.joueurs[jeton]["état_tour"] = 2

            # print(État.joueurs[jeton]["nom"]+":\tAprès :"+str(État.joueurs[jeton]["points"])+"pts")
            # print(État.joueurs[jeton]["nom"]+":\tEn attente que chacun soit traité.")

            # Attendre que le tour de chacun soit traité
            est_prêt = False
            while not est_prêt:
                est_prêt = True
                for k in État.joueurs:
                    if État.joueurs[k]["état_tour"] < 2:
                        est_prêt = False
                        sleep(0.01)
                        break

            # print(État.joueurs[jeton]["nom"]+":\tChaque tour est traité, envoie de la réponse.")

            # Construire l'état du jeu s'il est le premier à se rendre ici.
            if not État.infos_jeu:
                # print(État.joueurs[jeton]["nom"]+":\tEst premier, construction de l'état du jeu.")
                joueurs_infos : dict[str:dict[str:any]] = {}
                joueurs_noms : list[str] = []
                for k in État.joueurs.keys():
                    joueurs_noms.append(État.joueurs[k]["nom"])
                    joueurs_infos[État.joueurs[k]["nom"]] = {
                        "points":État.joueurs[k]["points"],
                        "points_obtenus":État.joueurs[k]["points_obtenus"],
                        "action":État.joueurs[k]["action"]
                    }
                État.infos_jeu = {
                    "joueurs":joueurs_noms,
                    "joueurs_info":joueurs_infos,
                }
            
            # Répondre au joueur
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            self.wfile.write(json.dumps(
                {
                    "erreurs":erreurs,
                    "joueurs":État.infos_jeu["joueurs"],
                    "joueurs_info":État.infos_jeu["joueurs_info"]
                }
            ).encode())

            # print(État.joueurs[jeton]["nom"]+":\tRéponse envoyée")

            # Nettoyage
            est_dernier = True
            for k in État.joueurs.keys():
                if k == jeton:
                    continue
                if État.joueurs[k]["état_tour"] != 3:
                    est_dernier = False
                    break

            État.joueurs[jeton]["état_tour"] = 3

            # Si c'est la dernière requête répondue
            if est_dernier:
                # print(État.joueurs[jeton]["nom"]+":\tEst dernier, nettoyage.")
                État.tours_soumis = 0
                État.tours_traités = 0
                État.tours_répondus = 0
                État.infos_jeu = None
                État.tours_jeu += 1

                for k in État.joueurs.keys():
                    État.joueurs[k]["état_tour"] = 0

                if État.tours_jeu >= 250:
                    # print(État.joueurs[jeton]["nom"]+":\tFin de la partie.")
                    État.réinitialiser()
            return

        self.send_response(404,"Ce noeud n'existe pas")
        self.end_headers()

def analyser_arguments():
    if "--help" in sys.argv or "-h" in sys.argv or "-?" in sys.argv:
        print(
"""
USAGE serveur.py [ARGS]

--help -h -?    Afficher ce message d'aide
-n <int>        Nombre de participants à cette partie
-p <int>        Port exposé pour la connection
"""
        )
        exit()

    if "-n" in sys.argv:
        try:
            État.n_joueurs_attente = int(sys.argv[sys.argv.index("-n")+1])
        except Exception:
            print("L'argument '-n' doit être suivit d'un entier.")
    if "-p" in sys.argv:
        try:
            État.port = int(sys.argv[sys.argv.index("-p")+1])
        except Exception:
            print("L'argument '-p' doit être suivit d'un entier.")

def main():
    analyser_arguments()
    ThreadingHTTPServer(('',État.port),ServeurHTTP).serve_forever()

if __name__ == "__main__":
    main()