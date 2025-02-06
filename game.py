import pygame
from pygame import Vector2
from typing import Union
from dataclasses import dataclass
import data
from window import GameObject, Sprite, Text
from player import Player


@dataclass
class Game_Table(object):
    """class with basic Game vars"""
    turn:int


class Game(Sprite):
    """the Table_Top games class."""

    def __init__(self, name:str, *players:tuple[Player], save_record=False):
        """
        `name`: the name of the game.
        `players`: the players playing.
        `save_record`: if True will save game to Database.
        """

        self.name = name
        self.players = players
        self.save_record = save_record

        self.table:Game_Table = Game_Table(turn=-1)
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

    def start_game(self, save_record=False):
        self.game_running = True
        self.table.turn = -1
        self.save_record = save_record
        self.history = ''
        self.next_turn()

    def draw(self):
        self.turn_text.draw()

    def check_events(self, event) -> None:
        """checks for inputs eg: key press, mouse clicks, ect."""
        pass

    def next_turn(self) -> None:
        """move to the next player."""
        self.table.turn = (self.table.turn+1)%len(self.players)
        self.set_moves()
        self.set_turn_text(self.table.turn)
        
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

    def set_turn_text(self, player:int) -> None:
        """set the text, of turn text, if it exsists, to the `player`s name."""
        if GameObject.window != None:
            self.turn_text.set_text(self.players[player].name)

    def valid_move(self) -> bool:
        """returns true if the move is a valid move, else returns false"""
        return True

    def set_winner_text(self, winner) -> None:
        """sets the turn_text, if it exsists, to the Winner of game."""
        if GameObject.window != None:
            if type(winner) == int:
                self.turn_text.set_text(self.players[winner].name)
            elif type(winner) == str:
                self.turn_text.set_text(winner)

    def end_game(self, winner) -> None:
        """ends the game, and returns to menu."""
        self.set_winner_text(winner)
        self.game_running = False
        if self.save_record:
            data.save_record(self.name, self.players, winner, self.history)
        
        if GameObject.window == None:
            self.destroy()
        # print('-'*80)
        # print(self.history)
        # print('-'*80)

    def show_record(self, players:list[Player], record:str) -> None:
        """showes what the board looks like if `record` it played."""
        pass

    def show_game(self, players:list[Player], record:str) -> None:
        """shows `record` of game played one move at a time."""
        pass

