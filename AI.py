import random
from player import Player


class Game_AI(Player):
    """the parent class ai for Table_Top"""
    
    def __init__(self, name:str, title:str):
        """
        `name`: the name of the ai.
        `title`: the title of the ai, normaly formated as The _.
        """
        super().__init__(name, True)
        self.title = title

    def calculate_move(self, options:list, table:dict) -> int:
        """pick move from `options` based on `table`, then returns the index."""
        return 0
    

class Randy(Game_AI):
    """picks a random move and ingores the table setup."""

    def __init__(self):
        super().__init__("Randy", "The Random")

    def calculate_move(self, options, table):
        move = random.randint(0, len(options)-1)
        return move
