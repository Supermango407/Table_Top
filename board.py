from __future__ import annotations
import pygame
from pygame import Vector2
from spmg_pygame.gameobject import Gameobject
from spmg_pygame.collider import Collider, CircleCollider
from spmg_pygame.draggable import draggable
from typing import Union, Type
from dataclasses import dataclass
from game import Game, GameTable, GameMove
from collections.abc import Callable
from collider import Collider


class Board(Gameobject):
    
    def __init__(self,
    game_ref:Game,
    tile_count:tuple[int, int]=(8, 8),
    tile_size:int=64,
    tile_colors:Union[tuple[int, int, int], tuple[tuple[int, int, int]]]=((255, 255, 255), (0, 0, 0)),
    tile_border_width:int=0,
    tile_border_color:tuple[int, int, int]=None,
    **kwargs
    ):
        self.game_ref = game_ref
        """a reference to the game the board is apart of"""
        self.tile_count = tile_count
        """the number of tiles in the format (x, y)"""
        self.tile_size = tile_size
        """the size of tiles"""
        self.tile_colors = tile_colors
        """the color of the tiles
        NOTE: use two colors for checkered pattern."""
        self.tile_border_width = tile_border_width
        """the width of the border between tiles"""

        # set the `tile_color` to tuple if only one value is given
        # else just set it to the `tile_colors` argument
        if type(tile_colors[0]) != tuple:
            self.tile_colors = (tile_colors,)
        else:
            self.tile_colors = tile_colors

        self.tile_border_color = None
        """the color of the border between tiles
        NOTE: if no color given, `tile_border_color` will
        default to be an offset of `tile_colors`[0]."""
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

        
        self.tile_spacing = self.tile_size+self.tile_border_width
        """the spaceing between adjecent tiles"""

        super().__init__(anchor=Vector2(0.5, 0.5), relative_position=Vector2(0.5, 0.5), **kwargs)

    def clear_board(self):
        """deletes all pieces on the board."""
        for piece in self.pieces:
            self.pieces[piece].destroy()
        self.pieces = dict()

    def draw(self) -> None:
        """the size of the tiles including the boarder"""
        # draw a rect with the scale and color of the board
        pygame.draw.rect(self.window, self.tile_colors[0], (self.window_position.x, self.window_position.y, self.size.x, self.size.y))

        # add checkered pattern if there is than more one color
        if len(self.tile_colors) > 1:
            for x in range(self.tile_count[0]):
                for y in range(self.tile_count[1]):
                    if (x+y) % 2 == 0:
                        pygame.draw.rect(self.window, self.tile_colors[1], (self.window_position.x + x*self.tile_spacing, self.window_position.y + y*self.tile_spacing, self.tile_size, self.tile_size))

        # draw border if it exsist
        if self.tile_border_width != 0:
            x_pos_on = self.tile_size+self.window_position.x
            """the next vertical line drawn's x pos"""
            
            for _ in range(1, self.tile_count[0]):
                pygame.draw.rect(self.window, self.tile_border_color, (x_pos_on, self.window_position.y, self.tile_border_width, self.size.y))
                x_pos_on += self.tile_spacing

            y_pos_on = self.tile_size+self.window_position.y
            """the next horizantal line drawn's y pos"""
            
            for _ in range(1, self.tile_count[1]):
                pygame.draw.rect(self.window, self.tile_border_color, (self.window_position.x, y_pos_on, self.size.x, self.tile_border_width))
                y_pos_on += self.tile_spacing

        super().draw()

    def set_size(self, new_size = None, set_children = True):
        if new_size == None:
            x = self.tile_count[0]*self.tile_size + self.tile_border_width*(self.tile_count[0]-1)
            y = self.tile_count[1]*self.tile_size + self.tile_border_width*(self.tile_count[1]-1)
            new_size = Vector2(x, y)
        
        super().set_size(new_size, set_children)

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

        # if there's' already a piece there, return False
        # else place Peice and return True
        if self.pieces.get(tile_index):
            return False
        
        if piece == None:
            self.pieces[tile_index] = Piece(tile, self, piece_color)
        else:
            piece.place_on_board(self, tile)
            self.pieces[tile_index] = piece

        return True

    def get_piece_on(self, tile:Vector2) -> Piece:
        """returns piece on `tile` if it exsits, else returns None."""
        return self.pieces.get(self.get_tile_index(tile))

    def get_tile_at(self, position:Vector2) -> Vector2:
        """returns tile at global `position` if it exists"""
        position -= self.window_position

        # return None of not over board
        if min(position) < 0 or position.x > self.size.x or position.y > self.size.y:
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

    def get_tile_global_position(self, tile:Vector2) -> Vector2:
        """returns the global position of `tile`, relitive to the board."""
        return Vector2(1, 1)*self.tile_size//2 + tile*self.tile_spacing + self.window_position
    
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


