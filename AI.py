import random


class Game_AI(object):
    """the parent class ai for Table_Top"""
    nickname = ""
    
    def calculate_move(self, options:list, table:dict) -> int:
        """pick move from `options` based on `table`, then returns the index."""
        return 0
    

class Randy(Game_AI):
    """picks a random move and ingores the table setup."""
    nickname = "The Random"

    def calculate_move(self, options, table):
        return random.randint(len(options))
    