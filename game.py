import pygame
from pygame import Vector2
from typing import Union
import data
from window import GameObject, Sprite, Text
from player import Player


class Game(Sprite):
    """the Table_Top games class."""

    def __init__(self, name:str, *players:tuple[Player]):
        """
        `name`: the name of the game.
        `players`: the players playing.
        """

        self.name = name
        self.players = players

        self.turn = -1
        self.table = None
        self.display_game = True
        # the current set up of the game
        self.history = ""

        # `turn_text`: text of the player whose turn it is
        if GameObject.window != None:
            self.turn_text = Text(
                self.players[0].name,
                anchor='top',
                position=Vector2(GameObject.window.get_width()//2, 16),
                color=(255, 255, 255)
            )
        
        self.game_running = False
        
        super().__init__()

    def start_game(self, display_game=True):
        self.display_game = display_game
        self.game_running = True
        self.turn = -1
        self.history = ''
        self.next_turn()

    def draw(self):
        if self.display_game:
            self.turn_text.draw()

    def check_events(self, event) -> None:
        """checks for inputs eg: key press, mouse clicks, ect."""
        pass

    def next_turn(self) -> None:
        """move to the next player."""
        self.turn = (self.turn+1)%len(self.players)
        self.set_moves()
        self.turn_text.set_text(self.players[self.turn].name)
        
    def play_move(self, move=None):
        """plays `move` by player whos turn it is.
        then checks to see if the game ended
        if not, goes to the next player's turn."""
        self.record_move(move)
        
        winner = self.get_winner()
        if winner == None:
            self.next_turn()
        else:
            self.end_game(winner)
        
    def record_move(self, move=None) -> None:
        """saves the `move` to history."""
        pass

    def get_winner(self) -> Union[None, int, str]:
        """returns None if no one has won yet,
        an int if a player wins,
        and 'tie' if its a tie"""
        return None

    def set_moves(self) -> list:
        """sets `moves` to a list with all valid moves."""
        self.moves = []

    def valid_move(self) -> bool:
        """returns true if the move is a valid move, else returns false"""
        return True

    def end_game(self, winner:str) -> None:
        """ends the game, and returns to menu."""
        if type(winner) == int:
            self.turn_text.set_text(self.players[winner].name)
            print(f"Player {winner+1} is the winner!")
        else:
            self.turn_text.set_text("Tie")
            print('its a ', winner)
        
        self.game_running = False
        data.save_record(self.name, self.players, winner, self.history)
        # print('-'*80)
        # print(self.history)
        # print('-'*80)

    def show_record(self, record:str) -> None:
        """showes what the board looks like if `record` it played."""
        pass

    def show_game(self, record:str) -> None:
        """shows `record` of game played one move at a time."""
        pass

