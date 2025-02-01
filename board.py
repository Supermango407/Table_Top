import pygame
from pygame import Vector2
from typing import Union
from window import GameObject, Sprite


class Board(Sprite):
    def __init__(self, anchor:str='center', offset:pygame.Vector2=Vector2(0, 0), tile_count:tuple[int, int]=(8, 8), tile_size:int=64, tile_colors:Union[tuple[int, int, int], tuple[tuple[int, int, int]]]=((255, 255, 255), (0, 0, 0)), tile_border_width:int=0, tile_border_color:tuple[int, int, int]=None):
        """
        `anchor`: where the board is placed on the screen eg:
            top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right.
        `offset`: added offset to `position`
        `tile_count`: the number of tiles in the format (x, y)
        `tile_size`: the size of tiles
        `tile_colors`: the color of the tiles
            if two colors are given colors will be used in checkered pattern
        `tile_border_width`: the width of the border between tiles
        `tile_border_color`: the color of the border between tiles
            if no color give will default to be an offset of the first index of `tile_colors`
        """
        self.anchor = anchor
        self.offset = offset
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

        # set the board width and height
        self.board_width = self.tile_count[0]*self.tile_size + self.tile_border_width*(self.tile_count[0]-1)
        self.board_height = self.tile_count[1]*self.tile_size + self.tile_border_width*(self.tile_count[1]-1)
        
        self.position = Vector2(0, 0)
        self.set_position()
        self.tile_spacing = self.tile_size+self.tile_border_width
        """the spaceing between adjecent tiles"""

        super().__init__()

    def set_position(self):
        # set `x` base on `self.anchor` and `self.offset`
        if 'left' in self.anchor:
            x = self.offset.x
        elif 'right' in self.anchor:
            x = self.offset.x+self.window.get_width()-self.board_width
        else:
            x = self.offset.x+self.window.get_width()//2-self.board_width//2
            
        # set `y` base on `self.anchor`
        if 'top' in self.anchor:
            y = self.offset.y
        elif 'bottom' in self.anchor:
            y = self.offset.y+self.window.get_height()-self.board_height
        else:
            y = self.offset.y+self.window.get_height()//2-self.board_height//2
        
        self.position = Vector2(x, y)

    def draw(self) -> None:
        # TODO fix misaligned border
        """the size of the tiles including the boarder"""

        # draw a rect with the scale and color of the board
        pygame.draw.rect(self.window, self.tile_colors[0], (self.position.x, self.position.y, self.board_width, self.board_height))

        # add checkered pattern if there is than more one color
        if len(self.tile_colors) > 1:
            for x in range(self.tile_count[0]):
                for y in range(self.tile_count[1]):
                    if (x+y) % 2 == 0:
                        pygame.draw.rect(self.window, self.tile_colors[1], (self.position.x + x*self.tile_spacing, self.position.y + y*self.tile_spacing, self.tile_size, self.tile_size))

        # draw border if it exsist
        if self.tile_border_width != 0:
            x_pos_on = self.tile_size+self.position.x
            """the next vertical line drawn's x pos"""
            for _ in range(1, self.tile_count[0]):
                pygame.draw.rect(self.window, self.tile_border_color, (x_pos_on, self.position.y, self.tile_border_width, self.board_height))
                x_pos_on += self.tile_spacing

            y_pos_on = self.tile_size+self.position.y
            """the next horizantal line drawn's y pos"""
            for _ in range(1, self.tile_count[1]):
                pygame.draw.rect(self.window, self.tile_border_color, (self.position.x, y_pos_on, self.board_width, self.tile_border_width))
                y_pos_on += self.tile_spacing

    def get_tile_at(self, position:Vector2) -> Vector2:
        """returns index of tile at `positions` if it exists"""
        position -= self.position

        # return None of not over board
        if min(position) < 0 or position.x > self.board_width or position.y > self.board_height:
            return None

        # reutrn None if on border
        if self.tile_border_width > 0 and (position.x%self.tile_spacing > self.tile_size or position.y%self.tile_spacing > self.tile_size):
            return None
        
        return position//self.tile_spacing

    def get_all_tiles(self) -> list[Vector2]:
        """generator that reutrns a list with all tile locations in it."""
        tiles = []
        for x in range(self.tile_count[0]):
            for y in range(self.tile_count[1]):
                tiles.append(Vector2(x, y))
        return tiles

    def get_global_position(self, position:Vector2) -> Vector2:
        """returns the global postion of `position`"""
        return self.position + Vector2(1, 1)*self.tile_size//2 + position*self.tile_spacing
    
    def get_tile_index(self, position:Vector2) -> int:
        """returns what number `position` is
        when look through the tiles left to right, then up to down"""
        return int(position.y*self.tile_count[0] + position.x)

    def get_tile_from_index(self, index:int):
        """returns the local postion of tile at `index`"""
        x = index%self.tile_count[0]
        y = (index-x)//self.tile_count[0]
        return Vector2(x, y)

