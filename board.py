import pygame
from typing import Union

class Board(object):

    def __init__(self, window:pygame.Surface, tile_count:tuple[int, int]=(8, 8), tile_size:int=64, tile_colors:Union[tuple[int, int, int], tuple[tuple[int, int, int]]]=((255, 255, 255), (0, 0, 0)), tile_border_width:int=0, tile_border_color:tuple[int, int, int]=None):
        """
        `window`: the window the board is drawn on
        `tile_count`: the number of tiles in the format (x, y)
        `tile_size`: the size of tiles
        `tile_colors`: the color of the tiles
            if two colors are given colors will be used in checkered pattern
        `tile_border_width`: the width of the border between tiles
        `tile_border_color`: the color of the border between tiles
            if no color give will default to be an offset of the first index of `tile_colors`
        """
        self.window = window
        self.tile_count = tile_count
        self.tile_size = tile_size
        self.tile_colors = tile_colors
        self.tile_border_width = tile_border_width

        # set the `tile_color` to tuple if only one value is given
        # else just set it to the `tile_colors` argument
        if type(tile_colors[0]) != tuple:
            self.tile_colors = (tile_colors,)
        else:
            self.tile_colors = tile_colors

        # if `tile_border_color` is none set it to an offset of first index of `tile_colors`
        if tile_border_color == None:
            tile_color:tuple[int, int, int] = self.tile_colors[0]
            # if `tile_color` is a darker, set `color` to a lighter hue
            # else `color` to a darker hue
            if max(tile_color) <= 127:
                # set each of the rgb values to an average of it value and 255
                color = [(i+255)//2 for i in tile_color]
            else:
                # set each of the rgb values to an average of it value and 0 (same as halfing the value)
                color = [i//2 for i in tile_color]
            self.tile_border_color = color
        else:
            self.tile_border_color = tile_border_color

    def draw(self) -> None:
        board_width = self.tile_count[0]*self.tile_size + self.tile_border_width*(self.tile_count[0]-1)
        board_height = self.tile_count[1]*self.tile_size + self.tile_border_width*(self.tile_count[1]-1)
        
        # draw a rect with the scale and color of the board
        pygame.draw.rect(self.window, self.tile_colors[0], (0, 0, board_width, board_height))

        # draw border if it exsist
        if self.tile_border_width != 0:
            x_pos_on = self.tile_size
            """the next vertical line drawn's x pos"""
            for _ in range(1, self.tile_count[0]):
                pygame.draw.line(self.window, self.tile_border_color, (x_pos_on, 0), (x_pos_on, board_height), self.tile_border_width)
                x_pos_on += self.tile_size+self.tile_border_width

            y_pos_on = self.tile_size
            """the next horizantal line drawn's y pos"""
            for _ in range(1, self.tile_count[1]):
                pygame.draw.line(self.window, self.tile_border_color, (0, y_pos_on), (board_width, y_pos_on), self.tile_border_width)
                y_pos_on += self.tile_size+self.tile_border_width

        # TODO: add checkered pattern
