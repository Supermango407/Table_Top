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
from board import Board, ActivePiece
import collider


class TestSprite(collider.DraggableSprite):
    def __init__(self, position):
        super().__init__(position, collider=collider.CircleCollider(Vector2(0, 0),  50), show_collider=True)

    def test(self):
        print('test')

    def onlifted(self, started, ended):
        super().onlifted(started, ended)
        self.set_position(ended)
        self.test()
    
    def draw(self):
        pygame.draw.circle(self.window, (0, 0, 255), self.position, 50)
        super().draw()


class CheckersPiece(ActivePiece):
    """a piece for `Checkers` game."""

    def __init__(self, player:int, tile, is_king=False):
        
        super().__init__(
            tile=tile,
            color=checkers_settings.piece_colors[player],
            collider=collider.CircleCollider(
                position=Vector2(0, 0),
                radius=0, # radiues will be when piece is placed on board.
            ),
            show_collider=True
        )
        self.player = player
        self.is_king = is_king

    def place_on_board(self, board):
        super().place_on_board(board)
        self.collider.radius = self.raduis

    def get_moves(self):
        """gets valid moves for piece."""
        moves = []
        # add the moves up the board if your player 1 or if your a king
        if self.player == 0 or self.is_king:
            moves.extend([
                self.tile + Vector2(-1, -1),
                self.tile + Vector2(1, -1)
            ])

        # add the moves down the board if your player 2 or if your a king
        if self.player == 1 or self.is_king:
            moves.extend([
                self.tile + Vector2(-1, 1),
                self.tile + Vector2(1, 1)
            ])
        
        return moves

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
        # TestSprite(Vector2(100, 100))
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

