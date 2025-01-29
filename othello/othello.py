import pygame
from pygame import Vector2
import os
import sys
sys.path.append('../table_top')
import othello.game_settings as game_settings
from game import Game
from board import Board


class Othello(Game):
    
    def __init__(self, window):
        super().__init__(window, 'Othello')
        self.board = Board(
            window,
            tile_size=game_settings.board['tile_size'],
            tile_border_width=game_settings.board['border_width'],
            tile_colors=game_settings.board['baground_color'],
            tile_border_color=game_settings.board['border_color']
        )
    
    def draw(self):
        self.board.draw()
