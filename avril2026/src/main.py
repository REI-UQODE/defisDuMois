from bot import Bot, testBot

class Jeu:
    def __init__(self):
        self.joueurs = None

def main():
    bots = [
        Bot(),
        testBot(),
        testBot()]

    for i in range(250):
        for b in bots:
            b.action = b.tour(bots)

        for b1 in bots:
            b1.points_obtenus = 0
            for b2 in bots:
                if b1 == b2:
                    continue
                
                if b1.action and b2.action:
                    b1.points_obtenus += 2
                elif b1.action and not b2.action:
                    b1.points_obtenus += 3
                elif not b1.action and not b2.action:
                    b1.points_obtenus += 1
                # else Faux et Vrai : b1.points_obtenus += 0
            
            b1.points += b1.points_obtenus

if __name__ == "__main__":
    main()