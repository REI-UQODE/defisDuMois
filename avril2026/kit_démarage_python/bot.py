import random
from time import time

class Bot:
    NOM : str = "Super Bot Python!" + str(time())
    SERVEUR_REP : str = "../serveur_src/serveur.py" # Répertoire vers l'exécutable du serveur. Si non fournit, présumerra qu'il est déjà en marche
    ADRESSE : str = "127.0.0.1:5000" # Adresse pour se connecter au serveur

    def __init__(self):
        pass

    def tour(self, dernier_tour : dict[str:any]) -> bool:
        print(dernier_tour)
        # Vous pouvez faire mieux ;)
        return random.choice([True,False])