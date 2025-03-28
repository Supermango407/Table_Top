from __future__ import annotations
import pygame
import threading
import time
from pygame import Vector2
from dataclasses import dataclass
import sys
sys.path.append('../table_top')
import checkers.checkers_settings as checkers_settings
from window import GameObject, Sprite, Button
import ai as AI
from player import Player
from game import Game, Game_Table, GameVars
from board import PieceMove, Piece, Board
import collider


@dataclass
class Table(Game_Table):
    """curent set up of board
        `turn`: whos turn it currently is.
        `pieces`: pieces on board.
    """
    pieces:list[CheckersPiece]
    
    piece_jumping:CheckersPiece = None 
    # if player jumped a piece, the piece that
    # jumped is the only piece that can jump again,
    # and `piece_jumping` will be set to the piece that jumped.
    # else `piece_jumping` will be set to None, and any piece can move.


@dataclass
class Move(PieceMove):
    piece:CheckersPiece
    piece_jumping:CheckersPiece=None


class CheckersPiece(Piece):
    """a piece for `Checkers` game."""

    def __init__(self, player:int, tile:Vector2, kinging_row:int):
        """
        `player`: the player who controls the piece.
        `tile`: the tile the piece is on.
        `king_row`: the row the piece gets kinged on.
        """
        super().__init__(
            tile=tile,
            color=checkers_settings.piece_colors[player],
            # collider=collider.CircleCollider(
            #     position=Vector2(0, 0),
            #     radius=0, # radiues will be when piece is placed on board.
            # ),
            # show_collider=True,
            outline_thickness=2
        )
        self.player = player
        self.kinging_row = kinging_row
        self.is_king = False

    def draw(self):
        super().draw()

        # draw king crown
        if self.is_king:
            scale = checkers_settings.board['tile_size']//8
            pygame.draw.polygon(
                self.window,
                (255, 255, 0),
                [
                    self.global_position + Vector2(-scale, scale),
                    self.global_position + Vector2(-scale, -scale),
                    self.global_position + Vector2(-scale//2, 0),
                    self.global_position + Vector2(0, -scale),
                    self.global_position + Vector2(scale//2, 0),
                    self.global_position + Vector2(scale, -scale),
                    self.global_position + Vector2(scale, scale),
                ]
        )

    def place_on_board(self, board):
        super().place_on_board(board)
        # self.collider.radius = self.raduis

    def get_tile_moves(self) -> Move:
        """gets valid moves for piece."""
        moves:list[Move] = []
        tile_offsets:list[Vector2] = []

        # if not pieces turn than there are no valid moves
        if self.player != self.board.game_ref.table.turn:
            return []

        # if a piece was just jumped
        piece_jumping:CheckersPiece = self.board.game_ref.table.piece_jumping
        """the piece that just jumped. will be None if no piece was just jumped."""
        if piece_jumping != None and piece_jumping != self:
            return []

        # add the moves up the board if your player 1 or if your a king
        if self.player == 0 or self.is_king:
            tile_offsets.extend([
                Vector2(-1, -1),
                Vector2(1, -1)
            ])

        # add the moves down the board if your player 2 or if your a king
        if self.player == 1 or self.is_king:
            tile_offsets.extend([
                Vector2(-1, 1),
                Vector2(1, 1)
            ])
        
        # filter through the invalid moves
        for tile_offset in tile_offsets:
            tile = self.tile + tile_offset

            # skip tile if it is not on the board.
            if not self.board.tile_on_board(tile):
                continue
            
            piece_on_tile:CheckersPiece = self.board.get_piece_on(tile)
            if piece_on_tile != None:
                # skip tile if frendly piece is on it
                if piece_on_tile.player == self.player:
                    continue

                # if enemy piece is on tile then check the tile behind it.
                tile_behind_piece = tile_offset*2 + self.tile
                # if the tile is on the board and no piece is on it,
                # then you can jump over the enemy piece, and should added
                # the tile behind the enemy piece to tiles
                if self.board.tile_on_board(tile_behind_piece) and self.board.get_piece_on(tile_behind_piece) == None:
                    moves.append(Move(self, tile_behind_piece, piece_on_tile))
            else:
                # tile empty. if didn't just jump than add move to list
                if piece_jumping == None:
                    moves.append(Move(self, tile))
        
        return moves

    def jump(self):
        """called when `self` is jumped."""
        self.destroy()

    def promote(self):
        """changes piece to a king."""
        self.is_king = True


class Checkers(Game):
    game_vars = GameVars('Checkers', 2)

    def __init__(self):
        super().__init__()
        self.table:Table = Table(turn=-1, pieces=[])
        self.board = Board(
            game_ref=self,
            tile_colors=checkers_settings.board['colors'],
            tile_size=checkers_settings.board['tile_size'],
        )

        if self.display_game:
            self.next_turn_button = Button(None, text_value='Next Turn', anchor='bottom', parrent=self)
            self.set_position()
    
    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            tile_clicked = self.board.get_tile_at(pygame.mouse.get_pos())
            if tile_clicked != None: # clicked on board
                # if piece is selected but not dragging
                if self.board.piece_selected != None and not self.board.piece_selected.sprite_dragging:
                    # if valid move than play move
                    for move in self.board.piece_selected.get_tile_moves():
                        if move.tile == tile_clicked:
                            self.play_move(move)
                            break

    def start_game(self, *players, save_record=False):
        self.set_board()
        self.table.piece_jumping = None

        # go to next turn after move is played
        self.auto_next_turn:bool=True

        super().start_game(*players, save_record=save_record)

    def play_move(self, move:Move):
        move.piece.move_piece(move.tile)
        self.auto_next_turn=True
        
        # if jumping a piece
        if move.piece_jumping != None:
            move.piece_jumping.jump()

            # set piece_jumping to the piece thats jumping,
            # so that that is the only piece that can jump again.
            self.table.piece_jumping = move.piece
            
            # set auto_next_turn to false
            self.auto_next_turn=False

        # if selected piece on kinging row than promote the piece
        if not move.piece.is_king and move.piece.tile[1] == move.piece.kinging_row:
            move.piece.promote()
        
        super().play_move(auto_next_turn=self.auto_next_turn)

    def next_turn(self):
        super().next_turn()
        self.table.piece_jumping = None

        # set locked of pieces
        for piece in self.table.pieces:
            if piece.player == self.table.turn:
                piece.locked = False
            else:
                piece.locked = True
        
    def set_board(self):
        """puts the pieces in there starting position."""
        self.board.clear_board()
        
        # self.place_piece(0, Vector2(0, 7), 0)
        # self.place_piece(0, Vector2(2, 7), 0)
        # self.place_piece(0, Vector2(4, 7), 0)
        # self.place_piece(0, Vector2(6, 7), 0)
        # self.place_piece(0, Vector2(1, 6), 0)
        # self.place_piece(0, Vector2(3, 6), 0)
        # self.place_piece(0, Vector2(5, 6), 0)
        # self.place_piece(0, Vector2(7, 6), 0)
        # self.place_piece(0, Vector2(0, 5), 0)
        # self.place_piece(0, Vector2(2, 5), 0)
        # self.place_piece(0, Vector2(4, 5), 0)
        # self.place_piece(0, Vector2(6, 5), 0)

        # self.place_piece(1, Vector2(1, 0), 7)
        # self.place_piece(1, Vector2(3, 0), 7)
        # self.place_piece(1, Vector2(5, 0), 7)
        # self.place_piece(1, Vector2(7, 0), 7)
        # self.place_piece(1, Vector2(0, 1), 7)
        # self.place_piece(1, Vector2(2, 1), 7)
        # self.place_piece(1, Vector2(4, 1), 7)
        # self.place_piece(1, Vector2(6, 1), 7)
        # self.place_piece(1, Vector2(1, 2), 7)
        # self.place_piece(1, Vector2(3, 2), 7)
        # self.place_piece(1, Vector2(5, 2), 7)
        self.place_piece(1, Vector2(7, 2), 7)

    def place_piece(self, player:int, tile:Vector2, king_row:int):
        """places piece on board at `tile`"""
        piece = CheckersPiece(player, tile, king_row)
        self.board.place_piece(tile, piece)
        self.table.pieces.append(piece)

    def click_test(self):
        print(self)

