import pygame
from pygame import Vector2
from typing import Union
from window import GameObject, Sprite, Text


class Game(Sprite):
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

        # `turn_text`: text of the player whose turn it is
        self.turn_text = Text('Player 1', anchor='top', position=Vector2(GameObject.window.get_width()//2, 16))
        
        super().__init__()

    def draw(self):
        self.turn_text.draw()

    def check_events(self, event) -> None:
        """checks for inputs eg: key press, mouse clicks, ect."""
        pass

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

    def get_moves(self) -> list:
        """reutrns a list with all valid moves."""
        return []

    def valid_move(self) -> bool:
        """returns true if the move is a valid move, else returns false"""
        return True

