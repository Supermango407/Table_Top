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
from collider import CircleCollider


class CheckersPiece(Piece):
    """a piece for `Checkers` game."""

    def __init__(self, player:int, tile):
        
        super().__init__(
            tile=tile,
            color=checkers_settings.piece_colors[player],
            collider_type=CircleCollider,
            onlick=self.click_test
        )
        self.player = player

    def place_on_board(self, board):
        super().place_on_board(board)
        self.collider.radius = self.raduis

    # def set_position(self, position):
    #     super().set_position(position)
    #     self.collider.position = position

    # def destroy(self):
    #     self.collider.destroy()
    #     return super().destroy()

    def click_test(self):
        print(self)
        self.destroy()
    
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
        # CircleCollider(Vector2(100, 100), 50, onclick=self.click_test, show=True)
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

    def click_test(self):
        print(self)

