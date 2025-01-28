import pygame
from typing import Union

class Game(object):
    """the table top games class."""

    def __init__(self, window:pygame.Surface, name: str, players: Union[int, tuple[int]]=2):
        """
        `window`: the window the game is displayed on
        `name`: the name of the game
        `players`: the number of players the game is for
            use tupple if there are multiple options
        """
        self.window = window
        self.name = name

        # set the `players` to tuple if only one value is given
        # else just set it to the `players` argument
        if type(players) == int:
            self.players = (players,)
        else:
            self.players = players

    def start(self) -> None:
        pass

    def update(self) -> None:
        self.draw()
    
    def draw(self) -> None:
        pass