class Piece(Gameobject):
    """sprites that can be placed on boards, but only one per tile."""

    def __init__(self,
    color:tuple[int, int, int],
    outline_color:tuple[int, int, int]=None,
    outline_thickness:int=1,
    **kwargs
    ):
        self.color:tuple[int, int, int] = color
        """the color of the piece."""
        self.outline_color:tuple[int, int, int] = outline_color
        """the color of the piece's outline.
        if left None there wont be an outline."""
        self.outline_thickness:int = outline_thickness
        """the thickness of the piece's outline.
            if `outline_color` is None it wont matter."""
        self.board:Board = None
        """the board the piece is placed on."""
        self.tile:Vector2 = None
        """where on board piece is placed."""

        # position will be set when piece is placed but it needs a place holder.
        # uses Sprite.__init__ instead of super().__init__ because
        # super doesn't work with Active Piece double inheritance.
        Gameobject.__init__(self, position=Vector2(0, 0), **kwargs)

    def place_on_board(self, board:Board, tile:Vector2):
        """called when this piece is placed on a board."""
        self.board = board
        # self.board.place_piece(self, self.position)
        self.raduis = self.board.tile_size*0.4
        self.move_to_tile(tile)
        
    def move_to_tile(self, tile:Vector2):
        """move the piece to `tile`."""
        self.tile_on = tile
        self.set_position(self.board.get_tile_global_position(tile))

    def draw(self):
        if self.board != None:
            # draw piece
            pygame.draw.circle(
                Gameobject.window,
                self.color,
                self.global_position,
                self.raduis,
            )

            # draw outline if it exsitst
            if self.outline_color != None:
                pygame.draw.circle(
                    Gameobject.window,
                    self.outline_color,
                    self.global_position,
                    self.raduis,
                    self.outline_thickness,
                )
        super().draw()

    def destroy(self):
        del(self.board.pieces[self.board.get_tile_index(self.tile)])
        super().destroy()


# Active Games
# --------------------------------------------------------------------------------

@dataclass
class ActiveGameTable(GameTable):
    """base class of a table for ActiveBoardGames."""
    pieces:list[ActivePiece]
    """pieces on board."""


@dataclass
class ActiveGameMove(GameMove):
    piece:ActivePiece
    """the piece moving"""
    move_to:Vector2
    """tile moving to"""


@draggable
class ActivePiece(Piece):
    """a piece that can move for tile to tile."""

    def __init__(self, player:int, **kwargs):
        self.player:int = player
        """the index of thr player whos piece it is."""
        self.selected:bool = False
        """whether the piece is selected or not."""
        self.tile_on:Vector2 = None
        """the tile the piece is on."""
        super().__init__(**kwargs)

        if not hasattr(self, "collider"):
            self.collider:Collider = CircleCollider(
                radius=1,
                # hidden=False,
                parent=self
            )
            """the collider of the Piece."""

    def stopped_dragging(self, start:Vector2, end:Vector2):
        """called when piece is clicked."""
        print(start, end)

    def draw(self):
        if self.selected:
            pygame.draw.circle(self.window, "light gray", self.global_position, self.board.tile_size//2)

            for move in self.get_tile_moves():
                pygame.draw.circle(self.window, "light gray", self.board.get_tile_global_position(move.move_to), 10)
        return super().draw()

    def get_tile_moves(self) -> list[ActiveGameMove]:
        """gets a list of all tiles."""
        return []


class ActiveBoardGame(Game):
    """board game where the player moves the pieces."""

    def __init__(self, **kwargs):
        if not hasattr(self, "board"):
            self.board:Board = None
            """the board the game is played on."""
        if not hasattr(self, "piece_type"):
            self.piece_type:Type[ActivePiece] = ActivePiece
            """the type of `ActivePiece` the board game uses."""
        if not hasattr(self, "table"):
            self.table:ActivePiece = ActivePiece(turn=-1, pieces=[])
        
        self.piece_selected:ActivePiece = None
        """the current piece selected."""
        self.started_clicking_at:Vector2 = None
        """the position the mouse was clicked at
        when holding down the mouse button."""

        super().__init__(**kwargs)
    
    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.started_clicking_at = self.mouse_pos
        if event.type == pygame.MOUSEBUTTONUP:
            tile:Vector2 = self.board.get_tile_at(self.mouse_pos)
            """what tile the mouse is over."""
            start_tile:Vector2 = self.board.get_tile_at(self.started_clicking_at)
            """what tile the mouse was on when clicked."""
            if tile != None and start_tile != None:
                # only click if the mouse hasn't moved.
                if tile == start_tile:
                    self.tile_clicked(tile)

    def tile_clicked(self, tile:Vector2) -> None:
        """called when tile is clicked."""
        piece_at = self.board.get_piece_on(tile)
        self.deselect_piece()

        if piece_at != None:
            self.select_piece(piece_at)

    def start_game(self, *players, save_record=False):
        self.set_board()
        super().start_game(*players, save_record=save_record)

    def set_board(self):
        """puts the pieces in there starting position."""
        self.board.clear_board()
        
    def place_piece(self, player:int, tile:Vector2):
        """places piece on board at `tile`"""
        piece = self.piece_type(player)
        self.board.place_piece(tile, piece)
        self.table.pieces.append(piece)

    def select_piece(self, piece:ActivePiece):
        """selectets `piece`."""
        self.piece_selected = piece
        self.piece_selected.selected = True
        self.piece_selected.render_on_top()

    def deselect_piece(self):
        """deselects the selected piece if it exists."""
        if self.piece_selected != None:
            self.piece_selected.selected = False
        self.piece_selected = None

# --------------------------------------------------------------------------------
