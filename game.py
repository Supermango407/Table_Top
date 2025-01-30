import pygame
from typing import Union
from window import GameObject


class Game(GameObject):
    """the table top games class."""

    def __init__(self,name:str, players:int=2):
        """
        `name`: the name of the game
        `players`: the number of players playing
        """

        self.name = name
        self.players = players

        self.turn = 0
        self.table = None
        """the current set up of the game."""

        super().__init__()

    def next_turn(self) -> None:
        """check winner and if there's none move to the next player."""
        winner = self.get_winner()
        if winner == None:
            self.turn = (self.turn+1)%self.players

    def get_winner(self) -> Union[None, int, str]:
        """returns None if no one has won yet,
        an int if a player wins,
        and 'tie' if its a tie"""
        return None

    def check_events(self, event) -> None:
        """checks for inputs eg: key press, mouse clicks, ect."""
        pass

