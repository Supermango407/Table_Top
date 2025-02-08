import pygame
import threading
import time
from pygame import Vector2
from dataclasses import dataclass
import sys
sys.path.append('../table_top')
import checkers.checkers_settings as checkers_settings
from window import GameObject, Sprite
import ai as AI
from player import Player
from game import Game, Game_Table, GameVars
from board import Board, Piece


class CheckersPiece(Piece):
    """a piece for `Checkers` game."""

    def __init__(self, player:int, tile):
        self.player = player
        super().__init__(tile, None, checkers_settings.piece_colors[player])

    # TODO
    def king(self):
        """changes piece to a king."""
        pass


class Checkers(Game):
    game_vars = GameVars('Checkers', 2)

    def __init__(self):
        super().__init__()
        self.board = Board(
            tile_colors=checkers_settings.board['colors'],
            tile_size=checkers_settings.board['tile_size'],
        )
    
    def start_game(self, *players, save_record=False):
        self.set_board()
        return super().start_game(*players, save_record=save_record)

    def set_board(self):
        """puts the pieces in there starting position."""
        self.board.clear_board()
        
        self.place_piece(0, Vector2(0, 7))
        self.place_piece(0, Vector2(2, 7))
        self.place_piece(0, Vector2(4, 7))
        self.place_piece(0, Vector2(6, 7))
        self.place_piece(0, Vector2(1, 6))
        self.place_piece(0, Vector2(3, 6))
        self.place_piece(0, Vector2(5, 6))
        self.place_piece(0, Vector2(7, 6))
        self.place_piece(0, Vector2(0, 5))
        self.place_piece(0, Vector2(2, 5))
        self.place_piece(0, Vector2(4, 5))
        self.place_piece(0, Vector2(6, 5))

        self.place_piece(1, Vector2(1, 0))
        self.place_piece(1, Vector2(3, 0))
        self.place_piece(1, Vector2(5, 0))
        self.place_piece(1, Vector2(7, 0))
        self.place_piece(1, Vector2(0, 1))
        self.place_piece(1, Vector2(2, 1))
        self.place_piece(1, Vector2(4, 1))
        self.place_piece(1, Vector2(6, 1))
        self.place_piece(1, Vector2(1, 2))
        self.place_piece(1, Vector2(3, 2))
        self.place_piece(1, Vector2(5, 2))
        self.place_piece(1, Vector2(7, 2))

    def place_piece(self, player:int, tile:Vector2):
        """places piece on board at `tile`"""
        piece = CheckersPiece(player, tile)
        self.board.place_piece(tile, piece)

