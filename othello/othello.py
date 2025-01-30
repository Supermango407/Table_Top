import pygame
from pygame import Vector2
from typing import Union
import os
import sys
sys.path.append('../table_top')
import othello.game_settings as game_settings
from game import Game
from board import Board, TilePosition
from window import GameObject, Sprite


class Othello(Game):
    
    def __init__(self):
        super().__init__('Othello')
        self.board = Board(
            tile_size=game_settings.board['tile_size'],
            tile_border_width=game_settings.board['border_width'],
            tile_colors=game_settings.board['baground_color'],
            tile_border_color=game_settings.board['border_color']
        )

        self.table = [
            Piece(0, Vector2(3, 3)),
            Piece(1, Vector2(3, 4)),
            Piece(1, Vector2(4, 3)),
            Piece(0, Vector2(4, 4)),
        ]

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            tile_pos = self.board.get_tile_at(pygame.mouse.get_pos())
            if tile_pos != None:
                if event.button == 1:
                    Piece(0, tile_pos)
                elif event.button == 3:
                    Piece(1, tile_pos)


class Piece(Sprite):
    childeren = []

    def __init__(self, player:int, position:Union[Vector2, TilePosition]):
        """
        `player`: the player who controls the piece.
        `position`: the position on the board the peice is on.
        """
        self.player = player

        if type(position) == Vector2:
            self.position = TilePosition(position)
        else:
            self.position = position

        self.childeren.append(self)
        super().__init__()

    def update(self) -> None:
        """called once per frame"""
        self.draw()

    def draw(self) -> None:
        pygame.draw.circle(
            self.window,
            game_settings.piece_colors[self.player],
            self.position.get_global_position(),
            game_settings.piece_size
        )
