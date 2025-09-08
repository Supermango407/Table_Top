from __future__ import annotations
import pygame
from pygame import Vector2
from typing import Union
from dataclasses import dataclass
from game import Game
from collections.abc import Callable
from window import GameObject, Sprite
from collider import Collider


class Board(Sprite):
    
    def __init__(self, game_ref:Game, position:Vector2=Vector2(0, 0), anchor:str='center', tile_count:tuple[int, int]=(8, 8), tile_size:int=64, tile_colors:Union[tuple[int, int, int], tuple[tuple[int, int, int]]]=((255, 255, 255), (0, 0, 0)), tile_border_width:int=0, tile_border_color:tuple[int, int, int]=None, parrent:Sprite=None, check_events:bool=False):
        """
        `position`: the location of the sprite onscreen.
        `anchor`: where the board is placed on the screen eg:
            top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right.
        `game_ref`: a reference to the game the board is apart of.
        `tile_count`: the number of tiles in the format (x, y)
        `tile_size`: the size of tiles
        `tile_colors`: the color of the tiles
            if two colors are given colors will be used in checkered pattern
        `tile_border_width`: the width of the border between tiles
        `tile_border_color`: the color of the border between tiles
            if no color give will default to be an offset of the first index of `tile_colors`
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        `check_events`: if True will check events,
            eg: key_presses, mouse clicks ect.
        """
        self.game_ref = game_ref
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
            # if `tile_color` is a darker, set `tile_border_color` to a lighter hue
            # else `tile_border_color` to a darker hue
            if max(tile_color) <= 127:
                # set each of the rgb values to an average of it value and 255
                color = [(i+255)//2 for i in tile_color]
            else:
                # set each of the rgb values to an average of it value and 0 (same as halfing the value)
                color = [i//2 for i in tile_color]
            self.tile_border_color = color
        else:
            self.tile_border_color = tile_border_color

        self.pieces:dict[Piece] = dict()

        # set the board width and height
        self.board_width = self.tile_count[0]*self.tile_size + self.tile_border_width*(self.tile_count[0]-1)
        self.board_height = self.tile_count[1]*self.tile_size + self.tile_border_width*(self.tile_count[1]-1)
        
        self.tile_spacing = self.tile_size+self.tile_border_width
        """the spaceing between adjecent tiles"""

        super().__init__(local_position=position, anchor=anchor, parrent=parrent, check_events=check_events)

    def clear_board(self):
        """deletes all pieces on the board."""
        for piece in self.pieces:
            self.pieces[piece].destroy()
        self.pieces = dict()

    def draw(self) -> None:
        """the size of the tiles including the boarder"""

        # draw a rect with the scale and color of the board
        pygame.draw.rect(self.window, self.tile_colors[0], (self.global_position.x, self.global_position.y, self.board_width, self.board_height))

        # add checkered pattern if there is than more one color
        if len(self.tile_colors) > 1:
            for x in range(self.tile_count[0]):
                for y in range(self.tile_count[1]):
                    if (x+y) % 2 == 0:
                        pygame.draw.rect(self.window, self.tile_colors[1], (self.global_position.x + x*self.tile_spacing, self.global_position.y + y*self.tile_spacing, self.tile_size, self.tile_size))

        # draw border if it exsist
        if self.tile_border_width != 0:
            x_pos_on = self.tile_size+self.global_position.x
            """the next vertical line drawn's x pos"""
            
            for _ in range(1, self.tile_count[0]):
                pygame.draw.rect(self.window, self.tile_border_color, (x_pos_on, self.global_position.y, self.tile_border_width, self.board_height))
                x_pos_on += self.tile_spacing

            y_pos_on = self.tile_size+self.global_position.y
            """the next horizantal line drawn's y pos"""
            
            for _ in range(1, self.tile_count[1]):
                pygame.draw.rect(self.window, self.tile_border_color, (self.global_position.x, y_pos_on, self.board_width, self.tile_border_width))
                y_pos_on += self.tile_spacing

        super().draw()

    def get_width(self):
        return self.board_width
    
    def get_height(self):
        return self.board_height

    def tile_on_board(self, tile:Vector2) -> bool:
        """return true if `tile` is in on the board."""
        # if x is outside the board, return False.
        if tile.x < 0 or tile.x > self.tile_count[0]-1:
            return False
        
        # if y is outside the board, return False.
        if tile.y < 0 or tile.y > self.tile_count[1]-1:
            return False
            
        # else return True
        return True

    def place_piece(self, tile:Vector2, piece:Piece=None, piece_color:tuple[int, int, int]=(127, 127, 127)) -> bool:
        """places `piece` on `tile` if `tile` is empty.
            if `piece` is left None it will create a new Piece with `color`.
            returns True if successful, else returns False."""
        tile_index = self.get_tile_index(tile)

        # if there's' alread a piece there, return False
        # else place Peice and return True
        if self.pieces.get(tile_index):
            return False
        
        if piece == None:
            self.pieces[tile_index] = Piece(tile, self, piece_color)
        else:
            piece.place_on_board(self)
            self.pieces[tile_index] = piece

        return True

    def get_piece_on(self, tile:Vector2) -> Piece:
        """returns piece on `tile` if it exsits, else returns None."""
        return self.pieces.get(self.get_tile_index(tile))

    def get_tile_at(self, position:Vector2) -> Vector2:
        """returns tile at global `position` if it exists"""
        position -= self.global_position

        # return None of not over board
        if min(position) < 0 or position.x > self.board_width or position.y > self.board_height:
            return None

        # reutrn None if on border
        if self.tile_border_width > 0 and (position.x%self.tile_spacing > self.tile_size or position.y%self.tile_spacing > self.tile_size):
            return None
        
        return position//self.tile_spacing

    def get_all_tiles(self) -> list[Vector2]:
        # TODO: make this function a generator?
        """reutrns a list with all tiles in it."""
        tiles = []
        for x in range(self.tile_count[0]):
            for y in range(self.tile_count[1]):
                tiles.append(Vector2(x, y))
        return tiles

    def get_tile_position(self, tile:Vector2) -> Vector2:
        """returns the global position of `tile`, relitive to the board."""
        return Vector2(1, 1)*self.tile_size//2 + tile*self.tile_spacing
    
    def get_tile_index(self, tile:Vector2) -> int:
        """returns what number `tile` is
        when going through the tiles left to right, then up to down
        like scaning, or reading."""
        return int(tile.y*self.tile_count[0] + tile.x)

    def get_tile_from_index(self, index:int) -> Vector2:
        """returns the tile at `index`"""
        x = index%self.tile_count[0]
        y = (index-x)//self.tile_count[0]
        return Vector2(x, y)


class Piece(Sprite):
    """sprites that can be placed on boards, but only one per tile."""

    def __init__(self, tile:Vector2, color:tuple[int, int, int], outline_color:tuple[int, int, int]=None, outline_thickness:int=1, hidden=False, parrent:Sprite=None, check_events:bool=False):
        """
        `tile`: where on board piece is placed.
        `color`: the color of the piece.
        `outline_color`: the color of the piece's outline.
            if left None there wont be an outline.
        `outline_thickness`: the thickness of the piece's outline.
            if `outline_color` is None it wont matter.
        `hidden`: if true, sprite will not be drawn to screen.
        `parrent`: what object the sprite is placed relitive to.
            defaults to Window.
            if not None the sprite wont be drawn, so it can be drawn in the parrents script.
        `check_events`: if True will check events,
            eg: key_presses, mouse clicks ect.
        """
        self.tile = tile
        self.color = color
        self.outline_color = outline_color
        self.outline_thickness = outline_thickness
        self.board = None

        # position will be set when piece is placed but it needs a place holder.
        # uses Sprite.__init__ instead of super().__init__ because
        # super doesn't work with Active Piece double inheritance.
        Sprite.__init__(self, local_position=Vector2(0, 0), hidden=hidden, parrent=parrent, check_events=check_events)

    def place_on_board(self, board:Board):
        """called when this piece is placed on a board."""
        self.board = board
        self.board.add_child(self)
        self.raduis = self.board.tile_size*0.4
        self.set_position(self.board.get_tile_position(self.tile))
        
    def draw(self):
        if self.board != None:
            # draw piece
            pygame.draw.circle(
                GameObject.window,
                self.color,
                self.global_position,
                self.raduis,
            )

            # draw outline if it exsitst
            if self.outline_color != None:
                pygame.draw.circle(
                    GameObject.window,
                    self.outline_color,
                    self.global_position,
                    self.raduis,
                    self.outline_thickness,
                )
        super().draw()

    def destroy(self):
        del(self.board.pieces[self.board.get_tile_index(self.tile)])
        super().destroy()


# class ActiveBoard(Board):

#     def __init__(self, game_ref:Game, position:Vector2=Vector2(0, 0), anchor:str='center', tile_count=(8, 8), tile_size=64, tile_colors=((255, 255, 255), (0, 0, 0)), tile_border_width=0, tile_border_color=None, move_color:tuple[int, int, int]=(127, 0, 255), parrent:Sprite=None):
#         """
#         `position`: the location of the sprite onscreen.
#         `anchor`: where the board is placed on the screen eg:
#             top_left, top, top_right, left, center, right, bottom_left, bottom, bottom_right.
#         `game_ref`: a reference to the game the board is apart of.
#         `tile_count`: the number of tiles in the format (x, y)
#         `tile_size`: the size of tiles
#         `tile_colors`: the color of the tiles
#             if two colors are given colors will be used in checkered pattern
#         `tile_border_width`: the width of the border between tiles
#         `tile_border_color`: the color of the border between tiles
#             if no color give will default to be an offset of the first index of `tile_colors`
#         `move_color`: the color of the avalible move dots.
#         `parrent`: what object the sprite is placed relitive to.
#             defaults to Window.
#             if not None the sprite wont be drawn, so it can be drawn in the parrents script.
#         """
#         super().__init__(game_ref=game_ref, position=position, anchor=anchor, tile_count=tile_count, tile_size=tile_size, tile_colors=tile_colors, tile_border_width=tile_border_width, tile_border_color=tile_border_color, check_events=True)
#         self.move_color = move_color

#         # piece selected keeps track of last piece click
#         # for games with active pieces (like chess and checkers).
#         # it normaly shows the valid moves for said piece.
#         self.piece_selected:ActivePiece = None
    
#     def check_event(self, event):
#         if event.type == pygame.MOUSEBUTTONUP:
#             self.deselect()

#     def deselect(self) -> None:
#         """deselects selected piece if one exsists."""
#         if self.piece_selected != None:
#             self.piece_selected.deselect()
#             self.piece_selected = None


# class ActivePiece(Piece):
#     """a Piece that has moves, and can usally be dragged around."""

#     def __init__(self, tile:Vector2, color:tuple[int, int, int], collider:Collider, selected_outline_color:tuple[int,int,int]=(255, 255, 63), outline_color:tuple[int, int, int]=(None), outline_thickness:int=1, locked:bool=False, show_collider:bool=False, hidden=False, parrent:Sprite=None):
#         """
#         `tile`: where on board piece is placed.
#         `color`: the color of the piece.
#         `collider`: the collider of the sprite.
#         `selected_outline_color`: the oultile color of the sprite when selected.
#         `outline_color`: the color of the piece's outline.
#             if left None there wont be an outline.
#         `outline_thickness`: the thickness of the piece's outline.
#             if `outline_color` is None it wont matter.
#         `locked`: if true, piece isn't selectable.
#         `show_collider`: if true will display the collider
#         `hidden`: if true, sprite will not be drawn to screen.
#         `parrent`: what object the sprite is placed relitive to.
#             defaults to Window.
#             if not None the sprite wont be drawn, so it can be drawn in the parrents script.
#         """
        
#         super().__init__(
#             self,
#             tile=tile,
#             color=color,
#             outline_color=outline_color,
#             outline_thickness=outline_thickness,
#             hidden=hidden,
#             parrent=parrent
#         )
        
#         self.board:ActiveBoard = None
#         self.selected_outline_color = selected_outline_color

#         # the color of the pieces outline when not selected
#         self.main_outline_color = outline_color

#         # if this piece is currently selected by board.
#         self.selected = False

#     def draw(self):
#         super().draw()

#         # if piece selected show valid move dots
#         if self.selected:
#             tile_moves = self.get_tile_moves()
#             for tile_move in tile_moves:
#                 pygame.draw.circle(
#                     self.window,
#                     self.board.move_color,
#                     self.board.get_tile_position(tile_move.tile),
#                     self.board.tile_size//8
#                 )

#     def move_piece(self, tile:Vector2) -> None:
#         """moves self to a tile on `board`."""
#         # update board pieces list
#         del(self.board.pieces[self.board.get_tile_index(self.tile)])
#         self.board.pieces[self.board.get_tile_index(tile)] = self
        
#         self.tile = tile
#         self.set_position(self.board.get_tile_position(tile))
#         self.board.deselect()

#     def select(self) -> None:
#         """sets `self` as selected piece."""
#         # cant select if piece is locked
#         if self.locked:
#             return
        
#         self.board.piece_selected = self
#         self.outline_color = self.selected_outline_color
#         self.selected = True

#     def deselect(self):
#         """deselects self and removes it from boards selected."""
#         self.selected = False
#         self.board.piece_selected = None
#         self.outline_color = self.main_outline_color

#     def get_tile_moves(self) -> list[PieceMove]:
#         """gets a list of tiles the piece can move to."""
#         return []

#     def onlifted(self, sprite_start, sprite_end):
#         super().onlifted(sprite_start, sprite_end)
#         if self.board.get_tile_at(sprite_start.copy()) == self.board.get_tile_at(sprite_end.copy()):
#             self.set_position(sprite_start.copy())
#             self.select()
#         else:
#             tile_over = self.board.get_tile_at(sprite_end)
#             if tile_over != None:
#                 # check to see if piece is over a valid tile
#                 for move in self.get_tile_moves():
#                     if move.tile == tile_over:
#                         self.board.game_ref.play_move(move=move)
#                         break
#                 # if not a valid tile, move back to starting spot
#                 else:
#                     self.set_position(sprite_start.copy())

