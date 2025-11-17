import pygame
import spmg
from spmg_pygame.gameobject import Gameobject
# from spmg import ui
from pygame import Vector2
from typing import Union
from dataclasses import dataclass
import data
from player import Player


@dataclass
class GameVars(object):
    """dataclase of the game varables.
        `name`: the name of the game.
        `players`: how many players can play this game.
            use int if there only one option.
            use tuple if there are multiple options.
    """
    name:str
    """the name of the Game"""
    players:Union[int, tuple[int]]
    """the number of players that can play the game"""
    # TODO: add image var


@dataclass
class GameTable(object):
    """dataclass with basic Game vars"""
    turn:int
    """who's turn it is"""
    # TODO: add timer


@dataclass
class GameMove(object):
    player:int
    """the index of whos turn it is."""


class Game(spmg.Gameobject):
    """the Table_Top games class."""
    game_vars:GameVars = GameVars("GAME_PARENT_CLASS", 0)

    def __init__(self, display_game:bool=True):
        self.players = []
        self.save_record = False
        self.display_game = display_game # TODO: implement fully. GameObject.window != None
        """if True the game will be shown on the screen,
        else it will be hidden, for processing."""

        if not hasattr(self, "table"):
            self.table:GameTable = GameTable(turn=-1)
            """the current set up of the game"""

        self.history = ""
        """record of moves played"""

        self.game_running = False
        """if in middle of game or not"""
        
        super().__init__(listen=True)

        # `turn_text`: text of the player whose turn it is
        if self.display_game:
            self.turn_text = spmg.ui.Text(
                value="",
                position=Vector2(0, 16),
                anchor=Vector2(0.5, 0),
                relative_position=Vector2(0.5, 0),
                bg_color=(255, 255, 255),
                # parent=self
            )
        
    def start_game(self, *players:tuple[Player], save_record=False):
        """starts new game."""
        self.game_running = True
        self.players = players
        self.table.turn = -1
        self.save_record = save_record
        self.history = ''
        self.next_turn()

    def next_turn(self) -> None:
        """move to the next player."""
        self.table.turn = (self.table.turn+1)%len(self.players)
        self.set_moves()
        self.set_turn_text(self.table.turn)
        
    def play_move(self, move=None, auto_next_turn:bool=True) -> None:
        """
        plays `move` by player whos turn it is.
        then checks to see if the game ended
        if not, goes to the next player's turn.
            `auto_next_turn`: if set to False will not automaticly go to next turn.
        """
        self.record_move(move)
        
        winner = self.get_winner()
        if winner == None:
            if auto_next_turn:
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
        if self.display_game:
            self.turn_text.set_text(self.players[player].name)

    def valid_move(self, move=None) -> bool:
        """returns true if the move is a valid move, else returns false"""
        return True

    def set_winner_text(self, winner) -> None:
        """sets the turn_text, if it exsists, to the Winner of game."""
        if self.display_game:
            if type(winner) == int: # player wins
                self.turn_text.set_text(self.players[winner].name+" Wins")
            elif type(winner) == str: # tie
                self.turn_text.set_text(winner)

    def end_game(self, winner) -> None:
        """ends the game, and returns to menu."""
        self.set_winner_text(winner)
        self.game_running = False
        if self.save_record:
            data.save_record(self.game_vars.name, self.players, winner, self.history)
        
        if not self.display_game:
            self.destroy()
        
        # print('-'*80)
        # print(self.history)
        # print('-'*80)

    def show_record(self, players:list[Player], record:str) -> None:
        """shows what the end looks like if `record` is played."""
        pass

    def show_game(self, players:list[Player], record:str, time_between_moves:float=0.5) -> None:
        """shows `record` of game played one move at a time."""
        pass

