import pygame
from pygame import Vector2
from typing import Union
from window import GameObject, Sprite, Text
from player import Player


class Game(Sprite):
    """the Table_Top games class."""

    def __init__(self, *players:tuple[Player]):
        """
        `players`: the players playing
        """

        self.players = players

        self.turn = -1
        self.table = None
        self.history = ""
        """the current set up of the game."""

        # `turn_text`: text of the player whose turn it is
        self.turn_text = Text(
            self.players[0].name,
            anchor='top',
            position=Vector2(GameObject.window.get_width()//2, 16),
            color=(255, 255, 255)
        )
        
        self.game_running = True
        
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
            self.turn = (self.turn+1)%len(self.players)
            self.set_moves()
            self.turn_text.set_text(self.players[self.turn].name)
            
            if self.players[self.turn].is_ai:
                if len(self.moves) > 0:
                    self.play_move(self.moves[self.players[self.turn].calculate_move(self.moves, self.table)])
        else:
            if type(winner) == int:
                print(f"Player {winner+1} is the winner!")
            
            self.end_game()

    def play_move(self, move=None):
        """plays `move` by player whos turn it is.
        then goes to the next player's turn."""
        self.next_turn()
        print(move)
        self.record_move(move)
        
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

    def end_game(self):
        """ends the game, and returns to menu."""
        self.game_running = False
        print(self.history)

