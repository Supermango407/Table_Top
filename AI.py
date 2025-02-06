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

    def calculate_move(self, options:list, table) -> int:
        """pick move from `options` for `game`, then returns the index."""
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
        move = self.generator.choice(range(len(options)))
        return move


class Immanuel(Game_AI):
    """does whatever move looks best in the moment, without thinking about the future."""

    def __init__(self, seed=None):
        if seed == None:
            self.seed = random.randint(0, 1000000000)
        else:
            self.seed = seed

        self.generator = random.Random(self.seed)
        super().__init__(f"IMMANUEL", "The Impulsive", (str(self.seed),))

    def calculate_move(self, options, table):
        print('no game selected')

