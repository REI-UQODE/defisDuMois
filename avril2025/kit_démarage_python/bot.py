import random

class Bot:
    def __init__(self):
        pass

    def tour(self, dernier_tour : dict[str:any]) -> bool:
        print(dernier_tour)
        # Vous pouvez faire mieux ;)
        return random.choice([True,False])