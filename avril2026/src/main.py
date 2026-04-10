import json

from bot import Bot, TestBot

class Jeu:
    def __init__(self):
        self.joueurs = None

def main():
    bots = [
        Bot(),
        TestBot(),
        TestBot()]

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
        
        print("Tour "+str(i))
        print(json.dumps(
            {
                "Bot":{
                    "action":bots[0].action,
                    "points":bots[0].points,
                    "gains":bots[0].points_obtenus
                },
                "TestBot1":{
                    "action":bots[1].action,
                    "points":bots[1].points,
                    "gains":bots[1].points_obtenus
                },
                "TestBot2":{
                    "action":bots[2].action,
                    "points":bots[2].points,
                    "gains":bots[2].points_obtenus
                }
            }, indent=2)
            )

if __name__ == "__main__":
    main()