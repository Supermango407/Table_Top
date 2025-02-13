from __future__ import annotations
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
from board import ActiveBoard, ActivePiece, PieceMove
import collider


# class TestSprite(collider.DraggableSprite):
#     def __init__(self, position):
#         super().__init__(position, collider=collider.CircleCollider(Vector2(0, 0),  50), show_collider=True)

#     def test(self):
#         print('test')

#     def onlifted(self, started, ended):
#         super().onlifted(started, ended)
#         self.set_position(ended)
#         self.test()
    
#     def draw(self):
#         pygame.draw.circle(self.window, (0, 0, 255), self.position, 50)
#         super().draw()


@dataclass
class Move(PieceMove):
    piece_jumping:CheckersPiece=None


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
            # show_collider=True,
            outline_thickness=2
        )
        self.player = player
        self.is_king = is_king

    def place_on_board(self, board):
        super().place_on_board(board)
        self.collider.radius = self.raduis

    def get_tile_moves(self):
        """gets valid moves for piece."""
        moves:list[Move] = []
        tile_offsets:list[Vector2] = []

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
                # tile empty, add it to tiles.
                moves.append(Move(self, tile))
        
        return moves

    def jump(self):
        """called when `self` is jumped."""
        self.destroy()

    # TODO
    def king(self):
        """changes piece to a king."""
        pass


class Checkers(Game):
    game_vars = GameVars('Checkers', 2)

    def __init__(self):
        super().__init__()
        self.board = ActiveBoard(
            tile_colors=checkers_settings.board['colors'],
            tile_size=checkers_settings.board['tile_size'],
        )
    
    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            tile_clicked = self.board.get_tile_at(pygame.mouse.get_pos())
            if tile_clicked != None: # clicked on board
                if self.board.piece_selected != None:
                    # if valid move than play move
                    for move in self.board.piece_selected.get_tile_moves():
                        if move.tile == tile_clicked:
                            self.play_move(move)
                            break

    def start_game(self, *players, save_record=False):
        self.set_board()
        # TestSprite(Vector2(100, 100))
        return super().start_game(*players, save_record=save_record)

    def play_move(self, move:Move):
        move.piece.move_piece(move.tile)
        if move.piece_jumping != None:
            move.piece_jumping.jump()

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

