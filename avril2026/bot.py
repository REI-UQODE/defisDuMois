from __future__ import annotations
import random

class Bot:
    def __init__(self):
        self.action : bool = True
        self.points : int = 0
        self.points_obtenus : int = 0
    
    def tour(self, bots : list[Bot,TestBot]) -> bool:
        # Vous pouvez faire mieux ;)
        return random.choice([True,False])

class TestBot:
    def __init__(self):
        self.action : bool = True
        self.points : int = 0
        self.points_obtenus : int = 0
    
    def tour(self, bots : list) -> bool:
        return random.choice([True,False])