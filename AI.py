import random
from player import Player


class Game_AI(Player):
    """the parent class ai for Table_Top"""
    
    def __init__(self, name:str, title:str, data:tuple[str]):
        """
        `name`: the name of the ai.
        `title`: the title of the ai, normaly formated as The _.
        `data`: information about the specific ai for `record_name`.
        """
        super().__init__(name, True)

        self.title = title
        self.data = data

        # the name that will be saved in database.
        self.record_name = f"{name}({','.join(data)})"

    def calculate_move(self, options:list, table:dict) -> int:
        """pick move from `options` based on `table`, then returns the index."""
        return 0


class Randy(Game_AI):
    """picks a random move and ingores the table setup."""

    def __init__(self, seed=None):
        if seed == None:
            self.seed = random.randint(0, 1000000000)
        else:
            self.seed = seed

        self.generator = random.Random(self.seed)
        super().__init__(f"RANDY", "The Random", (str(self.seed),))

    def calculate_move(self, options, table):
        move = self.generator.randint(0, len(options)-1)
        return move

