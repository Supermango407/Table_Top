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
from player import Player


class Piece(Sprite):
    childeren = []

    @staticmethod
    def get_piece_at(position:Vector2):
        for piece in Piece.childeren:
            if piece.position == position:
                return piece
            
        return None

    def __init__(self, color:str, position:Union[Vector2, TilePosition]):
        """
        `color`: the color of the piece.
        `position`: the position on the board the peice is on.
        """
        self.color = color

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
            game_settings.piece_colors[Othello.colors.index(self.color)],
            self.position.get_global_position(),
            game_settings.piece_size
        )

    def flip(self):
        """flips the piece and gives it to the other player."""
        self.color = Othello.colors[1] if self.color == Othello.colors[0] else Othello.colors[0]


class Othello(Game):
    colors = ('B', 'W')
    
    def __init__(self, *players:tuple[Player]):
        super().__init__(*players)
        self.board = Board(
            tile_size=game_settings.board['tile_size'],
            tile_border_width=game_settings.board['border_width'],
            tile_colors=game_settings.board['baground_color'],
            tile_border_color=game_settings.board['border_color']
        )

        self.table = [
            Piece(Othello.colors[0], Vector2(3, 3)),
            Piece(Othello.colors[1], Vector2(3, 4)),
            Piece(Othello.colors[1], Vector2(4, 3)),
            Piece(Othello.colors[0], Vector2(4, 4)),
        ]

        self.next_turn()

    def update(self):
        super().update()

    def next_turn(self):
        super().next_turn()
        if len(self.moves) == 0:
            self.skip_turn()
        else:
            self.turn_text.set_color(game_settings.piece_colors[self.turn])

    def get_winner(self):
        print(len(self.table))
        if len(self.table) >= 64:
            player_pieces = [0, 0]

            # count the number of pieces for each player
            for piece in self.table:
                player_pieces[Othello.colors.index(piece.color)] += 1
            
            if player_pieces[0] > player_pieces[1]:
                return 0
            else:
                return 1
        else:
            return None

    def skip_turn(self):
        """skips the turn of the current player."""
        print('turn skipped')
        self.next_turn()

    def check_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and not self.players[self.turn].is_ai:
                tile_pos = self.board.get_tile_at(pygame.mouse.get_pos())
                if tile_pos != None and self.valid_move(tile_pos):
                        self.play_move(tile_pos)

    def set_moves(self):
        self.moves = []
        moves = self.board.get_all_tiles()

        # delete the moves that arent valid
        for move in moves:
            # if a peice is already there its not valid.
            if self.valid_move(move):
                self.moves.append(move)

    def play_move(self, move:TilePosition):
        piece = self.place_piece(move)
        self.table.append(piece)
        super().play_move(move)

    def record_move(self, move:TilePosition):
        self.history += Othello.colors[self.turn]
        self.history += str(move.get_index())

    def valid_move(self, move:TilePosition):
        # isn't valid if a piece is already there
        if Piece.get_piece_at(move) != None:
            return False
        
        # isn't valid if it doesn't flip any pieces
        if len(self.get_flip_pieces(move)) == 0:
            return False
        
        return True

    def place_piece(self, position:Vector2) -> Piece:
        """places a peice on the board, and returns the piece."""
        piece = Piece(Othello.colors[self.turn], position)
        for piece in self.get_flip_pieces(position):
                piece.flip()
        return piece

    def get_flip_pieces(self, tile:TilePosition) -> list[Piece]:
        """reutrns a list of pieces that will flip if a peice is placed at `position`"""
        pieces = [] # the reutrn value

        # `direction_offets`: the amount you add for each direcion
        # that needs to be checked.
        direction_offets = [
            Vector2(0, -1), # top
            Vector2(1, -1), # top right
            Vector2(1, 0), # right
            Vector2(1, 1), # bottom right
            Vector2(0, 1), # bottom
            Vector2(-1, 1), # bottom left
            Vector2(-1, 0), # left
            Vector2(-1, -1), # top left
        ]
        
        for offset in direction_offets:
            # `pieces_along_direction` will be thrown out
            # if it can't find a piece of the same color
            # as the current player.
            # if it does find one it will be added to `pieces`
            pieces_along_direction = []

            # does range 1-7 cause thats the most the pieces
            # that can be fliped in a specific direction
            for i in range(1, 8):
                piece_at_point_checking = Piece.get_piece_at(tile.position + offset*i)
                
                # if no peice is at the `piece_at_point_checking`
                # then break out of nested loop 
                # and move of to the next direction
                if piece_at_point_checking == None:
                    break

                # if piece found is the same color as player
                # add `pieces_along_direction` to `pieces`
                # then move to the next direction
                if piece_at_point_checking.color == Othello.colors[self.turn]:
                    pieces.extend(pieces_along_direction)
                    break

                # if piece found is a difernt color than player
                # then add it to `piece_at_point_checking`
                else:
                    pieces_along_direction.append(piece_at_point_checking)
        
        return pieces
    
